# This file takes in data from us_births_from_social.csv and import it to the table birthdates.
# us_births_from_social.csv has a.csv by day breakdown of the new social security number holders with rows
# year, month, date_of_month, day_of_week, and births, and it goes from 2000 to 2014.

import csv
import os
import sqlite3
import datetime


# Takes in the name of the file and returns the data in an array of rows of the form date (datetime), birth (int).
def get_births(name_of_file):
    births_by_date = []

    # Open the document and get the lines from it.
    with open(name_of_file) as csvfile:
        reader = csv.DictReader(csvfile)

        # Take in the line and convert it into the date and birth.
        for row in reader:
            date = datetime.datetime(int(row["year"]), int(row["month"]), int(row["date_of_month"]))
            births_by_date.append([date, int(row['births'])])

    return births_by_date


# Takes in the rows in form of date (datetime), births (int) which is generated by get_births and inserts rows into
# the database in form of date, and births
def export_data_to_sql(rows, cursor):
    for row in rows:
        date = row[0].strftime('%Y%m%d')  # convert date into proper format for SQL
        births = row[1]
        cursor.execute("INSERT INTO birthdates VALUES (" + date + ", " + str(births) + ")")


def main():
    # Set up connection to the database.
    connection = sqlite3.connect("ssnNumbers.db")
    cursor = connection.cursor()

    rows = get_births(os.path.join(str(os.getcwd()), "Birth-Data", "us_births_from_social.csv"))

    # Input the data into database.
    export_data_to_sql(rows, cursor)
    connection.commit()


if __name__ == "__main__":
    main()


