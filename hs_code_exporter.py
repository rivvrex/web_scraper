import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

BASE_URL = "https://www.customs.go.jp/english/tariff/2025_04_01/"
MAIN_URL = BASE_URL + "index.htm"
OUTPUT_FILE = "HS_2025_Japan_codes.xlsx"


def get_chapter_links():
    """
    Scrape the main page to get all chapter 'Tariff rate' links.
    Returns: List of dicts with section, chapter, desc, url.
    """
    resp = requests.get(MAIN_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    chapter_links = []
    # Find all tables with class 'standard'
    tables = soup.find_all('table', class_='standard')
    for table in tables:
        # Section: try to get from previous <p><strong>...</strong></p> or from <caption>
        section = None
        prev = table.find_previous_sibling()
        while prev and not (prev.name == 'p' and prev.find('strong')):
            prev = prev.find_previous_sibling()
        if prev and prev.find('strong'):
            section = prev.find('strong').get_text(strip=True)
        if not section and table.caption:
            section = table.caption.get_text(strip=True)
        # For each row, extract chapter, desc, and link
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if len(cols) >= 3:
                chapter = cols[0].get_text(strip=True)
                desc = cols[1].get_text(strip=True)
                link = cols[2].find('a')
                if link and 'href' in link.attrs:
                    url = BASE_URL + link['href']
                    chapter_links.append({
                        'section': section,
                        'chapter': chapter,
                        'desc': desc,
                        'url': url
                    })
    return chapter_links


def parse_chapter_page_flat(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    tables = soup.find_all('table')
    flat_rows = []
    if len(tables) >= 5:
        main_table = tables[4]
        for row in main_table.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 3:
                code_raw = cols[0].get_text(strip=True)
                desc = cols[2].get_text(strip=True)
                if not desc:
                    continue  # skip if description is missing
                code = re.sub(r'\D', '', code_raw)
                hs2 = hs4 = hs6 = ""
                if len(code) == 2:
                    hs2 = code
                elif len(code) == 4:
                    hs4 = code
                elif len(code) == 6:
                    hs6 = code
                else:
                    continue
                flat_rows.append({
                    'HS2': hs2,
                    'HS4': hs4,
                    'HS6': hs6,
                    'Description': desc
                })
    return flat_rows


def save_main_page_html():
    resp = requests.get(MAIN_URL)
    resp.raise_for_status()
    os.makedirs('nts', exist_ok=True)
    with open('nts/index.html', 'wb') as f:
        f.write(resp.content)
    print('Saved main page HTML to nts/index.html')


def main():
    print(f"Scraping main page: {MAIN_URL}")
    chapter_links = get_chapter_links()
    print(f"Found {len(chapter_links)} chapters.")
    all_flat_rows = []
    for i, ch in enumerate(chapter_links, 1):
        print(f"[{i}/{len(chapter_links)}] Scraping {ch['chapter']} - {ch['desc']}...")
        try:
            flat_rows = parse_chapter_page_flat(ch['url'])
            all_flat_rows.extend(flat_rows)
        except Exception as e:
            print(f"  Failed to scrape {ch['url']}: {e}")
    if not all_flat_rows:
        print("No data scraped. Exiting.")
        return
    df = pd.DataFrame(all_flat_rows)
    print(f"Exporting {len(df)} rows to {OUTPUT_FILE}...")
    df.to_excel(OUTPUT_FILE, index=False)
    print("Done.")


if __name__ == "__main__":
    # save_main_page_html()
    main()