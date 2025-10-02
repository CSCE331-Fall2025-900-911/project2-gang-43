import pandas as pd
import random
import csv
from datetime import datetime, timedelta

# Read the items CSV
items_df = pd.read_csv('csv/item.csv')

# Generate Orders and Order_Items CSV
def generate_orders_and_items_csv(total_sales_target=750000, weeks=39):
    orders_data = []
    order_items_data = []
    cumulative_sales = 0
    start_date = datetime.now() - timedelta(weeks=weeks)
    order_id = 1
    
    while cumulative_sales < total_sales_target:
        # Generate order timestamp within 39 weeks
        order_timestamp = start_date + timedelta(
    days=random.randint(0, weeks*7),
    hours=random.randint(0, 23),
    minutes=random.randint(0, 59)
)
        
        # Generate a random target for this order (right-skewed 10-300)
        target_order_total = round(10 + (random.random() ** 9) * 290, 2)
        
        # Start each order at 0
        order_total = 0
        order_items = {}  # Track items for this order to avoid duplicates
        
        # Keep adding items until order_total > target_order_total
        while order_total <= target_order_total:
            # Randomly select an item from item table
            item = items_df.sample(1).iloc[0]
            # Random quantity (1-3)
            quantity = random.randint(1, 3)
            # Add item price to order_total
            item_price = item['Price']
            
            # If item already exists in this order, add to quantity
            if item['Item_ID'] in order_items:
                order_items[item['Item_ID']]['quantity'] += quantity
            else:
                order_items[item['Item_ID']] = {
                    'quantity': quantity,
                    'price': item_price
                }
            
            order_total += (item_price * quantity)
        
        # Add order items to data (no duplicates now)
        for item_id, details in order_items.items():
            order_items_data.append([
                order_id,
                item_id,
                details['quantity'],
                details['price']
            ])
        
        # Add completed order to orders_data
        orders_data.append([
            order_id,
            order_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            round(order_total, 2)
        ])
        
        # Add this order's total to cumulative sales
        cumulative_sales += order_total
        order_id += 1
        
    
    # Write Orders CSV
    with open('csv/orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Order_ID', 'Order_Timestamp', 'Order_Total'])
        writer.writerows(orders_data)
    
    # Write Order_Item CSV
    with open('csv/order_item.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Order_ID', 'Item_ID', 'Quantity', 'Item_Price'])
        writer.writerows(order_items_data)
    
    print(f"Total Sales: ${cumulative_sales:.2f}")
    print(f"Number of Orders: {len(orders_data)}")
    print(f"Number of Order Items: {len(order_items_data)}")
    
    return orders_data, order_items_data

# Generate the CSVs
orders, order_items = generate_orders_and_items_csv()

print("CSVs generated successfully!")