import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com"
}


def download_file(session, url, local_path):
    try:
        response = session.get(url, timeout=15, headers=HEADERS)
        response.raise_for_status()

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Downloaded: {url}")
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")


def clone_website(url, output_folder="cloned_site"):
    if not url.startswith("http"):
        print("❌ Please provide a valid URL starting with http or https")
        return

    os.makedirs(output_folder, exist_ok=True)

    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    print("🚀 Cloning website...")

    session = requests.Session()

    # Download main page
    try:
        response = session.get(url, timeout=15, headers=HEADERS)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        print(f"❌ Failed to fetch main page: {e}")
        return

    # Save main page
    main_file = os.path.join(output_folder, "index.html")
    with open(main_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Main page saved as index.html")

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all assets
    assets = set()

    for tag in soup.find_all(["link", "img", "script"]):
        if tag.name == "link":
            link = tag.get("href")
        else:
            link = tag.get("src")

        if link:
            assets.add(link)

    # Download assets
    for asset in assets:
        full_url = urllib.parse.urljoin(base_url, asset)

        # skip external websites
        if not full_url.startswith(base_url):
            continue

        # local path
        parsed = urllib.parse.urlparse(full_url)
        asset_path = parsed.path.split("?")[0]  # remove ?v=123

        # skip directories or empty paths
        if not asset_path or asset_path.endswith("/") or asset_path == "/":
            continue

        local_path = os.path.join(output_folder, asset_path.lstrip("/"))

        download_file(session, full_url, local_path)

    print(f"\n✅ Done! Website cloned into: {output_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clone_site.py <url>")
        sys.exit(1)

    target_url = sys.argv[1]
    clone_website(target_url)