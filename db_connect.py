import mysql.connector

db_connect = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="base",
    port="3306"
)

cursor = db_connect.cursor()
