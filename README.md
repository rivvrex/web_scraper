# Japan Customs HS Code Scraper

This project provides a Python script that scrapes the Japan Customs website to extract Harmonized System (HS) codes and their descriptions for the 2025 tariff schedule.

## Description

The script (`hs_code_exporter.py`) performs the following tasks:
1. Scrapes the Japan Customs website (2025 version)
2. Extracts HS codes at different levels (HS2, HS4, and HS6)
3. Collects corresponding descriptions for each code
4. Exports the data to an Excel file

## Features

- Scrapes all chapters from the Japan Customs website
- Handles hierarchical HS code structure (2-digit, 4-digit, and 6-digit codes)
- Organizes data by sections and chapters
- Exports data to Excel format for easy analysis
- Includes error handling for failed requests
- Progress tracking during scraping

## Requirements

- Python 3.6 or higher
- Required Python packages are listed in `requirements.txt`

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:
```bash
python hs_code_exporter.py
```

The script will:
1. Start scraping from the main page
2. Process each chapter sequentially
3. Create an Excel file named `HS_2025_Japan_codes.xlsx` with the results

## Output Format

The generated Excel file contains the following columns:
- `HS2`: 2-digit HS code (chapter level)
- `HS4`: 4-digit HS code (heading level)
- `HS6`: 6-digit HS code (subheading level)
- `Description`: Description of the HS code

## Source Data

The data is sourced from the Japan Customs website:
- Base URL: https://www.customs.go.jp/english/tariff/2025_04_01/
- Data version: 2025 (Effective from April 1, 2025)

## Notes

- The script includes a `save_main_page_html()` function for debugging purposes (commented out by default)
- Internet connection is required to run the script
- Processing time depends on the network speed and server response time

## Error Handling

The script includes error handling for:
- Failed HTTP requests
- Missing or malformed data
- Network connectivity issues

Each failed scraping attempt for a chapter is logged but doesn't stop the overall process. 