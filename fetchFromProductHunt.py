import requests
import json
import csv
from datetime import datetime, timedelta

def fetch_producthunt_products():
    # Get today's date and the date from a week ago
    today_date = datetime.now()
    week_ago = today_date - timedelta(days=7)
    
    # Format the dates as strings in the required format
    week_ago_str = week_ago.strftime('%Y-%m-%d')
    today_str = today_date.strftime('%Y-%m-%d')
    
    # Define the URL and headers for the API request
    url = 'https://api.producthunt.com/v2/api/graphql'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer FTLWQq7bru06ZCywZ4k-sQm9UJoIQErS9wFRBLmFgtg',
        'User-Agent': 'YOUR_APP_NAME_HERE'
    }
    
    # Define the GraphQL query with the correct date range
    query = f'''
    {{
        posts(first: 50, featured: true, postedBefore: "{today_str}T00:00:00.000Z", postedAfter: "{week_ago_str}T00:00:00.000Z") {{
            edges {{
                node {{
                    name
                    tagline
                }}
            }}
        }}
    }}'''
    
    # Send the POST request to the Product Hunt API
    response = requests.post(url, headers=headers, json={'query': query})
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        products = []
        
        # Extract product information from the response
        for edge in data['data']['posts']['edges']:
            product = {
                'Name': edge['node']['name'],
                'Description': edge['node']['tagline']
            }
            products.append(product)
        
        return products
    else:
        print('Error:', response.status_code, response.text)

