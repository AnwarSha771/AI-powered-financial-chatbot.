from sec_edgar_downloader import Downloader
import os
import pandas as pd
from bs4 import BeautifulSoup
import re

# Initialize a downloader instance. Save in the current directory.
dl = Downloader("MyCompany", "email@example.com", ".")

# List of companies (tickers) and their CIK (if known, else we can use ticker)
# We can map tickers to CIK, but for simplicity, we use tickers and let the downloader find CIK.
# However, it's better to use CIK. We can get CIK from a mapping or use the ticker.

# For example, we'll use:
companies = {
    'AAPL': '0000320193',   # Apple Inc.
    'MSFT': '0000789019',   # Microsoft
    'GOOGL': '0001652044',   # Alphabet (Google)
}

# We want the last three 10-K filings for each company.
# Note: The last three fiscal years might not be calendar years. We'll get the last three 10-Ks.

# Create a DataFrame to store the results
df = pd.DataFrame(columns=['Company', 'Fiscal Year', 'Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities', 'Cash Flow from Operating Activities'])

for ticker, cik in companies.items():
    # Download the last three 10-K filings
    dl.get("10-K", cik, limit=3)

    # The filings are saved in `./sec-edgar-filings/{cik}/10-K/{accession_number}/full-submission.txt`
    # We need to parse each filing.

    base_path = f"./sec-edgar-filings/{cik}/10-K"
    # List the directories (each accession is a directory)
    for accession_dir in os.listdir(base_path):
        filing_path = os.path.join(base_path, accession_dir, 'full-submission.txt')
        # Read the filing
        with open(filing_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the filing to extract the financials.
        # This is the hard part because the filing is a long text and HTML.
        # We can look for the financial statements in the HTML.

        # We'll use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(content, 'html.parser')

        # We need to find the financial statements. They are usually in tables.
        # We can look for the table that contains the terms we need.

        # Alternatively, we can look for the specific tags that have the data.
        # This is highly dependent on the filing and can break.

        # We are going to look for the following terms in the table rows:
        #   Total Revenue
        #   Net Income
        #   Total Assets
        #   Total Liabilities
        #   Cash Flow from Operating Activities

        # We'll search for each term and then try to get the value from the adjacent cell.

        # This is a simplified approach and may not work for all filings.

        data = {
            'Total Revenue': None,
            'Net Income': None,
            'Total Assets': None,
            'Total Liabilities': None,
            'Cash Flow from Operating Activities': None
        }

        # We look for all tables and then rows
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                text_cells = [cell.get_text(strip=True) for cell in cells]
                # We'll check each cell for the term
                for i, text in enumerate(text_cells):
                    for term in data.keys():
                        if term in text:
                            # The value might be in the next cell or in the same row but next column
                            if i < len(text_cells) - 1:
                                # Try to extract a number from the next cell
                                next_cell = text_cells[i+1]
                                # Remove non-numeric characters (except decimal and minus)
                                value_str = re.sub(r'[^\d.-]', '', next_cell)
                                if value_str:
                                    try:
                                        value = float(value_str)
                                        data[term] = value
                                    except:
                                        pass

        # We also need the fiscal year. We can get it from the filing date or from the document.
        # The filing date is in the header. We can look for the period of report.
        # We can also get the fiscal year from the document.

        # Let's assume we get the filing date from the accession directory: the accession number has the date.
        # The accession number is like: 0000320193-20-000096, and the date is 2020-09-26 -> fiscal year 2020.
        # Actually, the accession number: the first part is CIK, then two digits of year, then the rest.
        # We can extract the year from the accession_dir: it's in the form YYYYMMDD, but the accession_dir is the accession number without the dashes? Actually, the directory is named by the accession number.

        # Alternatively, we can parse the filing date from the filing.

        # We'll look for the period of report in the filing.
        # The period of report is usually in the header of the 10-K.

        # For simplicity, we'll use the year from the filing date in the file name? Not exact.

        # Instead, we can use the filing date from the SEC metadata. But we don't have that.

        # Alternatively, we can skip and use the year from the directory structure? Not reliable.

        # Let's try to extract from the document:
        # Look for the string "For the fiscal year ended"
        fiscal_year = None
        match = re.search(r'For the fiscal year ended\s*[^\d]*(\d{4})', content, re.IGNORECASE)
        if match:
            fiscal_year = match.group(1)
        else:
            # Try another pattern
            match = re.search(r'fiscal year ended\s*[^\d]*(\d{4})', content, re.IGNORECASE)
            if match:
                fiscal_year = match.group(1)

        # If we found the fiscal year, then we can use it.
        if fiscal_year:
            # Append to the DataFrame
            new_row = {
                'Company': ticker,
                'Fiscal Year': fiscal_year,
                'Total Revenue': data['Total Revenue'],
                'Net Income': data['Net Income'],
                'Total Assets': data['Total Assets'],
                'Total Liabilities': data['Total Liabilities'],
                'Cash Flow from Operating Activities': data['Cash Flow from Operating Activities']
            }
            df = df.append(new_row, ignore_index=True)

# Save the DataFrame to a CSV file
df.to_csv('financial_data.csv', index=False)
