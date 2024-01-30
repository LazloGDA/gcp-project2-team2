import pandas as pd
import mysql.connector
from pymongo import MongoClient

# MongoDB connection settings
mongo_uri = "mongodb://mongodb:27017/"
mongo_db_name = "data_db"
mongo_collection_name = "data_collection"

# MySQL connection settings
mysql_config = {
    'user': 'root',
    'password': 'password',
    'host': 'mysql',
    'database': 'data_db',
    'raise_on_warnings': True
}

# Connect to MongoDB
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

if mongo_collection.count_documents({}) == 0:
    print("MongoDB collection is empty")
else:
    print("MongoDB collection is not empty")

# Fetch data from MongoDB
data = list(mongo_collection.find({}))

# Convert to Pandas DataFrame

#weather_data = []
#for doc in data:
    #weather_record = {
        #'city_number': doc.get('city_number', 'Default Value'),
        #'city_name': doc.get('name', 'Default Value'),
        #'country': doc.get('sys', {}).get('country', 'Default Value'),
        #'latitude': doc.get('coord', {}).get('lat', 'Default Value'),
        #'longitude': doc.get('coord', {}).get('lon', 'Default Value'),
        #'temperature': doc.get('main', {}).get('temp', 'Default Value'),
        #'weather': doc.get('weather', [{'main': 'Default Value'}])[0].get('main', 'Default Value'),
        #'weather_desc': doc.get('weather', [{'description': 'Default Value'}])[0].get('description', 'Default Value')
    #}
    #weather_data.append(weather_record)


#df = pd.DataFrame(weather_data)

df = pd.DataFrame()

if len(data) > 0 and isinstance(data[0], dict):
    doc = data[0]
    weather_record = {
        'city_number': doc.get('city_number', 0),
        'city_name': doc.get('name', 'Default Value'),
	'country': doc.get('sys', {}).get('country', 'Default Value'),
    	'latitude': doc.get('coord', {}).get('lat', 'Default Value'),
    	'longitude': doc.get('coord', {}).get('lon', 'Default Value'),
    	'temperature': doc.get('main', {}).get('temp', 'Default Value'),
    	'weather': doc.get('weather', [{'main': 'Default Value'}])[0].get('main', 'Default Value'),
    	'weather_desc': doc.get('weather', [{'description': 'Default Value'}])[0].get('description', 'Default Value')
}
    df = pd.DataFrame([weather_record])

if not df.empty:
    print(df)
    # Connect to MySQL
    mysql_conn = mysql.connector.connect(**mysql_config)
    cursor = mysql_conn.cursor()

    # Prepare a SQL query to insert data
    insert_sql = """
    INSERT INTO weather (city_number, city_name, country, latitude, longitude, temperature, weather, weather_desc)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Iterate over DataFrame rows and execute SQL query for each row
    for row in df.itertuples(index=False):
        cursor.execute(insert_sql, tuple(row))

    # Commit and close MySQL connection
    mysql_conn.commit()
    cursor.close()
    mysql_conn.close()

else:
    print('DF is empty')
