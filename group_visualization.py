# This file is doing some preliminary visualization of the highest group numbers for the area code of 41.

import matplotlib.pyplot as plt
import datetime
import sqlite3


# Get the births from the table name and format it for the graph.
def get_births(name_of_table, cursor):
    # Collect data and set up return variables.
    rows = cursor.execute("SELECT * FROM " + name_of_table + " WHERE areanumber = 41").fetchall()
    dates = []
    group_numbers = []

    # Get data from database and form it into to lists for the plot.
    for row in rows:
        date_str = str(row[0])
        new_date = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))

        dates.append(new_date)
        group_numbers.append(row[2])
    return dates, group_numbers


def main():
    # Set up connection to database.
    connection = sqlite3.connect("ssnNumbers.db")
    cursor = connection.cursor()

    date, group_numbers = get_births("groupnumbers", cursor)

    # Make plot.
    fig, ax = plt.subplots()
    ax.plot(date, group_numbers, "ro")
    plt.show()


if __name__ == "__main__":
    main()

