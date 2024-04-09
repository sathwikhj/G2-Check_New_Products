import streamlit as st
import pandas as pd
from getG2 import get_G2_products
from fetchFromProductHunt import fetch_producthunt_products
from betaList import products_released,  get_previous_week_filename
from datetime import datetime
import os

# Function to fetch Product Hunt products
def fetch_producthunt():
    return pd.DataFrame(fetch_producthunt_products())

# Function to fetch G2 products
def fetch_g2():
    g2_data = get_G2_products()
    return {product['name'] for product in g2_data}

# Function to fetch Beta List products
def fetch_betalist():
    return pd.DataFrame(products_released())

def main():
    st.title('New Products Tracker')
    if st.button('Fetch Data From Product Hunt'):
        st.write('Fetching data...')
        df_producthunt = fetch_producthunt()
        st.write('Data fetched successfully!')
        st.write(df_producthunt)
    
    if st.button('Fetch Data From BetaList'):
        st.write('Fetching data...')
        beta_names = fetch_betalist()
        st.write('Data fetched successfully!')
        st.write(beta_names)
    
    if st.button('Fetch Data From G2'):
        st.write('Fetching data...')
        g2_names = fetch_g2()
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

if __name__ == '__main__':
    main()