from closedPrice import get_closed_price
from getOfferPrice import fetch_data
import pandas as pd

# 1. Fetch Raw Data
ipo_list = fetch_data()

if ipo_list:
    df = pd.DataFrame(ipo_list)
    clean_df = df[['proposedTickerSymbol', 'pricedDate', 'companyName', 'sharesOffered', 'proposedSharePrice']]
else:
    print("No data available.")
    exit()

results = []

print(f"Found {len(clean_df)} IPOs. Processing...")

for index, row in clean_df.iterrows():
    ticker = row['proposedTickerSymbol']
    raw_price = row['proposedSharePrice']
    
    # 1. Skip rows where price is None 
    if raw_price is None or str(raw_price).lower() == 'none':
        print(f"Skipping {ticker}: Price is missing.")
        continue

    # 2. Clean Data Types
    try:
        # Remove commas from shares (e.g., "15,000,000" -> 15000000)
        shares_str = str(row['sharesOffered']).replace(',', '').replace('$', '')
        shares_offered = int(float(shares_str)) # float conversion first handles "1000.0" strings
        
        # Clean price (just in case)
        offer_price = float(str(raw_price).replace('$', '').strip())
    except ValueError as e:
        print(f"Skipping {ticker}: Data format error ({e})")
        continue

    # 3. Get Market Data
    market_data = get_closed_price(ticker)

    if market_data:
        try:
            first_day_close = market_data['close']
            
            results.append({
                "ticker": ticker,
                "offer_price": offer_price, 
                "close_price": first_day_close,
                "ipo_date": row['pricedDate'],
                "shares_offered": shares_offered
            })
            print(f"Processed {ticker}: Offer ${offer_price} -> Close ${first_day_close}")

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    else:
        print(f"No market data available for ticker: {ticker}")

# 4. Save to CSV for Analysis
results_df = pd.DataFrame(results)
results_df.to_csv('ipo_data_clean.csv', index=False)
print(f"\nSuccess. {len(results_df)} clean records saved to 'ipo_data_clean.csv'.")