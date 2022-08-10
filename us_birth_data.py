import re
import csv
import os
import sqlite3
import datetime
import matplotlib

def get_births(name_of_table, connection):
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM " + name_of_table).fetchall()
    value_dict = {}
    total = 0
    for row in rows:
        date = str(row[0])
        new_date = datetime.date(2000, int(date[4:6]), int(date[6:8]))
        births = row[1]
        #if not (new_date.day == 29 and new_date.month == 2):
        if new_date in value_dict:
            value_dict[new_date] += births
        else:
            value_dict[new_date] = births
        total += births
    return value_dict, total


def export_data_to_sql(export_table, import_table, connection):
    cursor = connection.cursor()
    dict, total = get_births(import_table, connection)
    for date in dict:
        sql_date = date.strftime('%Y%m%d')
        birth_rate = dict[date]/total
        cursor.execute("INSERT INTO " + export_table +  " VALUES (" + sql_date + ", " + str(birth_rate)+ ")")
        print("INSERT INTO " + export_table +  " VALUES (" + sql_date + ", " + str(birth_rate)+ ")")


currentdir = str(os.getcwd())
connection = sqlite3.connect("ssnNumbers.db")
export_data_to_sql("leaprates", "birthdates", connection)
connection.commit()