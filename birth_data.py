import re
import csv
import os
import sqlite3
import datetime

# Takes in the name of the file and cleans the data into an array of rows.
def get_births(name_of_file):
    value_rows = []
    # Open the document and get the lines from it.
    with open(name_of_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)

            date = datetime.datetime(int(row["year"]), int(row["month"]), int(row["date_of_month"]))
            value_rows.append([date, int(row['births'])])
    return value_rows

def export_data_to_sql(name_of_file, connection):
    cursor = connection.cursor()
    rows = get_births(name_of_file)
    for row in rows:
        date = row[0].strftime('%Y%m%d')
        births = row[1]
        imbtw = ", "
        cursor.execute("INSERT INTO birthdates VALUES (" + date + imbtw + str(births) + ")")



currentdir = str(os.getcwd())
connection = sqlite3.connect("ssnNumbers.db")
export_data_to_sql(os.path.join(currentdir, "Birth-Data", "us_births_from_social.csv"), connection)
connection.commit()
