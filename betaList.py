import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime, timedelta
import os
import re
import logging

# Configure logging
logging.basicConfig(filename='Logs/Betalist_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_betalist_topics():
    try:
        base_url = 'https://betalist.com'
        data = []

        # Send a GET request to the URL
        response = requests.get('https://betalist.com/topics')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all div tags with the specified class
            divs = soup.find_all('div', class_='mt-2 grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5 gap-x-4')

            # Access the second div
            if len(divs) > 1:
                second_div = divs[1]

                # Find all 'a' tags inside the second div
                a_tags = second_div.find_all('a', class_='flex items-center gap-1 px-2 hover:bg-gray-100 group gap-4 hover:-my-[1px]')

                # Iterate over the 'a' tags
                for a in a_tags:
                    # Get the URL from the 'href' attribute of the 'a' tag and handle relative URLs
                    link = urljoin(base_url, a['href'])

                    # Send a request to the URL to extract its content
                    page_response = requests.get(link)

                    # Check if the request was successful (status code 200)
                    if page_response.status_code == 200:
                        # Parse the HTML content of the page
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')

                        # Extract text from 'a' tags with class 'block whitespace-nowrap text-ellipsis overflow-hidden font-medium'
                        a_content = page_soup.find_all('a', class_='block whitespace-nowrap text-ellipsis overflow-hidden font-medium')
                        for a2 in a_content:
                            # Extract text from 'a' tags with class 'block text-gray-500 dark:text-gray-400'
                            a2_content = page_soup.find_all('a', class_='block text-gray-500 dark:text-gray-400')

                            # Extract the text from the 'a' tag
                            name = a2.text.strip()
                            description = a2_content[0].text.strip()
                            
                            # Extract the category from the URL
                            category = link.split('/')[-1]

                            # Append the data to the list
                            data.append({'Name': name, 'Description': description})

                    else:
                        logging.error(f"Failed to retrieve page: {link}. Status code: {page_response.status_code}")

            else:
                logging.error('Second div not found.')

        else:
            logging.error(f'Failed to retrieve the webpage. Status code: {response.status_code}')

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'CSV/BetaList/BetaListProducts_{date_str}.csv'
        df.to_csv(filename, index=False)
        return df
    except Exception as e:
        logging.error(f"An error occurred while scraping Betalist topics: {str(e)}")
        return None

def load_csv_to_dataframe():
    try:
        # Get the file name for the previous week
        filename = get_latest_csv_from_betalist()

        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        # If the file is not found, return None
        logging.warning(f"CSV file '{filename}' not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading CSV to DataFrame: {str(e)}")
        return None
    
def products_released():
    try:
        # Load data from the Excel file into a DataFrame (assuming the file is named 'BetaListProducts.xlsx')
        df_old = load_csv_to_dataframe()

        # Scrape the latest data from Betalist and store it in another DataFrame
        df_new = scrape_betalist_topics()  # Assuming this function returns the latest data as a DataFrame
        # Compare the two DataFrames based on product names

        df_new = df_new[~df_new['Name'].isin(df_old['Name'])]

        # Return the new products as a list
        return df_new
    except Exception as e:
        logging.error(f"An error occurred while getting released products: {str(e)}")
        return []

def for_display_betalist():
    try:
        directory = 'CSV/BetaList'
        files = os.listdir(directory)
        prefix='BetaListProducts_'
        csv_files = [file for file in files if file.endswith('.csv') and file.startswith(prefix)]
        dates = [re.search(r'(\d{4}-\d{2}-\d{2})', file).group(1) for file in csv_files]
        sorted_dates = sorted(dates, reverse=True)
        latest_files = [file for file in csv_files if re.search(sorted_dates[0], file)]
        second_latest_files = [file for file in csv_files if re.search(sorted_dates[1], file)]
        latest_df = pd.read_csv(os.path.join(directory, latest_files[0]))
        second_latest_df = pd.read_csv(os.path.join(directory, second_latest_files[0]))
        new_products = latest_df[~latest_df['Name'].isin(second_latest_df['Name'])]
        return new_products
    except Exception as e:
        logging.error(f"An error occurred while displaying Betalist data: {str(e)}")
        return None
    
def get_latest_csv_from_betalist():
    try:
        folder_path = "CSV/BetaList"
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
    
# print(get_latest_csv_from_betalist())

