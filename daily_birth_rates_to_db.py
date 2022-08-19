# This file takes the data imported by birth_csv_to_db into the table birthdates and generates daily birth rates.
# TODO: Have to make a.csv separate database for leap years.

import sqlite3
import datetime


# Take in births from the birthdates and get the total births across the 14 years by day. Returns data in the form of
# births_by_day (dict), which has datetime keys of every day of the year, and total (int), the total number of births
# in the file.
def get_births(name_of_table, cursor):

    # Get data and set up the return variables.
    rows = cursor.execute("SELECT * FROM " + name_of_table).fetchall()
    births_by_day = {}
    total = 0

    # Take data from birthdates and total for each day.
    for row in rows:
        # Clean data for return rows.
        date = str(row[0])
        converted_date = datetime.date(2000, int(date[4:6]), int(date[6:8]))
        births = row[1]

        # Collate data for return rows.
        total += births
        if converted_date in births_by_day:
            births_by_day[converted_date] += births
        else:
            births_by_day[converted_date] = births

    return births_by_day, total


# Takes in births_by_day (dict) and total (int) and formats them into rates and inserts them into the table as rows of
# form date and birth_rate.
def export_data_to_sql(births_by_day, total, export_table, cursor):
    for date in births_by_day:
        # Format data for database.
        sql_date = date.strftime('%Y%m%d')
        birth_rate = births_by_day[date]/total

        cursor.execute("INSERT INTO " + export_table +  " VALUES (" + sql_date + ", " + str(birth_rate)+ ")")


def main():
    # Set up connection and define variables.
    connection = sqlite3.connect("ssnNumbers.db")
    cursor = connection.cursor()
    import_table = "birthdates"
    export_table = "birthrates"

    births_by_day, total = get_births(import_table, cursor)
    export_data_to_sql(births_by_day, total, export_table, cursor)

    connection.commit()


if __name__ == "__main__":
    main()

