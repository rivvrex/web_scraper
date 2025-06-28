import requests
from bs4 import BeautifulSoup
import re

def debug_chapter_page():
    url = "https://www.customs.go.jp/english/tariff/2025_04_01/data/e_01.htm"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    tables = soup.find_all('table')
    count = 0
    if len(tables) >= 5:
        main_table = tables[4]
        for row in main_table.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                code_raw = cols[0].get_text(strip=True)
                code = re.sub(r'\D', '', code_raw)
                if not code:
                    continue
                col_texts = [col.get_text(strip=True) for col in cols]
                print(f"Row {count+1}: Code: {code_raw} | Clean: {code} | Columns: {col_texts}")
                count += 1
                if count >= 10:
                    break

if _name_ == "_main_":
    debug_chapter_page()
