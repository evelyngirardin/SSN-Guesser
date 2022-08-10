import sqlite3

connection = sqlite3.connect("ssnNumbers.db")

cursor = connection.cursor()
cursor.execute("SELECT * FROM groupnumbers")