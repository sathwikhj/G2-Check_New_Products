import threading
import pandas as pd
from getG2 import get_G2_products
from fetchFromProductHunt import fetch_producthunt_products
from betaList import products_released
from datetime import datetime
# Function to fetch Product Hunt products
def fetch_producthunt():
    global df_producthunt
    df_producthunt = pd.DataFrame(fetch_producthunt_products())

# Function to fetch G2 products
def fetch_g2():
    global g2_names
    g2_data = get_G2_products()
    g2_names = {product['name'] for product in g2_data}

# Function to fetch Beta List products
def fetch_betalist():
    global beta_names
    beta_names=pd.DataFrame(products_released())


thread_producthunt = threading.Thread(target=fetch_producthunt)
thread_g2 = threading.Thread(target=fetch_g2)
thread_betalist = threading.Thread(target=fetch_betalist)

thread_producthunt.start()
thread_g2.start()
thread_betalist.start()

thread_producthunt.join()
thread_g2.join()
thread_betalist.join()



combined_df = pd.concat([beta_names, df_producthunt], ignore_index=True)
combined_df = combined_df[~combined_df['Name'].isin(g2_names)]
print(combined_df)
# Save the filtered DataFrame to a CSV file
date_str = datetime.now().strftime('%Y-%m-%d')
filename = f'Complete1/CSV/NewProducts/NewProducts_{date_str}.csv'
combined_df.to_csv(filename, index=False)
