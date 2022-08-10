# This file is doing some preliminary visualization of the highest group numbers for the area code of 41.

import matplotlib.pyplot as plt
import datetime
import sqlite3
import os

def get_births(name_of_table, connection):
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM " + name_of_table + " WHERE areanumber = 41").fetchall()
    dates = []
    groupnumbers = []
    for row in rows:
        date_str = str(row[0])
        new_date = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
        dates.append(new_date)
        groupnumbers.append(row[2])
    return dates, groupnumbers


def main():
    connection = sqlite3.connect("ssnNumbers.db")
    date, groupnumber = get_births("groupnumbers", connection)

    fig, ax = plt.subplots()
    ax.plot(date, groupnumber, "ro")
    plt.show()


if __name__ == "__main__":
    main()

