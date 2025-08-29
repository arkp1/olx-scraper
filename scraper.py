"""olx car-cover scraper
Usage:
  - Option A (fast, no browser): python scraper.py --mode requests
  - Option B (browser, reliable): python scraper.py --mode selenium
Outputs: results.json and results.csv in current directory.
"""
import argparse, json, csv, time, sys
from urllib.parse import urljoin

def parse_with_requests(url):
    import requests
    from bs4 import BeautifulSoup
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    items = []

    for a in soup.select('a[href*="/item/"]'):
        title = a.get_text(strip=True)
        href = a.get('href')
        if not title or not href:
            continue
        items.append({
            "title": title,
            "url": urljoin(url, href)
        })
    return items

def parse_with_selenium(url, headless=True):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    opts = Options()
    if headless:
        opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--lang=en-US')
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    # scroll to load more
    SCROLLS = 6
    for _ in range(SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)
    elems = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/item/"]')
    seen = set()
    items = []
    for e in elems:
        try:
            href = e.get_attribute('href')
            title = e.text.strip()
        except Exception:
            continue
        if not href or href in seen:
            continue
        seen.add(href)
        items.append({"title": title, "url": href})
    driver.quit()
    return items

def save(items, out_prefix='results'):
    with open(out_prefix + '.json','w',encoding='utf-8') as f:
        json.dump(items,f,ensure_ascii=False,indent=2)
    keys = ['title','url']
    with open(out_prefix + '.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            writer.writerow({k:it.get(k,'') for k in keys})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', default='https://www.olx.in/items/q-car-cover', help='OLX search URL')
    p.add_argument('--mode', choices=['requests','selenium'], default='requests')
    p.add_argument('--headless', action='store_true', help='Use headless browser when selenium mode')
    args = p.parse_args()
    url = args.url
    try:
        if args.mode == 'requests':
            items = parse_with_requests(url)
            if not items:
                print('No items found with requests parser. Try --mode selenium', file=sys.stderr)
            save(items)
            print(f'Saved {len(items)} items to results.json and results.csv')
        else:
            items = parse_with_selenium(url, headless=args.headless)
            save(items)
            print(f'Saved {len(items)} items to results.json and results.csv')
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
