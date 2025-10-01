import pandas as pd

# Read the CSV
df = pd.read_csv('/Users/anujaed/Downloads/order_item1.csv')

# Group by Order_ID and Item_ID, sum quantities
df_cleaned = df.groupby(['Order_ID', 'Item_ID'])['Quantity'].sum().reset_index()

# Add Item_Price (take the first price for each unique combination)
df_cleaned['Item_Price'] = df.groupby(['Order_ID', 'Item_ID'])['Item_Price'].first().reset_index(level=[0,1])['Item_Price']

# Save the cleaned CSV
df_cleaned.to_csv('/Users/anujaed/Downloads/order_item_cleaned.csv', index=False)

print(f"Original rows: {len(df)}")
print(f"Cleaned rows: {len(df_cleaned)}")