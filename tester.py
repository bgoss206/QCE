import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="97959795Trey!",
    database = 'testdatabase'
)

mycursor = db.cursor()


