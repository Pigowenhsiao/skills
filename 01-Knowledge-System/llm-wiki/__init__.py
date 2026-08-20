"""llm-wiki — PigoVault Knowledge Base System

Due to the hyphenated directory name 'llm-wiki', Python absolute imports
don't work normally. Import sub-modules directly via importlib:

    import sys, importlib.util
    sys.path.insert(0, "E:/python_Code/Agent/skills/01-Knowledge-System")
    from llm_wiki import check_session_start  # won't work due to hyphen

Instead use direct imports in your code:

    from llm_wiki.config import get_config, load_config
    from llm_wiki.utils import health_check, generate_report
    from llm_wiki.youtube_handler import fetch_youtube_metadata

Or see tests/test_utils.py for the full importlib pattern.
"""
__version__ = "2.0.0"
