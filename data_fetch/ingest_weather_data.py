# Project 2 -  Data Ingestion Container  
# Fetch Weather data via API call

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo 
import json

print('Ingest Weather data')

def scrape_single_city_page(soup, city_list):
  """
  Function to Scrap a single page
  Scrape the city page content given by Soup object <soup>
  The found cities are stored in the list <city_list>
  """

  print('Scrap Single City page')

  # Get City table:
  city_tab = soup.find('table', class_='table table-hover table-bordered')

  for row in city_tab.find_all('tr'):
    cols = row.find_all('td')

    if cols:
      # Structure of City table:
      # [0] City number
      # [1] City name
      # [2] Country
      # [3] Latitude
      # [4] Longitude

      city_list.append(
            {
                'city_number': cols[0].text.strip(),
                'city_name': cols[1].text.strip(),
                'country': cols[2].text.strip(),
                'latitude': float(cols[3].text.strip()),
                'longitude': float(cols[4].text.strip())
            })

# Function: Get Next Page within City Main URL
def get_next_page(soup, main_url):
  """
  Function to get the next page for the URL <main_url>
  Return : The URL for the next page
  """
  print('Search for next page')

  next_page_url = None
  next_page_link = soup.find_all('a', class_='page-link')
  for link in next_page_link:
    if link.text == "Next":
      print('Next page:')
      print(link['href'])
      # Get next page for main URL
      if link['href'].startswith(main_url) :
        next_page_url = link['href']
  return next_page_url

# Function Scrape all pages for the City Main URL
def scrape_all_city_data(main_url):
  '''
  Scrap all city pages for the URL <main_url>

  Return: Dataframe <df> which contains the City data
  '''
  print('Scrap all City pages')
  html_req = requests.get(main_url)
  soup = BeautifulSoup(html_req.text, 'html.parser')

  # Main list objects which collects the City metadata
  city_list = []

  # Scrap the first page
  scrape_single_city_page(soup, city_list)

  # Check if a next page is available
  next_page_url = get_next_page(soup, main_url)

  # Traverse through the next pages to collect
  # the data for all cities
  while next_page_url is not None:

    # Take the next page, scrap it and (if available) search for the (overnext) page
    html_req = requests.get(next_page_url)
    soup = BeautifulSoup(html_req.text, 'html.parser')
    scrape_single_city_page(soup, city_list)
    next_page_url = get_next_page(soup, main_url)

  # Store the results in a DataFrame
  df = pd.DataFrame(city_list)

  return df

def get_weather_data(latitude, longitude, appid):
  weather_data = dict()


  # Define the URL
  # Uncomment this line and please use this carefully: the appid is limited to 1,000,000 calls/month and 60 calls/minute
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={str(latitude)}&lon={str(longitude)}&units=metric&appid={appid}"

  # Make the request and get the response object
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
    # Parse the JSON content from the response
    data = response.json()
    #print(data)
  else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
    return weather_data

  #weather_data['temperature'] = data['main']['temp']
  #weather_data['weather'] = data['weather'][0]['main']
  #weather_data['weather_description'] = data['weather'][0]['description']
  weather_data = data 

  return weather_data


# Main program
# Overall parameters - needed for API Call

# OpenWeather API:
#openweather_appid = 'e88b8a7f2403142335eb142bbbdceed5'  # Laszlos
openweather_appid = '19f9b7de91755a5dc972bc7e1e09f6b7'   # Juergen

# City URLs
# Germany
main_url="https://geokeo.com/database/city/de"
# Hungary
#main_url="https://geokeo.com/database/region/hu/"

print('Start main program')
print(f"Scrap {main_url}")

# Caution: geokeo.com is currently not available !

'''
html_req = requests.get(main_url)
soup = BeautifulSoup(html_req.text, 'html.parser')

# Scrape the City data for main URL
df = None
df = scrape_all_city_data(main_url)
'''

# Calculate the Weather Data for the Cities
# Function provides a Dictonary which is split in 3 separate columns in the target DataFrame:
# - temperature
# - weather
# - weather description
# Value for additional (3.) Call parameter (appid) is set beforehand in Main script

print('Get Weather data')
#df[['temperature', 'weather', 'weather_desc']] = df.apply(lambda row, appid=openweather_appid: get_weather_data(row['latitude'], row['longitude'], appid), axis=1, result_type='expand')


print('End main program')

'''print(df)

#import time
#time.sleep(1800)

'''
# Hard coded example, because geokeo is currently not available
weather_data = get_weather_data(52.517036, 13.388860, openweather_appid)

print(weather_data)


# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://mongodb:27017/")

# database 
db = client["data_db"]

collection = db["data_collection"]


if isinstance(weather_data, list):
     collection.insert_many(weather_data)  
else:
     collection.insert_one(weather_data)

print('Print MongoDB entry')
print('Number of documents in collection:', collection.count_documents({}))

for doc in collection.find():
    print(doc)    


'''
import datetime

client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client.testdb
collection = db.testcollection

# Add data with timestamp
current_time = datetime.datetime.now()
collection.insert_one({"message": "Hello from Python to MongoDB!", "timestamp": current_time})

# Read data
for doc in collection.find():
    print(doc)

'''