import pandas as pd
from sec_edgar_downloader import Downloader

# Initialize downloader
dl = Downloader("YourCompanyName", "your-email@example.com")

# Define companies (example: Apple, Microsoft, Amazon)
companies = {
    "AAPL": "0000320193",  # Apple CIK
    "MSFT": "0000789019",  # Microsoft CIK
    "AMZN": "0001018724"   # Amazon CIK
}

# Create empty DataFrame
df = pd.DataFrame(columns=["Company", "Fiscal Year", "Total Revenue", "Net Income", 
                           "Total Assets", "Total Liabilities", "Operating Cash Flow"])

# Download 10-K filings and extract data
for ticker, cik in companies.items():
    dl.get("10-K", cik, limit=3)  # Last 3 filings
    
    # Parse filings (simplified example; actual parsing requires XBRL/HTML extraction)
    # Use tools like `beautifulsoup` or `xbrl` library for accurate extraction
    # This example uses mocked data for illustration
    for year in [2024, 2023, 2022]:  # Replace with actual fiscal years
        # REAL IMPLEMENTATION: 
        # 1. Locate filing in ./sec-edgar-filings/{cik}/10-K/
        # 2. Extract financials from XBRL/HTML tables
        # 3. Map to: Revenue, Net Income, Assets, Liabilities, OpCashFlow
        
        # Mock data (replace with actual extracted values)
        mock_data = {
            "Company": ticker,
            "Fiscal Year": year,
            "Total Revenue": 100_000_000 * (year - 2020),
            "Net Income": 20_000_000 * (year - 2020),
            "Total Assets": 500_000_000 * (year - 2020),
            "Total Liabilities": 300_000_000 * (year - 2020),
            "Operating Cash Flow": 50_000_000 * (year - 2020)
        }
        df = pd.concat([df, pd.DataFrame([mock_data])], ignore_index=True)

# Save to CSV
df.to_csv("10k_financials.csv", index=False)
