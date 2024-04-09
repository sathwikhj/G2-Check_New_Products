import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime, timedelta

def scrape_betalist_topics():
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
                    print(f"Failed to retrieve page: {link}. Status code:", page_response.status_code)

        else:
            print('Second div not found.')

    else:
        print('Failed to retrieve the webpage. Status code:', response.status_code)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'CSV/BetaList/BetaListProducts_{date_str}.csv'
    df.to_csv(filename, index=False)
    return df


def get_previous_week_filename():
    # Get today's date
    today = datetime.now()

    # Calculate the date a week ago
    week_ago = today - timedelta(days=7)

    # Format the dates as strings in the required format
    today_str = today.strftime('%Y-%m-%d')
    week_ago_str = week_ago.strftime('%Y-%m-%d')

    # Generate the file name
    filename = f'BetaListProducts_{week_ago_str}.csv'
    return filename

def load_csv_to_dataframe():
    # Get the file name for the previous week
    filename = 'CSV/BetaList/'+get_previous_week_filename()

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        # If the file is not found, return None
        print(f"CSV file '{filename}' not found.")
        return None
    
def products_released():
    # Load data from the Excel file into a DataFrame (assuming the file is named 'BetaListProducts.xlsx')
    try:
        # Read the Excel file into a DataFrame
        df_old = load_csv_to_dataframe()
    except FileNotFoundError:
        # If the file is not found, return an empty list
        print("Excel file not found.")
        return []

    # Scrape the latest data from Betalist and store it in another DataFrame
    df_new = scrape_betalist_topics()  # Assuming this function returns the latest data as a DataFrame
    # df_new=pd.read_csv('Complete1/CSV/BetaList/BetaListProducts_2024-04-07.csv')
    # Compare the two DataFrames based on product names

    df_new = df_new[~df_new['Name'].isin(df_old['Name'])]

    # Return the new products as a list
    return df_new