# This file is doing some preliminary visualization of the highest group numbers for the area code of 41.

import matplotlib.pyplot as plt
import datetime
import sqlite3


# Get the group numbers from the table name and format it for the graph.
def get_group_numbers(name_of_table, cursor):
    # Collect data and set up return variables.
    rows = cursor.execute("SELECT * FROM " + name_of_table + " WHERE areanumber = 41 AND date < 20110101 AND date > 20081231").fetchall()
    dates = []
    group_numbers = []

    # Get data from database and form it into to lists for the plot.
    for row in rows:
        date_str = str(row[0])
        new_date = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))

        dates.append(new_date)
        group_numbers.append(row[2])

    return dates, group_numbers

def get_births(cursor):
    # Collect data and set up return variables.
    year_births = cursor.execute("SELECT * FROM births WHERE year < 2011 AND year > 2008").fetchall()
    birth_rates = cursor.execute("SELECT * FROM birthrates").fetchall()

    dates = []
    births = []
    running_total = 13

    for year_total in year_births:
        year = year_total[0]
        birth_total = year_total[1]
        print(birth_total)
        for rate_set in birth_rates:
            date_str = str(rate_set[0])
            new_date = datetime.date(int(year), int(date_str[4:6]), int(date_str[6:8]))
            dates.append(new_date)
            rate = rate_set[1]
            new_births = rate*birth_total/10*2/4000
            running_total += new_births
            births.append(running_total)

    # Get data from database and form it into to lists for the plot.

    return dates, births
def main():
    # Set up connection to database.
    connection = sqlite3.connect("Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()

    dates, births = get_births(cursor)
    date, group_numbers = get_group_numbers("groupnumbers", cursor)
    print(group_numbers)

    # Make plot.
    fig, ax = plt.subplots()
    ax.plot(date, group_numbers, "ro")
    ax.plot(dates, births)
    plt.show()


if __name__ == "__main__":
    main()

