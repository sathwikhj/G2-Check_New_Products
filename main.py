import streamlit as st
import pandas as pd
from getG2 import get_G2_products, get_G2_products_display
from fetchFromProductHunt import fetch_producthunt_products
from betaList import products_released,  get_previous_week_filename, for_display_betalist
from datetime import datetime
from datetime import datetime, timedelta
import time

def fetch_producthunt():
    global df_producthunt
    df_producthunt = pd.DataFrame(fetch_producthunt_products())
    return df_producthunt

def fetch_g2():
    global g2_names
    g2_data = get_G2_products()
    g2_names = {product['name'] for product in g2_data}
    return g2_names

def fetch_betalist():
    global beta_names
    beta_names = pd.DataFrame(products_released())

def on_countdown_end():
    fetch_betalist()
    fetch_producthunt()
    fetch_g2()
    new_combined_df = pd.concat([beta_names, df_producthunt], ignore_index=True)
    new_combined_df = new_combined_df.drop_duplicates(subset=['names'])
    new_combined_df = new_combined_df[~new_combined_df['Name'].isin(g2_names)]  
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'CSV/NewProducts/NewProducts_{date_str}.csv'
    new_combined_df.to_csv(filename, index=False)

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

def main():
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
        beta_filename_latest = 'CSV/BetaList/'+get_previous_week_filename()
        beta_names = pd.read_csv(beta_filename_latest)
        df_producthunt = pd.DataFrame(fetch_producthunt())
        g2_names =  pd.DataFrame(fetch_g2())
        combined_df = pd.concat([beta_names, df_producthunt], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['Name'])
        combined_df = combined_df[~combined_df['Name'].isin(g2_names)]
        st.write(combined_df)
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'CSV/NewProducts/NewProducts_{date_str}.csv'
        combined_df.to_csv(filename, index=False)
        st.success(f'Filtered data saved to {filename}')
    
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

if __name__ == '__main__':
    main()