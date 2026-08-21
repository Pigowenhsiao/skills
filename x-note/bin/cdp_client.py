"""
cdp_client.py
=============
CDP (Chrome DevTools Protocol) client with auto-reconnect, heartbeat,
and cookie injection support.

Features:
- Auto-reconnect with exponential backoff (1s, 2s, 4s)
- Heartbeat to keep connection alive
- Cookie injection using Network.setCookie
- Graceful error handling for WebSocket/connection errors

Usage:
    from cdp_client import CDPClient, cdp_send, cdp_eval

    client = CDPClient(port=19825, cookies_file="x_cookies.json")
    client.connect()
    result = client.send("Page.navigate", {"url": "https://x.com/user"})
    response = client.eval("document.title")
    client.close()
"""
import json
import logging
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

import websocket

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper functions (standalone, work with raw websocket)
# ---------------------------------------------------------------------------

def cdp_send(ws, method: str, params: dict | None = None, msg_id: int = 1, timeout: float = 30.0) -> dict | None:
    """
    Send a CDP command and wait for response.

    Args:
        ws: WebSocket connection
        method: CDP method name (e.g., "Page.navigate")
        params: Optional dict of method parameters
        msg_id: Message ID for matching request/response
        timeout: Maximum time to wait for response

    Returns:
        Response dict or None if timeout/error
    """
    if ws is None or not ws.connected:
        return None

    payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
    try:
        ws.send(payload)
    except (
        websocket.WebSocketException,
        ConnectionResetError,
        BrokenPipeError,
    ) as e:
        logger.warning(f"cdp_send: failed to send {method}: {e}")
        return None

    deadline = time.time() + timeout
    remaining = deadline - time.time()
    while remaining > 0:
        try:
            ws.settimeout(min(remaining, 1.0))  # Check periodically for timeout updates
            raw = ws.recv()
            result = json.loads(raw)
            if result.get("id") == msg_id:
                return result
            # Handle async events (method calls without matching id)
            if "method" in result:
                logger.debug(f"cdp_send: async event: {result.get('method')}")
            remaining = deadline - time.time()
        except (
            websocket.WebSocketException,
            ConnectionResetError,
            BrokenPipeError,
        ) as e:
            logger.warning(f"cdp_send: recv failed during {method}: {e}")
            return None
        except Exception as e:
            logger.warning(f"cdp_send: unexpected error during {method}: {e}")
            remaining = deadline - time.time()

    logger.warning(f"cdp_send: timeout waiting for {method} (id={msg_id})")
    return None


def cdp_eval(ws, expression: str, msg_id: int = 1, timeout: float = 30.0) -> str:
    """
    Evaluate a JavaScript expression via Runtime.evaluate.

    Args:
        ws: WebSocket connection
        expression: JavaScript code to execute
        msg_id: Message ID for matching request/response
        timeout: Maximum time to wait for response

    Returns:
        String result (JSON-encoded for objects/arrays), or empty string on error
    """
    res = cdp_send(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True,
        "awaitPromise": True,
    }, msg_id=msg_id, timeout=timeout)

    if not res:
        return ""

    result = res.get("result", {})
    if isinstance(result, dict):
        result = result.get("result", {})

    val = result.get("value") if isinstance(result, dict) else None
    if val is None:
        return ""

    # Serialize objects/arrays as JSON, return primitives as-is
    if isinstance(val, (dict, list)):
        return json.dumps(val, ensure_ascii=False)
    return str(val)


# ---------------------------------------------------------------------------
# CDPClient class
# ---------------------------------------------------------------------------

class CDPClient:
    """
    Chrome DevTools Protocol client with auto-reconnect, heartbeat,
    and cookie injection capabilities.

    Attributes:
        port: CDP port number (default 19825)
        cookies_file: Path to cookies JSON file
        ws_url: WebSocket URL for CDP connection
        ws: The underlying WebSocket connection
    """

    def __init__(
        self,
        port: int = 19825,
        cookies_file: str | Path | None = None,
        heartbeat_interval: float = 30.0,
        max_backoff: float = 4.0,
        connect_timeout: float = 60.0,
    ):
        """
        Initialize CDP client.

        Args:
            port: CDP port (default 19825)
            cookies_file: Path to cookies file for injection (optional)
            heartbeat_interval: Seconds between heartbeat pings (default 30s)
            max_backoff: Maximum backoff delay in seconds (default 4s)
            connect_timeout: WebSocket connection timeout (default 60s)
        """
        self.port = port
        self.cookies_file = Path(cookies_file) if cookies_file else None
        self.heartbeat_interval = heartbeat_interval
        self.max_backoff = max_backoff
        self.connect_timeout = connect_timeout

        self.ws: Optional[websocket.WebSocket] = None
        self.ws_url: Optional[str] = None
        self._msg_id = 1
        self._lock = threading.Lock()
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._heartbeat_stop = threading.Event()
        self._connected = False
        self._reconnect_attempts = 0

    def _get_msg_id(self) -> int:
        """Generate unique message ID."""
        with self._lock:
            self._msg_id += 1
            return self._msg_id

    # ---------------------------------------------------------------------------
    # Connection management
    # ---------------------------------------------------------------------------

    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._connected and self.ws is not None and self.ws.connected

    def _check_port_alive(self) -> bool:
        """
        Check if CDP port is accepting connections using urllib.

        Returns:
            True if port responds, False otherwise
        """
        try:
            url = f"http://localhost:{self.port}/json"
            with urllib.request.urlopen(url, timeout=5) as resp:
                return resp.status == 200
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            ConnectionRefusedError,
            OSError,
        ):
            return False

    def _get_ws_url(self) -> str:
        """
        Get WebSocket URL for the first available page tab.

        Returns:
            WebSocket debugger URL string

        Raises:
            RuntimeError: If no page tab found or CDP not available
        """
        if not self._check_port_alive():
            raise RuntimeError(f"CDP port {self.port} is not responding")

        url = f"http://localhost:{self.port}/json"
        with urllib.request.urlopen(url, timeout=10) as resp:
            pages = json.loads(resp.read())

        for page in pages:
            if page.get("type") == "page" and "webSocketDebuggerUrl" in page:
                return page["webSocketDebuggerUrl"]

        raise RuntimeError(f"No usable page tab found on port {self.port}")

    def _establish_connection(self) -> bool:
        """
        Establish WebSocket connection to CDP.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.ws_url = self._get_ws_url()
            self.ws = websocket.create_connection(
                self.ws_url,
                timeout=self.connect_timeout,
            )
            self._connected = True
            self._reconnect_attempts = 0
            logger.info(f"CDP connected: {self.ws_url[:80]}...")
            return True
        except Exception as e:
            logger.error(f"CDP connection failed: {e}")
            self._connected = False
            return False

    def reconnect(self) -> bool:
        """
        Attempt to reconnect with exponential backoff (1s, 2s, 4s).

        Returns:
            True if reconnected successfully, False if max attempts reached
        """
        backoff_delays = [1.0, 2.0, 4.0]
        max_attempts = len(backoff_delays)

        for attempt in range(max_attempts):
            delay = backoff_delays[min(attempt, len(backoff_delays) - 1)]
            logger.info(f"CDP reconnect attempt {attempt + 1}/{max_attempts} after {delay}s backoff...")

            # Close existing connection if any
            self._close_unsafe()

            time.sleep(delay)

            if self._establish_connection():
                # Inject cookies on successful reconnect
                self._inject_cookies()
                return True

        logger.error("CDP reconnect failed after all backoff attempts")
        self._connected = False
        return False

    def connect(self) -> bool:
        """
        Connect to CDP, optionally inject cookies.

        Returns:
            True if connected successfully, False otherwise
        """
        if self.is_connected():
            return True

        if not self._establish_connection():
            return False

        # Inject cookies if file provided
        if self.cookies_file and self.cookies_file.exists():
            self._inject_cookies()

        # Start heartbeat thread
        self._start_heartbeat()

        return True

    # ---------------------------------------------------------------------------
    # Cookie injection
    # ---------------------------------------------------------------------------

    def load_cookies(self) -> list[dict]:
        """
        Load cookies from JSON file.

        Supports multiple formats:
        - Chrome's cookies SQLite export (list of dicts with name, value, domain, etc.)
        - Netscape cookies format (array of objects)

        Returns:
            List of cookie dictionaries
        """
        if not self.cookies_file or not self.cookies_file.exists():
            logger.warning(f"Cookies file not found: {self.cookies_file}")
            return []

        try:
            raw = self.cookies_file.read_text(encoding="utf-8")
            cookies = json.loads(raw)

            if not isinstance(cookies, list):
                logger.warning("Cookies file does not contain a list")
                return []

            # Validate minimum required fields
            validated = []
            for c in cookies:
                if not isinstance(c, dict):
                    continue
                name = c.get("name") or c.get("Name")
                value = c.get("value") or c.get("Value")
                if name:
                    validated.append(c)

            logger.info(f"Loaded {len(validated)} cookies from {self.cookies_file.name}")
            return validated

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in cookies file: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return []

    def _inject_cookies(self) -> int:
        """
        Inject cookies using Network.setCookie for each cookie.

        Returns:
            Number of cookies successfully injected
        """
        cookies = self.load_cookies()
        if not cookies:
            return 0

        injected = 0
        for cookie in cookies:
            # Build Network.setCookie parameters
            params = {
                "name": cookie.get("name") or cookie.get("Name", ""),
                "value": cookie.get("value") or cookie.get("Value", ""),
            }

            # Optional fields
            domain = cookie.get("domain") or cookie.get("Domain")
            if domain:
                params["domain"] = domain

            path = cookie.get("path") or cookie.get("Path")
            if path:
                params["path"] = path

            secure = cookie.get("secure") or cookie.get("Secure")
            if secure is not None:
                params["secure"] = bool(secure)

            http_only = cookie.get("httpOnly") or cookie.get("http_only")
            if http_only is not None:
                params["httpOnly"] = bool(http_only)

            same_site = cookie.get("sameSite") or cookie.get("same_site")
            if same_site:
                params["sameSite"] = same_site

            expires = cookie.get("expires") or cookie.get("expiresDate") or cookie.get("Expires")
            if expires:
                try:
                    params["expires"] = float(expires)
                except (ValueError, TypeError):
                    pass

            try:
                resp = self.send("Network.setCookie", params)
                if resp and resp.get("result", {}).get("success"):
                    injected += 1
                else:
                    logger.debug(f"setCookie failed for {params['name']}: {resp}")
            except Exception as e:
                logger.warning(f"Failed to inject cookie {params.get('name')}: {e}")

        logger.info(f"Injected {injected}/{len(cookies)} cookies")
        return injected

    # ---------------------------------------------------------------------------
    # Heartbeat
    # ---------------------------------------------------------------------------

    def _heartbeat_loop(self):
        """Background thread to send periodic pings."""
        while not self._heartbeat_stop.wait(timeout=self.heartbeat_interval):
            if not self.is_connected():
                logger.warning("CDP heartbeat: connection lost")
                break

            try:
                # Use Runtime.evaluate with a simple expression
                resp = self.send("Runtime.evaluate", {
                    "expression": "1 + 1",
                    "returnByValue": True,
                }, timeout=10.0)
                if resp is None:
                    logger.warning("CDP heartbeat: no response, connection may be dead")
                    self._trigger_reconnect()
                    break
            except Exception as e:
                logger.warning(f"CDP heartbeat failed: {e}")
                self._trigger_reconnect()
                break

    def _trigger_reconnect(self):
        """Trigger async reconnection in background."""
        def _async_reconnect():
            logger.info("CDP: triggering async reconnect...")
            self._stop_heartbeat()
            self.reconnect()
            if self.is_connected():
                self._start_heartbeat()

        t = threading.Thread(target=_async_reconnect, daemon=True)
        t.start()

    def _start_heartbeat(self):
        """Start the heartbeat thread."""
        self._stop_heartbeat()
        self._heartbeat_stop.clear()
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            name="cdp-heartbeat",
            daemon=True,
        )
        self._heartbeat_thread.start()

    def _stop_heartbeat(self):
        """Stop the heartbeat thread."""
        self._heartbeat_stop.set()
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=2.0)
        self._heartbeat_thread = None

    # ---------------------------------------------------------------------------
    # Send / Eval
    # ---------------------------------------------------------------------------

    def send(
        self,
        method: str,
        params: dict | None = None,
        timeout: float = 30.0,
        auto_reconnect: bool = True,
    ) -> dict | None:
        """
        Send a CDP command with optional auto-reconnect.

        Args:
            method: CDP method name
            params: Method parameters
            timeout: Response timeout
            auto_reconnect: Whether to attempt reconnect on failure

        Returns:
            Response dict or None
        """
        msg_id = self._get_msg_id()

        try:
            result = cdp_send(self.ws, method, params, msg_id, timeout)

            if result is None and auto_reconnect and self.is_connected():
                # Connection might be dead, try to detect and reconnect
                logger.warning(f"CDP send returned None for {method}, checking connection...")
                if not self._check_port_alive():
                    logger.info("CDP port not responding, attempting reconnect...")
                    if self.reconnect():
                        # Retry once after reconnect
                        msg_id = self._get_msg_id()
                        result = cdp_send(self.ws, method, params, msg_id, timeout)

            return result

        except (
            websocket.WebSocketException,
            ConnectionResetError,
            BrokenPipeError,
        ) as e:
            logger.warning(f"CDP send error for {method}: {e}")
            if auto_reconnect:
                if self.reconnect():
                    msg_id = self._get_msg_id()
                    return cdp_send(self.ws, method, params, msg_id, timeout)
            return None

    def eval(self, expression: str, timeout: float = 30.0) -> str:
        """
        Evaluate JavaScript expression.

        Args:
            expression: JavaScript code
            timeout: Response timeout

        Returns:
            String result or empty string on error
        """
        msg_id = self._get_msg_id()

        try:
            return cdp_eval(self.ws, expression, msg_id, timeout)
        except (
            websocket.WebSocketException,
            ConnectionResetError,
            BrokenPipeError,
        ) as e:
            logger.warning(f"CDP eval error: {e}")
            return ""

    # ---------------------------------------------------------------------------
    # Health check
    # ---------------------------------------------------------------------------

    def health_check(self) -> dict[str, Any]:
        """
        Perform health check on CDP connection.

        Returns:
            Dict with status, port_alive, connected, ws_connected fields
        """
        port_alive = self._check_port_alive()
        ws_connected = self.is_connected()

        # Try a simple CDP command if websocket is connected
        cdp_ok = False
        if ws_connected:
            try:
                resp = self.send("Runtime.evaluate", {
                    "expression": "true",
                    "returnByValue": True,
                }, timeout=5.0)
                cdp_ok = resp is not None
            except Exception:
                cdp_ok = False

        return {
            "status": "healthy" if (port_alive and ws_connected and cdp_ok) else "unhealthy",
            "port_alive": port_alive,
            "connected": ws_connected,
            "ws_connected": ws_connected,
            "cdp_ok": cdp_ok,
            "port": self.port,
            "ws_url": self.ws_url[:80] + "..." if self.ws_url else None,
        }

    # ---------------------------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------------------------

    def _close_unsafe(self):
        """Close WebSocket without locks (for internal use)."""
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None
        self._connected = False

    def close(self):
        """Close the CDP connection and stop heartbeat."""
        self._stop_heartbeat()
        with self._lock:
            self._close_unsafe()
        logger.info("CDP client closed")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __del__(self):
        try:
            self._stop_heartbeat()
            self._close_unsafe()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Convenience factory / context manager
# ---------------------------------------------------------------------------

def create_cdp_client(
    port: int = 19825,
    cookies_file: str | Path | None = None,
    connect: bool = True,
) -> CDPClient:
    """
    Factory function to create and optionally connect a CDPClient.

    Args:
        port: CDP port
        cookies_file: Path to cookies file
        connect: Whether to immediately connect

    Returns:
        Connected CDPClient instance
    """
    client = CDPClient(port=port, cookies_file=cookies_file)
    if connect:
        if not client.connect():
            raise RuntimeError(f"Failed to connect to CDP on port {port}")
    return client
