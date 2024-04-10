import requests
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(filename='Logs/producthunt_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_producthunt_products():
    # Define the URL and headers for the API request
    url = 'https://api.producthunt.com/v2/api/graphql'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer FTLWQq7bru06ZCywZ4k-sQm9UJoIQErS9wFRBLmFgtg',
        'User-Agent': 'YOUR_APP_NAME_HERE'
    }
    
    # List to store all product releases
    all_products = []
    
    # Get today's date
    today_date = datetime.now().date()
    
    # Iterate over the past week
    for i in range(7):
        # Calculate the date for each day of the past week
        query_date = today_date - timedelta(days=i)
        
        # Format the date as required for the query
        query_date_str = query_date.strftime('%Y-%m-%d')
        
        # Define the GraphQL query with the correct date
        query = f'''
        {{
            posts(first: 50, featured: true, postedBefore: "{query_date_str}T23:59:59.999Z", postedAfter: "{query_date_str}T00:00:00.000Z") {{
                edges {{
                    node {{
                        name
                        tagline
                    }}
                }}
            }}
        }}'''
        
        try:
            # Send the POST request to the Product Hunt API
            response = requests.post(url, headers=headers, json={'query': query})
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the JSON response
            data = response.json()
            
            # Extract product information from the response
            for edge in data['data']['posts']['edges']:
                product = {
                    'Name': edge['node']['name'],
                    'Description': edge['node']['tagline'],
                    'Date': query_date_str
                }
                all_products.append(product)
                
        except requests.RequestException as e:
            logging.error(f"Error fetching data for {query_date_str}: {str(e)}")
        except Exception as ex:
            logging.exception(f"An error occurred while processing data for {query_date_str}: {str(ex)}")
    
    return all_products
