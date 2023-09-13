# Import the required modules
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import datetime

# Define the cities and localities for scraping
cities = [
    "Pune",
    "Delhi",
    "Mumbai",
    "Lucknow",
    "Agra",
    "Ahmedabad",
    "Kolkata",
    "Jaipur",
    "Chennai",
    "Bengaluru",
]
localities = {
    "Pune": ["Baner", "Hinjewadi", "Kharadi", "Wakad", "Viman Nagar"],
    "Delhi": ["Dwarka", "Rohini", "Saket", "Lajpat Nagar", "Karol Bagh"],
    # Add the rest of the localities for each city
}

# Define the base URL for 99acres
base_url = "https://www.99acres.com/search/property/buy/"

# Define the MongoDB connection string and database name
mongo_url = "mongodb://localhost:27017/"
db_name = "property_data"

# Create a MongoDB client and a collection for storing the scraped data
client = MongoClient(mongo_url)
db = client[db_name]
collection = db["properties"]


# Define a function to scrape property data from a given city and locality
def scrape_property_data(city, locality):
    # Create a URL for the city and locality
    url = (
        base_url
        + city.lower()
        + "-"
        + locality.lower()
        + "?city="
        + str(cities.index(city) + 1)
        + "&preference=S&area_unit=1&res_com=R"
    )

    # Create a headless Chrome browser with Selenium
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    # Load the URL and wait for the page to load completely
    browser.get(url)
    browser.implicitly_wait(10)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Find all the property listings on the page
    listings = soup.find_all("div", class_="srpNw_tble")

    # Loop through each listing and extract the property details
    for listing in listings:
        # Initialize an empty dictionary to store the property data
        property_data = {}

        # Find the property name, cost, type, area, and link elements
        name_elem = listing.find("a", class_="body_med")
        cost_elem = listing.find("span", class_="srpNw_price")
        type_elem = listing.find("div", class_="srpDetail")
        area_elem = listing.find("td", class_="srpTuple__areaValue")
        link_elem = listing.find("a", class_="body_med srpTuple__propertyName")

        # Extract the text from each element and store it in the dictionary
        if name_elem:
            property_data["Property Name"] = name_elem.text.strip()
        if cost_elem:
            property_data["Property Cost"] = cost_elem.text.strip()
        if type_elem:
            property_data["Property Type"] = type_elem.text.strip().split("\n")[0]
        if area_elem:
            property_data["Property Area"] = area_elem.text.strip()

        # Store the city and locality in the dictionary
        property_data["propertyLocality"] = locality
        property_data["propertyCity"] = city

        # Extract the link from the element and store it in the dictionary
        if link_elem:
            property_data["Individual Property Link"] = link_elem["href"]

        # Insert the dictionary into the MongoDB collection
        collection.insert_one(property_data)

    # Close the browser
    browser.quit()


# Define a function to schedule the scraping script using Django-crontab
def schedule_scraping_script():
    # Import the django_crontab module
    from django_crontab import crontab

    # Define a list of cron jobs to run twice daily for each city and locality
    cron_jobs = []

    # Loop through each city and locality and create a cron job entry
    for city in cities:
        for locality in localities[city]:
            # Define the cron expression to run at 8 AM and 8 PM every day
            cron_expr = "0 8,20 * * *"

            # Define the command to call the scrape_property_data function with the city and locality arguments
            command = "scrape_property_data('{}', '{}')".format(city, locality)

            # Append a tuple of cron expression, command, and an optional name to the cron jobs list
            cron_jobs.append(
                (cron_expr, command, "scrape_{}_{}".format(city, locality))
            )

    # Add the cron jobs list to the CRONJOBS setting in the Django project
    CRONJOBS = cron_jobs


# Call the schedule_scraping_script function to start the scraping process
schedule_scraping_script()
