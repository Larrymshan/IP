import pandas as pd

#Read csv file
try:
    df = pd.read_csv('ipo_data_clean.csv')
except FileNotFoundError:
    print("CSV file not found.")
    exit()

if df.empty:
    print("Dataset empty")
    exit()

# Define underpricing as (close-open)/open
df['underpricing']=(df['close_price']-df['offer_price'])/df['offer_price']

# Define money left as (close-open)/total shares offered
df['money_left']=(df['close_price']-df['offer_price'])*df['shares_offered']

# Get variables for analysis
ave_underpricing = df['underpricing'].mean()
median_underpricing = df['underpricing'].median()
std_underpricing = df['underpricing'].std()
tot_money_left = df['money_left'].sum()

# Print results

print(f"Total IPOS Analyzed: {len(df)}")
print(f"Average First Day Return: {ave_underpricing:.2%}")
print(f"Median First Day Return: {median_underpricing:.2%}")
print(f"Volatility (StdDev): {std_underpricing:.4f}")
print(f"Total Money Left on Table: {tot_money_left:.2f}")

print("-----Top 5 Best Performing IPOS-----")
print(df[['ticker', 'offer_price', 'close_price', 'underpricing']].sort_values(by='underpricing', ascending=False).head(5))

print("-----Top 5 Money Left on Table-----")
print(df[['ticker', 'offer_price', 'close_price', 'money_left']].sort_values(by='money_left', ascending=False).head(5))