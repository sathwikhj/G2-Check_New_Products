import subprocess
import json
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='Logs/g2_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_G2_products():
    curl_command = 'curl -g -X GET -H "Authorization: Token token=40239d3e48892b4dc5a8754dc3a89fb0963bdb38819dd9a31496f216d99c7dc5" -H "Content-Type: application/vnd.api+json" https://data.g2.com/api/v1/products'
    try:
        curl_output = subprocess.check_output(curl_command, shell=True)
    except subprocess.CalledProcessError as e:
        logging.error("Error executing curl command: %s", e)
        return None
    try:
        response_data = json.loads(curl_output)
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON response: %s", e)
        return None

    # Extract product information
    products = []
    for product in response_data.get('data', []):
        product_info = {
            'name': product['attributes'].get('short_name', 'N/A'),
        }
        products.append(product_info)
    return products

def get_G2_products_display():
    curl_command = 'curl -g -X GET -H "Authorization: Token token=40239d3e48892b4dc5a8754dc3a89fb0963bdb38819dd9a31496f216d99c7dc5" -H "Content-Type: application/vnd.api+json" https://data.g2.com/api/v1/products'
    try:
        curl_output = subprocess.check_output(curl_command, shell=True)
    except subprocess.CalledProcessError as e:
        logging.error("Error executing curl command: %s", e)
        return None
    try:
        response_data = json.loads(curl_output)
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON response: %s", e)
        return None

    # Extract product information
    products = []
    for product in response_data.get('data', []):
        product_info = {
            'name': product['attributes'].get('short_name', 'N/A'),
            'description': product['attributes'].get('description', 'N/A'),
        }
        products.append(product_info)
    df = pd.DataFrame(products)
    return df
