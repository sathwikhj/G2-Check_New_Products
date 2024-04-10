import streamlit as st
import pandas as pd
from getG2 import get_G2_products, get_G2_products_display
from fetchFromProductHunt import fetch_producthunt_products
from betaList import products_released, for_display_betalist
from datetime import datetime
from datetime import datetime, timedelta
import time
import os
import logging

# Configure logging
logging.basicConfig(filename='Logs/main_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_producthunt():
    try:
        global df_producthunt
        products = fetch_producthunt_products()
        if products:
            df_producthunt = pd.DataFrame(products)
        else:
            df_producthunt = pd.DataFrame()
        return df_producthunt
    except Exception as e:
        logging.error("Error fetching data from Product Hunt: %s", str(e))


def fetch_g2():
    try:
        global g2_names
        g2_data = get_G2_products()
        g2_names = {product['name'] for product in g2_data}
        return g2_names
    except Exception as e:
        logging.error("Error fetching data from G2: %s", str(e))

def fetch_betalist():
    try:
        global beta_names
        products = products_released()
        if products:
            beta_names = pd.DataFrame(products)
        else:
            beta_names = pd.DataFrame()
    except Exception as e:
        logging.error("Error fetching data from BetaList: %s", str(e))

def on_countdown_end():
    try:
        fetch_betalist()
        fetch_producthunt()
        fetch_g2()
        new_combined_df = pd.concat([beta_names, df_producthunt], ignore_index=True)
        new_combined_df = new_combined_df.drop_duplicates(subset=['names'])
        new_combined_df = new_combined_df[~new_combined_df['Name'].isin(g2_names)]  
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'CSV/NewProducts/NewProducts_{date_str}.csv'
        new_combined_df.to_csv(filename, index=False)
    except Exception as e:
        logging.error("Error processing data at the end of countdown: %s", str(e))

def get_next_saturday():
    today = datetime.today()
    days_until_saturday = (5 - today.weekday()) % 7
    next_saturday = today + timedelta(days=days_until_saturday)
    return next_saturday.replace(hour=0, minute=0, second=0, microsecond=0)

def get_time_until_next_saturday():
    next_saturday = get_next_saturday()
    now = datetime.now()
    time_until_saturday = next_saturday - now
    return time_until_saturday

def format_time_delta(delta):
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{delta.days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def get_latest_csv_from_NewProducts():
    try:
        folder_path = "CSV/NewProducts"
        # Get list of all files in the folder
        files = os.listdir(folder_path)

        # Filter out directories from the list
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

        if not files:
            logging.warning("No CSV files found in the directory: %s", folder_path)
            return None  # Return None if no files found in the folder

        # Get the latest modified file based on modification time
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

        # Return the full path of the latest file
        return os.path.join(folder_path, latest_file)
    except Exception as e:
        logging.error("An error occurred while getting the latest CSV file: %s", str(e))
        return None


def main():
    try:
        st.title('New Products Tracker G2')
        if st.button('Fetch Data From Product Hunt'):
            st.write('Fetching data...')
            df_producthunt = fetch_producthunt()
            st.write('Data fetched successfully!')
            st.write(df_producthunt)
        
        if st.button('Fetch Data From BetaList'):
            st.write('Fetching data...')
            beta_names = for_display_betalist()
            st.write('Data fetched successfully!')
            st.write(beta_names)
        
        if st.button('Fetch Data From G2'):
            st.write('Fetching data...')
            g2_names = get_G2_products_display()
            st.write('Data fetched successfully!')
            st.write(g2_names)

        if st.button('Compare Data and make a csv file'):
            df_newprods=pd.read_csv(get_latest_csv_from_NewProducts())
            st.write(df_newprods)
        
        st.subheader("Countdown Timer Until Next Product Update")

        countdown_placeholder = st.empty()
        
        while True:
            time_until_saturday = get_time_until_next_saturday()
            if time_until_saturday.days < 0:
                st.error("Error: Could not calculate time until next Saturday.")
                break
            else:
                countdown_placeholder.write(f"Time Left: {format_time_delta(time_until_saturday)}")
                
            if datetime.now().weekday() == 5:  # Saturday
                on_countdown_end()
                break
                
            time.sleep(1)  
    except Exception as e:
        logging.error("An error occurred in the main function: %s", str(e))

if __name__ == '__main__':
    main()