import yfinance as yf
import pandas as pd

# S&P 500 Ticker
sp_ticker = yf.Ticker('^GSPC')

# S&P 500 Data
sp_data = sp_ticker.history(period="1y")

# Get info from csv
try:   
    df = pd.read_csv("ipo_data_clean.csv")
except FileNotFoundError:
    print("File not found")
    exit()

# file empty?
if df.empty:
    print("File empty")
    exit()

# underpricing ratio
df['underpricing'] = (df['close_price']-df['offer_price'])/df['offer_price']
df['abnorm_returns'] = 0.0

for index, row in df.iterrows():
    # 1. Date Conversion
    ipo_date = pd.to_datetime(row['ipo_date']).date() # Use .date() to strip time
    
    # 2. Match Date (Remove the minus 1 day logic)
    sp_data_for_date = sp_data[sp_data.index.date == ipo_date]
    
    # Check if we actually found market data for that day (avoids crash on weekends)
    if not sp_data_for_date.empty:
        
        # 3. Calculate Market Return (Close - Open) / Open
        market_open = sp_data_for_date['Open'].values[0]
        market_close = sp_data_for_date['Close'].values[0]
        norm_returns = (market_close - market_open) / market_open

        # 4. Calculate Abnormal Return
        abnorm_returns = row['underpricing'] - norm_returns

        # 5. WRITE TO DATAFRAME (The most important fix)
        df.loc[index, 'abnorm_returns'] = abnorm_returns
    else:
        # Handle cases where IPO was on a weekend/holiday
        df.loc[index, 'abnorm_returns'] = None

print("-----Top 5 Strongest Abnormal Returns-----")
print(df[['ticker', 'offer_price', 'close_price', 'underpricing', 'abnorm_returns']].sort_values(by = 'abnorm_returns', ascending=False).head(5))