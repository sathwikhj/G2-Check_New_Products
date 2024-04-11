from main import fetch_producthunt, get_latest_csv_from_NewProducts, force_fetch, get_time_until_next_saturday, format_time_delta
from betaList import for_display_betalist
from getG2 import get_G2_products_display
from datetime import datetime
from datetime import datetime
import time
import streamlit as st
import logging
import pandas as pd
logging.basicConfig(filename='Logs/main_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        st.title('New Products Tracker G2')
        st.subheader('Fetch Data:')
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

        st.subheader('Fetch New Products:')
        if st.button('Fetch New Products'):
            df_newprods=pd.read_csv(get_latest_csv_from_NewProducts())
            st.write(df_newprods)
        
        st.subheader('Force Run Today:')
        if st.button('Force Run Today'):
            force_fetch()

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
                force_fetch()
                
            time.sleep(1)  
    except Exception as e:
        logging.error("An error occurred in the main function: %s", str(e))

if __name__ == '__main__':
    main()