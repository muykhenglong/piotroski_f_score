# Piotroski F-Score Calculator

This Python script calculates the Piotroski F-Score for companies listed in the Dow Jones Industrial Average. The F-Score is a financial score used to assess the strength of a company's financial position based on 9 criteria involving profitability, leverage, liquidity, and operating efficiency.

## Features

- **Automated Data Extraction**: Leverages Selenium to fetch financial data from Yahoo Finance.
- **Financial Analysis**: Calculates the Piotroski F-Score based on recent financial data for each company.
- **Filtering and Ranking**: Removes financial stocks and ranks the remaining stocks based on their F-Score.

## Requirements

- Python 3.8.19

## How It Works

- Data Extraction: The script navigates to Yahoo Finance pages of each Dow component to extract relevant financial data for the current year and the two preceding years.
- Data Transformation: Extracted data is cleaned and transformed into numerical format suitable for analysis.
- F-Score Calculation: The script calculates the Piotroski F-Score for each non-financial stock based on the transformed data.
Output: The stocks are sorted by their F-Score, and the result is printed.

## Author

Muykheng Long - https://github.com/muykhenglong/
