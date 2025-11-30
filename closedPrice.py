import yfinance as yf
from datetime import datetime

def get_closed_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="max")

        if hist.empty:
            print("No historical data found for ticker: ", ticker_symbol)
            return None
        
        first_day = hist.iloc[0]

        date_string = first_day.name.strftime("%Y-%m-%d")
        date_format = ("%Y-%m-%d")
        datetime_object = datetime.strptime(date_string, date_format)
        
        return{
            "date": datetime_object,
            "open": first_day['Open'],
            "high": first_day['High'],
            "Low": first_day["Low"],
            "close": first_day['Close'],
            "volume": first_day["Volume"]
        }
    except Exception:
        print("error fetching data for ticker: ", ticker_symbol)
        return None
    

