# OLX Car Cover Scraper (example)

Short: Python script to fetch OLX search results for "car cover" and save to results.json / results.csv.

Two modes:
1. requests: fast, no browser. Works if OLX returns listing HTML directly.
2. selenium: reliable, renders JavaScript. Requires Chrome + chromedriver.

Quick start (Linux / WSL / macOS):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Option A - try requests first
python scraper.py --mode requests
# Option B - if listings don't appear, use Selenium (ensure chromedriver installed)
python scraper.py --mode selenium --headless
```

To put on GitHub:
```bash
git init
git add .
git commit -m "Initial OLX car-cover scraper"
gh repo create olx-car-cover-scraper --public --source=. --remote=origin
git push -u origin main
```
or using plain git + GitHub web: create a repo and push.

Disclaimer: Use responsibly. Respect OLX terms of service and robots.txt. This script is for personal/educational use.
