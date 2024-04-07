import subprocess
import json
import pandas as pd

def get_G2_products():
    curl_command='curl -g -X GET -H "Authorization: Token token=40239d3e48892b4dc5a8754dc3a89fb0963bdb38819dd9a31496f216d99c7dc5" -H "Content-Type: application/vnd.api+json" https://data.g2.com/api/v1/products'
    try:
        curl_output = subprocess.check_output(curl_command, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error executing curl command:", e)
        return None
    try:
        response_data = json.loads(curl_output)
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        return None

    # Extract product information
    products = []
    for product in response_data['data']:
        product_info = {
            'name': product['attributes']['short_name'],
        }
        products.append(product_info)
    return products
