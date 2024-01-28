import time
import logging
import mysql.connector

def get_db_connection_on_docker() :

  INSTCONN_NAME = f"{'docker-compose'}:{'gcp-project2-team2'}:{'sqldb'}"
  DB_USER = "dba"
  DB_PASS = "A1YTsqilzHkUQ4"
  DB_NAME = "metabase"
  HOST = "sqldb" # Container name in docker compose.yaml
  logging.info('InstConnName', INSTCONN_NAME)
  cnx = mysql.connector.connect(
    user = DB_USER,
    password = DB_PASS,
    host = HOST, #Cloud SQL instance internal IP address
    database = DB_NAME
    )

  return cnx

def insert_db_table(environment, df):
  if environment == 'VM':
    cnx = get_db_connection_on_vm()
  elif environment == 'DOCKER':
    cnx = get_db_connection_on_docker()    
  else:
    cnx = get_db_connection_on_colab()

  cursor = cnx.cursor()

  insert_stmt = (
    "INSERT INTO weather (city_number, city_name, country, latitude, longitude, temperature, weather, weather_desc, pic_url) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  )

  cursor.execute("DELETE FROM weather")
  cnx.commit()

  for i, row in df.iterrows():
        data = (row['city_number'], row['city_name'], row['country'], row['latitude'], row['longitude'],
                row['temperature'], row['weather'], row['weather_desc'], row['pic_url'])
        cursor.execute(insert_stmt, data)
  cnx.commit()
  print(f"{cursor.rowcount} rows inserted.")


  cursor.close()
  cnx.close()

def select_db_table(environment, df):
  if environment == 'VM':
    cnx = get_db_connection_on_vm()
  elif environment == 'DOCKER':
    cnx = get_db_connection_on_docker()    
  else:
    cnx = get_db_connection_on_colab()

  cursor = cnx.cursor()

  query = ("SELECT * from weather "
         )
  cursor.execute(query)

  for row in cursor.fetchall():
      print(row)

  cursor.close()
  cnx.close()

def create_db_table(environment):

  if environment == 'VM':
    cnx = get_db_connection_on_vm()
  elif environment == 'DOCKER':
    cnx = get_db_connection_on_docker()    
  else:
    cnx = get_db_connection_on_colab()

    #Creating a cursor object using the cursor() method
  cursor = cnx.cursor()
  
  #Dropping EMPLOYEE table if already exists.
  cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
  
  #Creating table as per requirement
  sql ='''CREATE TABLE EMPLOYEE(
     FIRST_NAME CHAR(20) NOT NULL,
     LAST_NAME CHAR(20),
     AGE INT,
     SEX CHAR(1),
     INCOME FLOAT
  )'''
  cursor.execute(sql)
  
  #Closing the connection
  conn.close()


# Create tables
environment = 'DOCKER'
#environment = 'VM'
#environment = 'COLAB'

print('Create table in MySQL DB')

create_db_table(environment)































i=1

while i == 100:
    time.sleep(5)
    logging.info(f"Hello from the Python Container! {i}")
    i += 1

df_list = ["city_number", "city_name", "country", "latitude", "longitude", "temperature", "weather", "weather_desc", "pic_url"]

