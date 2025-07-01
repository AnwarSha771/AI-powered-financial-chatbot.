# AI-powered-financial-chatbot.
For each company, to find the 10-K filings for the last three fiscal years. Extract the following financial figures: Total Revenue, Net Income, Total Assets, Total Liabilities, and Cash Flow from Operating Activities.

Identifying the companies for which to find 10-K filings
Finding the 10-K filings for the last three fiscal years for each company
Extracting financial figures from the 10-K filings: Total Revenue, Net Income, Total Assets, Total Liabilities, and Cash Flow from Operating Activities
Compiling the extracted financial data into a CSV file
We are going to:
Identify the companies (but the user didn't specify companies, so we need to clarify or assume we have a list)
For each company, we need to get the 10-K filings for the last three fiscal years
From each 10-K, extract: Total Revenue, Net Income, Total Assets, Total Liabilities, Cash Flow from Operating Activities
Compile into a CSV file
However, the user did not specify the companies. We have two options:
Ask the user for a list of companies
Assume we are going to use a predefined list (but we don't have one)
Given the ambiguity, we must ask for clarification
But note: The user might be expecting a general approach. Alternatively, we can provide a solution that works for a given list of companies
Let me re-read the query: "For each company" implies that we have a list of companies. But the user didn't provide any
We can:
Ask the user to provide a list of companies (ticker symbols or company names)
Alternatively, if we are to demonstrate, we can use a sample list
But the user also asks for a CSV file. We cannot generate a CSV without data
Given the constraints, I'll outline the steps and then provide a sample CSV for a few companies
Steps:
Obtain the list of companies: We need a list. Let's assume we are given a list of tickers. For example, we'll use: ['AAPL', 'MSFT', 'GOOGL']
For each company, get the 10-K filings for the last three fiscal years:
We can use the SEC Edgar API or a library like sec-edgar-downloader in Python to download the 10-K filings
The fiscal year for a company is usually the year ending on the company's fiscal year end. We want the last three years
Extract the financial figures:
Once we have the 10-K filings (which are in HTML or XBRL format), we can parse them to extract the required data
We can use a library like beautifulsoup4 for HTML or xbrl for XBRL. However, note that 10-K filings are available in both formats, but XBRL (specifically, the financial statements in XBRL) is machine-readable and easier
Compile into a CSV:
We will create a CSV with columns: Company, Fiscal Year, Total Revenue, Net Income, Total Assets, Total Liabilities, Cash Flow from Operating Activities
However, note: The user wants a CSV file. We are an AI and cannot run code, but we can generate a sample CSV string
But without actual data, we can only show a sample structure
Alternatively, we can use a financial data provider's API (like Alpha Vantage, Yahoo Finance, etc.) to get the financials, but note the user specifically asked for 10-K filings
