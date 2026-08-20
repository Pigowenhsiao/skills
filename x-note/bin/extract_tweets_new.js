
(function() {
    const cards = document.querySelectorAll('article[data-testid="tweet"]');
    const out = [];
    const seen = new Set();
    cards.forEach(card => {
        try {
            // Get status ID from link
            const links = card.querySelectorAll('a[href*="/status/"]');
            let status_id = null;
            for (const l of links) {
                const m = l.getAttribute("href").match(/\/status\/(\d+)/);
                if (m) { status_id = m[1]; break; }
            }
            if (!status_id || seen.has(status_id)) return;
            seen.add(status_id);

            const url = "https://x.com/i/status/" + status_id;
            const time = card.querySelector("time");
            const time_iso = time ? time.getAttribute("datetime") : null;
            const taipei_date = time_iso ? new Date(time_iso).toLocaleDateString("en-CA", {timeZone: "Asia/Taipei"}) : null;

            // Text
            const textEl = card.querySelector('[data-testid="tweetText"]');
            const text = textEl ? textEl.textContent : (card.querySelector('div[lang]')?.textContent || "");

            // Author
            const handleEl = card.querySelector('[data-testid="User-Name"]') || card;
            const handleLink = handleEl.querySelector('a[href*="/"]');
            const handle = handleLink ? handleLink.getAttribute("href").replace("/", "") : "";
            const displayName = handleEl.querySelector("span")?.textContent || "";

            // Counts - look for the interaction stat elements
            const stats = card.querySelectorAll('[data-testid]');
            let likes = 0, reposts = 0, replies = 0;
            stats.forEach(el => {
                const key = el.getAttribute('data-testid');
                const txt = el.textContent || "";
                const n = txt.match(/[\d,]+/);
                const num = n ? parseInt(n[0].replace(/,/g, ""), 10) : 0;
                if (key === 'like') likes = num;
                if (key === 'retweet') reposts = num;
                if (key === 'reply') replies = num;
            });

            out.push({
                status_id, url, time_utc: time_iso, taipei_date,
                text_preview: text.substring(0, 300),
                author_display: displayName, author_handle: handle,
                likes, reposts, replies
            });
        } catch(e) {}
    });
    return out;
})()
