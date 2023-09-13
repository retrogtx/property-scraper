# Import the required modules
import requests
from bs4 import BeautifulSoup
import pymongo
from django.core.management.base import BaseCommand
from django_cron import CronJobBase, Schedule

# Define the MongoDB database and collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["property_db"]
collection = db["property_data"]

# Define the base URL for 99acres website
base_url = "https://www.99acres.com"

# Define the property details to store
property_name = "Kalyans Skyway 9"
property_cost = "85.48 - 91.98 Lac"
property_type = "2BHK Flat"
property_area = "1315 - 1415 sqft"
property_locality = "Banjara Hills"
property_city = "Hyderabad"
property_link = "https://www.99acres.com/2-bhk-bedroom-apartment-flat-for-sale-in-kalyans-skyway-9-narsingi-hyderabad-1315-sq-ft-to-1415-sq-ft-npspid-P69187662"

# Create a dictionary with the property details
property_data = {
    "name": property_name,
    "cost": property_cost,
    "type": property_type,
    "area": property_area,
    "locality": property_locality,
    "city": property_city,
    "link": property_link,
}

# Insert the property data into the MongoDB collection
collection.insert_one(property_data)

# Define the cities and localities to scrape
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
    "Pune": ["Kharadi", "Hinjewadi", "Wakad"],
    "Delhi": ["Dwarka", "Rohini", "Saket"],
    "Mumbai": ["Andheri East", "Bandra West", "Kurla West"],
    "Lucknow": ["Gomti Nagar", "Indira Nagar", "Aliganj"],
    "Agra": ["Tajganj", "Dayal Bagh", "Kamla Nagar"],
    "Ahmedabad": ["Satellite", "Bopal", "Thaltej"],
    "Kolkata": ["Salt Lake City", "New Town", "Ballygunge"],
    "Jaipur": ["Malviya Nagar", "Vaishali Nagar", "Mansarovar"],
    "Chennai": ["Adyar", "Anna Nagar", "Velachery"],
    "Bengaluru": ["Indira Nagar", "Koramangala", "Whitefield"],
}


# Define a function to scrape property details from a given URL
def scrape_property(url):
    # Make a GET request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the property name, cost, type, area, and link elements
    name = soup.find("h1", class_="p_title")
    cost = soup.find("span", class_="pd_price")
    type_ = soup.find("span", class_="pd_prop_type")
    area = soup.find("span", class_="pd_area")
    link = soup.find("link", rel="canonical")

    # Extract the text from the elements and return a dictionary
    return {
        "name": name.text.strip() if name else None,
        "cost": cost.text.strip() if cost else None,
        "type": type_.text.strip() if type_ else None,
        "area": area.text.strip() if area else None,
        "link": link["href"] if link else None,
    }


# Define a function to scrape property listings from a given city and locality
def scrape_listings(city, locality):
    # Construct the URL for the city and locality page
    url = f"{base_url}/property-for-sale-in-{locality.replace(' ', '-')}-{city.replace(' ', '-')}-ffid"

    # Make a GET request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the property listing elements
    listings = soup.find_all("div", class_="srpNw_tble")

    # Loop through each listing and scrape the property details
    for listing in listings:
        # Find the property link element and get the href attribute
        link = listing.find("a", class_="body_med")
        href = link["href"] if link else None

        # If the href is not None, append the base URL and scrape the property details
        if href:
            property_url = base_url + href
            property_data = scrape_property(property_url)

            # Insert the property data into the MongoDB collection
            collection.insert_one(property_data)


# Define a custom Django command to run the scraping script
class Command(BaseCommand):
    help = "Scrape property data from 99acres website"

    def handle(self, *args, **options):
        # Loop through each city and locality and scrape the listings
        for city in cities:
            for locality in localities[city]:
                scrape_listings(city, locality)


# Define a custom Django cron job to schedule the scraping script twice daily
class ScrapePropertyCronJob(CronJobBase):
    RUN_EVERY_MINS = 720  # 12 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "property.scrape_property_cron_job"  # a unique code

    def do(self):
        # Run the scraping command
        Command().handle()
