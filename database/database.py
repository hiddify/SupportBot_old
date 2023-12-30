# database/database

import mysql.connector
import datetime, os
from log import log

# Load environment variables from .env file
load_dotenv()

# Define database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Define tables
USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  telegram_id VARCHAR(255) UNIQUE,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  username VARCHAR(255),
  is_admin BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255),
  message_id VARCHAR(255),
  message_type VARCHAR(255),
  message_data LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

OPTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS options (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) UNIQUE,
  value TEXT
)
"""

# Define database connection function
def connect():
     try:
          conn = mysql.connector.connect(
               host=DB_HOST,
               user=DB_USER,
               port=DB_PORT,
               password=DB_PASSWORD,
               database=DB_NAME,
               auth_plugin='mysql_native_password'
          )
          return conn
     except Exception as e:
          log.log_error(e)
          print('Error connecting to database:', e)
          return None

# Define initialization function
def init():
     conn = connect()

     # Check if the necessary tables exist in the database
     cursor = conn.cursor()

     # Tables
     tables = [
          "users",
          "messages",
          "options"
     ]

     if conn:
          for table in tables:
               cursor.execute(f"SHOW TABLES LIKE '{table}'")
               result = cursor.fetchone()
               if result:
                    # print(f"{table} table already exists.")
                    continue
               else:
                    # Create the table if it does not exist
                    if table == "users":
                         cursor.execute(USERS_TABLE)
                    elif table == "messages":
                         cursor.execute(MESSAGES_TABLE)
                    elif table == "options":
                         cursor.execute(OPTIONS_TABLE)


          cursor.close()
          conn.close()

# Define user insertion function
def insert_user(telegram_id, first_name, last_name, username):
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "SELECT * FROM users WHERE telegram_id = %s"
          value = (telegram_id,)
          cursor.execute(query, value)
          result = cursor.fetchone()
          cursor.close()
          conn.close()

          # If the user already exists in the database, do nothing
          if result:
               return
          # If the user does not exist in the database, insert their data into the database
          else:
               conn = connect()
               cursor = conn.cursor()
               query = "INSERT INTO users (telegram_id, first_name, last_name, username, is_admin) VALUES (%s, %s, %s, %s, %s)"
               values = (telegram_id, first_name, last_name, username, False)
               cursor.execute(query, values)
               conn.commit()
               cursor.close()
               conn.close()
               return

# Get user by telegram ID
def get_user(telegram_id):
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "SELECT * FROM users WHERE telegram_id = %s"
          values = (telegram_id,)
          cursor.execute(query, values)
          result = cursor.fetchone()
          cursor.close()
          conn.close()
          return result

# Get user by username
def get_user_by_username(username):
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "SELECT * FROM users WHERE username = %s"
          values = (username,)
          cursor.execute(query, values)
          result = cursor.fetchone()
          cursor.close()
          conn.close()
          return result

# Define admin retrieval function
def get_admins():
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "SELECT * FROM users WHERE is_admin = %s"
          values = (1,)
          cursor.execute(query, values)
          admins = cursor.fetchall()
          cursor.close()
          conn.close()
          return [admin[1] for admin in admins] if admins else []

# Insert a message into the database
def insert_message(user_id, message_id, message_type, message_data):
     current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "INSERT INTO messages (user_id, message_id, message_type, message_data, created_at) VALUES (%s, %s, %s, %s, %s)"
          values = (user_id, message_id, message_type, message_data, current_time)
          cursor.execute(query, values)
          conn.commit()
          cursor.close()
          conn.close()
          return

# Get an option from the database
def get_option(option_name):
     conn = connect()
     if conn:
          cursor = conn.cursor()
          query = "SELECT option_value FROM options WHERE option_name = %s"
          values = (option_name,)
          cursor.execute(query, values)
          result = cursor.fetchone()
          cursor.close()
          conn.close()
          if result:
               return result[0]
          else:
               return None

if __name__ == '__main__':
    init()
