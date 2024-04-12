New Products Tracker G2
The New Products Tracker G2 is a tool designed to track and identify new products released on various platforms such as Product Hunt, BetaList, and G2. This README file provides an overview of the project, including its functionalities, usage instructions, and components.

Overview
The New Products Tracker G2 fetches data from different sources, including:

Product Hunt: Fetches newly featured products using the Product Hunt API.
BetaList: Scrapes data from BetaList to identify new product releases.
G2: Retrieves product information from G2 using its API.
The project aims to identify new products not yet listed on G2 by cross-referencing data obtained from Product Hunt and BetaList with existing G2 product listings.

Components


main.py : 
The main.py script serves as the main orchestrator of the project. It includes the following functionalities:

Fetching Data: Provides buttons to fetch data from Product Hunt, BetaList, and G2 individually.
Fetch New Products: Displays the latest new products identified by cross-referencing data from Product Hunt and BetaList with existing G2 product listings.
Force Run Today: Allows forcing a data fetch for today's products from all sources.
Countdown Timer: Displays a countdown timer until the next scheduled product update.


getG2.py : 
This script, getG2.py, is responsible for fetching data from G2 using its API. It includes the following functionalities:

API Request Handling: The script constructs and sends HTTP requests to the G2 API using the requests library, including necessary headers and authorization tokens.
Data Extraction: Upon receiving a response from the G2 API, the script parses the JSON data and extracts relevant product information, such as product names and descriptions.
Error Handling: It implements error handling to gracefully handle exceptions that may occur during API requests, JSON decoding, or data extraction. Detailed error messages are logged for debugging purposes.

fetchFromProductHunt.py : 
This script, fetchFromProductHunt.py, is responsible for fetching data from Product Hunt. It includes the following functionalities:

API Request Handling: Similar to getG2.py, this script constructs and sends HTTP requests to the Product Hunt API, including necessary headers and authorization tokens.
Data Extraction: Upon receiving a response from the Product Hunt API, the script parses the JSON data and extracts relevant product information, such as product names and descriptions.
Error Handling: Like getG2.py, it implements error handling to gracefully handle exceptions that may occur during API requests, JSON decoding, or data extraction. Detailed error messages are logged for debugging purposes.

betaList.py : 
This script, betaList.py, is responsible for fetching data from BetaList. It includes the following functionalities:

Web Scraping: Instead of using an API, this script utilizes web scraping techniques to extract product data from the BetaList website. It sends HTTP requests to specific URLs, parses the HTML content, and extracts relevant information.
Data Extraction: Similar to the other scripts, betaList.py extracts product names and descriptions from the scraped HTML content. It employs BeautifulSoup, a Python library for web scraping, to navigate and extract data from HTML documents.


streamlit_main.py : 
This script, streamlit_main.py, serves as the main application script utilizing the Streamlit library to create an interactive web application. It includes the following functionalities:
User Interface: streamlit_main.py defines the layout and components of the Streamlit web application, including buttons, data display widgets, and countdown timers.
Data Fetching Integration: It integrates the functionality of the other scripts (getG2.py, fetchFromProductHunt.py, betaList.py) by calling their respective functions to fetch data from G2, Product Hunt, and BetaList.
User Interaction: streamlit_main.py provides buttons and interactive elements for users to trigger data fetching, display fetched data, and force a data fetch for today's products.
Error Handling: The script implements error handling to catch exceptions that may occur during data fetching or processing. It logs detailed error messages and provides feedback to the user if an error occurs.

CSV : 
The CSV directory stores CSV files containing fetched data, including new product listings (NewProducts) and historical data from Product Hunt, BetaList, and G2.


To run the project : 
streamlit run Streamlit_main.py
