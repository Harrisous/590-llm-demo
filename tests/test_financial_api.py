import requests
import os
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")

try:
    # GET request
    ticker = "AAPL"
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={FMP_API_KEY}"
    response = requests.get(url)
    
    # check
    if response.status_code == 200:
        data = response.json()
        print("Response Data:")
        print(data)
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print("An error occurred:", str(e))