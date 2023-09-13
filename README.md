# mobilics-project

Here is the bullet points for Github readme file in new line indentation:

- Project initially coded up to apply for an intern role at Mobilicis India Private Limited as a Python dev.
- Process through which I got through this program:
  - Set this up in a virtual environment
  - Import the required modules, packages
  - Made using Django, Selenium, Cron and MongoDB
  - Set up a scheduled cron job using Django-crontab or a similar tool
  - Defined the base URL (99acres in our case), Cities and Localities which can be changed according to user's custom needs.
  - Defined a custom Django cron job to schedule the scraping script twice daily
- Comments added for more understandibility
- Code uploaded as required by the recruiters, but also for people in the forseeable future who want to learn/understand a basic scrapping program
- Summary: This project is a Django web application that scrapes property data from 99acres website and stores it in a MongoDB database. The application also schedules and manages the scraping script using Django cron jobs. The application allows the user to view the scraped data on a web page in a tabular format. The application uses requests, BeautifulSoup, and pymongo modules to perform the scraping and database operations. The application also uses a custom Django command and a custom Django cron job to run and schedule the scraping script. The application is intended to demonstrate how to use Django to create a web-based property data scraper and scheduler 😊
