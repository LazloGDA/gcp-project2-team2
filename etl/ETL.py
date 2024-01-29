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

# Fetch data from MongoDB
data = list(mongo_collection.find({}))

# Convert to Pandas DataFrame
#df = pd.DataFrame(mongo_docs)
#df = pd.json_normalize(data)

# Handle the 'weather' part separately
weather_data = dict()
weather_data['city_number'] = '1'
weather_data['city_name'] = data['name']
weather_data['country'] = data['sys']['country']
weather_data['latitude'] = data['coord']['lat']
weather_data['longitude'] = data['coord']['lon']
weather_data['temperature'] = data['main']['temp']
weather_data['weather'] = data['weather'][0]['main']
weather_data['weather_desc'] = data['weather'][0]['description']

df = pd.DataFrame([weather_data])

#weather_data = pd.json_normalize(df['weather'][0] if 'weather' in df.columns else [])
#weather_columns = [f'weather.{col}' for col in weather_data.columns]
#df[weather_columns] = weather_data

# Drop the original 'weather' column
df.drop('weather', axis=1, inplace=True)

# Connect to MySQL
mysql_conn = mysql.connector.connect(**mysql_config)
cursor = mysql_conn.cursor()

# Prepare a SQL query to insert data
# Note: Adjust the SQL statement according to your table schema

insert_sql = """
INSERT INTO your_table_name (city_number, city_name, country, latitude, longitude, temperature, weather, weath>
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
# Iterate over DataFrame rows and execute SQL query for each row
for row in df.itertuples(index=False):
    cursor.execute(insert_sql, tuple(row))

# Commit and close MySQL connection
mysql_conn.commit()
cursor.close()
mysql_conn.close()

print("Data transfer complete.")
