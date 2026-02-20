import requests
from bs4 import BeautifulSoup

def scrape_metadata(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Helper to safely get meta content
        def get_meta(props):
            for p in props:
                tag = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
                if tag and tag.get("content"): return tag["content"]
            return None

        title = get_meta(["og:title", "twitter:title"]) or (soup.title.string if soup.title else url)
        desc = get_meta(["og:description", "description", "twitter:description"])
        image = get_meta(["og:image", "twitter:image"])

        return {"title": title, "description": desc, "image": image}
    except Exception as e:
        print(f"Scrape failed: {e}")
        return {"title": url, "description": "No metadata found", "image": None}