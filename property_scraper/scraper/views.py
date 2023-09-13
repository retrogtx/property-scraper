from django.shortcuts import render

# Create your views here.


def scrape_view(request):
    # Connect to MongoDB database and collection
    client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

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

    # Loop through each city and locality and scrape the listings
    for city in cities:
        for locality in localities[city]:
            scrape_listings(city, locality)

    # Get all the scraped data from the database
    data = list(collection.find())

    # Render a template with the scraped data
    return render(request, "scraper/scrape.html", {"data": data})
