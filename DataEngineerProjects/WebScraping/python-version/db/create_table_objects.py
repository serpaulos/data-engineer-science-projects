import mysql.connector as msql
import config

conn = None

try:
    conn = msql.connect(database=config.db_name, user=config.user, password=config.password, host=config.host)
    print('Database connected.')
except:
    print('Database not connected.')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()
conn.autocommit = True

# Preparing query to create a database
sql_create_table = (f"""
    CREATE TABLE IF NOT EXISTS {config.table_name}(
    id  int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    category	varchar(40) NOT NULL,
	title       varchar(200) NOT NULL,	
    price		DECIMAL NOT NULL,
	rating      char(10) NOT NULL,
	stock		char(10) NOT NULL,
    extract_date timestamp default current_timestamp
    )
""")

# Creating a database
cursor.execute(sql_create_table)
print(f"Table {config.table_name} created successfully........")

# Closing the conn
conn.close()
