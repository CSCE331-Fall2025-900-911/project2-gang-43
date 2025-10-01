import pandas as pd
import random
import csv
from datetime import datetime, timedelta

# Read the items CSV
items_df = pd.read_csv('csv/item.csv')

# Generate Orders CSV
def generate_orders_csv(total_sales_target=750000, weeks=39):
    orders_data = []
    current_sales = 0
    start_date = datetime.now() - timedelta(weeks=weeks)
    order_id = 1

    while current_sales < total_sales_target:
        # Ensure order is within 39 weeks
        order_timestamp = start_date + timedelta(days=random.randint(0, weeks*7))
        
        # Generate order with higher total to reach sales target
        order_total = round(random.uniform(50.00, 300.00), 2)
        order_status = random.choice(['pending', 'completed'])
        
        orders_data.append([
            order_id, 
            order_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
            order_total, 
            order_status
        ])
        
        current_sales += order_total
        order_id += 1

        # Break if we've exceeded 39 weeks
        if order_timestamp > start_date + timedelta(weeks=39):
            break
    
    # Write to CSV
    with open('csv/orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Order_ID', 'Order_Timestamp', 'Order_Total', 'Order_Status'])
        writer.writerows(orders_data)
    
    print(f"Total Sales: ${current_sales:.2f}")
    print(f"Number of Orders: {len(orders_data)}")
    
    return orders_data

# Generate Order_Item CSV
def generate_order_items_csv(orders_data, items_df):
    order_items_data = []
    order_item_id = 1
    
    for order in orders_data:
        order_id, _, order_total, _ = order
        remaining_total = order_total
        
        while remaining_total > 0:
            # Randomly select an item
            item = items_df.sample(1).iloc[0]
            
            # Determine quantity
            max_quantity = min(3, int(remaining_total / item['Price']) + 1)
            quantity = random.randint(1, max_quantity)
            item_total = round(item['Price'] * quantity, 2)
            
            order_items_data.append([
                order_item_id,
                order_id, 
                item['Item_ID'], 
                quantity, 
                item['Price']
            ])
            
            remaining_total = round(remaining_total - item_total, 2)
            order_item_id += 1
            
            # Prevent infinite loop
            if remaining_total < 1:
                break
    
    # Write to CSV
    with open('/Users/anujaed/Downloads/order_item.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Order_Item_ID', 'Order_ID', 'Item_ID', 'Quantity', 'Item_Price'])
        writer.writerows(order_items_data)
    
    return order_items_data

# Generate the CSVs
orders = generate_orders_csv()
generate_order_items_csv(orders, items_df)

print("CSVs generated successfully!")