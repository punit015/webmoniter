import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template
import threading
import datetime

# ------------- CONFIG ----------------

urls = [
    "https://eazzyone.com/top-10-webgames-site-to-play-free-online-games/",
    "https://eazzyone.com/gogoanime-watch-and-download-anime-online/",
    "https://eazzyone.com/downloadhub-movies-download-hindi/"
]

check_interval = 60  # 1 minute for testing
MAX_RETRIES = 3
RETRY_DELAY = 60  # 1 minute

# Store alerts history
alerts = []

# ------------------------------------

def fetch_site_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

app = Flask('')

@app.route('/')
def home():
    return render_template('index.html', alerts=list(reversed(alerts[-10:])))

def run():
    app.run(host='0.0.0.0', port=3000, debug=False)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

def main():
    keep_alive()

    print("Starting monitoring...")
    old_contents = {}

    for url in urls:
        content = fetch_site_text(url)
        if content:
            old_contents[url] = content
            test_alert = f"[ALERT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initial monitoring started for {url}"
            alerts.append(test_alert)
            print(test_alert)
        else:
            old_contents[url] = ""

    while True:
        time.sleep(check_interval)
        today = datetime.date.today().isoformat()
        for url in urls:
            new_content = fetch_site_text(url)
            if new_content is None:
                continue
            if new_content != old_contents[url]:
                alert_msg = f"[ALERT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Content changed on {url}"
                print(alert_msg)
                alerts.append(alert_msg)
                old_contents[url] = new_content
            else:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] No change detected on {url}")

if __name__ == "__main__":
    main()
