# this file will download the data from api and store the json files in \data
import requests
import os
import json
from dotenv import load_dotenv

# load api to fetch financial data
load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")

# set tickers list for extraction
tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOG", "GOOGL", "META", "BRK.B", "BRK.A",
    "TSLA", "AVGO", "LLY", "TSM", "WMT", "JPM", "V", "MA", "XOM", "COST",
    "ORCL", "UNH", "NFLX", "PG", "JNJ", "NVO", "HD", "ABBV", "BAC", "SAP",
    "TMUS", "KO", "BABA", "ASML", "CRM", "CVX", "WFC", "CSCO", "PM",
    "TM", "ABT", "AZN", "MRK", "IBM", "LIN", "NVS", "GE", "MCD",
    "ACN", "PEP", "HSBC", "MS", "AXP", "DIS", "SHEL", "ISRG",
    "PLTR", "T", "GS", "TMO", "BX", "ADBE", "NOW", "VZ",
    "TXN", "RTX", "QCOM", "INTU", "RY", "PGR", "AMGN",
    "SPGI", "BKNG", "AMD", "CAT", "PDD", "UBER", "BSX", "MUFG", 
    "SYK", "BLK", "HDB", "SONY", "UNP", "PFE",
    "DHR", "NEE", "SCHW", "C", "GILD", "UL", "TJX", "SHOP", "HON",
    "LOW", "SNY", "CMCSA", "TTE", "FI", "SBUX", "ADP", "ARM",
    "BA", "DE", "BHP", "VRTX", "AMAT", "SPOT", "PANW",
    "BMY", "MDT", "KKR", "BUD", "COP", "MMC", "PLD", "NKE", "CB", "APP",
    "ADI", "ETN", "UBS",
    "ANET", "LMT", "MELI", "TD", "RIO", "UPS", "MU"
]


try:
    # GET request
    for ticker in tickers:

        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={FMP_API_KEY}"
        response = requests.get(url)
    
        # check if there is return
        if response.status_code == 200:
            data = response.json()
            with open(os.path.join("data",f"{ticker}.json"), "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Response saved: {ticker}")
            
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)

except Exception as e:
    print("An error occurred:", str(e))