# -*- coding: utf-8 -*-
"""HelloWorld.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kNnsHZe9mP7jcu3Iq06ezi8bgotfy1fr
"""

print('Hello world')

#pip install mysql-connector-python

import mysql.connector
cnx = mysql.connector.connect(
    user = "root",
    password = "Start!789",
    host = "34.159.112.89",
    database = "Data_DB"
)

cursor = cnx.cursor()

select_query = ("SELECT * FROM DATA_DB.weather")

cursor.execute(select_query)

for row in cursor.fetchall():
    print(row)

cursor.close()
cnx.close()