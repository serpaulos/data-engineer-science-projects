import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import time
import config

try:
    actualdate = time.strftime("%d-%m-%Y")
    book_data = pd.read_csv('./data/books/' + actualdate + '-books.csv', encoding = 'utf8', header = None)
except:
    print("No file inside the folder... Run webscraper.py in order to create the file")

try:
    conn = msql.connect(database=config.db_name, user=config.user, password=config.password, host=config.host)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        for i, row in book_data.iterrows():
            #Travel,It's Only the Himalayas,45.17,Two,In stock
            sql = f"INSERT INTO {config.table_name} (category, title, price, rating, stock) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

#Closing the conn
conn.close()