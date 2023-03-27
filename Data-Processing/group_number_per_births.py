# This file is doing some preliminary visualization of the highest group numbers for the area code of 41.

import datetime
import sqlite3
import calendar

# Get the group numbers from the table name and format it for the graph.
def get_group_numbers(name_of_table, areanumber,  cursor):
    # Collect data and set up return variables.
    rows = cursor.execute("SELECT * FROM " + name_of_table + " WHERE areanumber = " + str(areanumber) + " AND highest = 1").fetchall()
    dates = []
    group_numbers = []
    rows.sort()
   # Get data from database and form it into to lists for the plot.
    for row in rows:
        date_str = str(row[0])
        new_date = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))

        dates.append(new_date)

        group_numbers.append(row[2])
    return dates, group_numbers

def get_births(dates, cursor):
    # Collect data and set up return variables.
    year_births = dict(cursor.execute("SELECT * FROM births").fetchall())
    birth_rates = dict(cursor.execute("SELECT * FROM birthrates").fetchall())
    leap_rates = dict(cursor.execute("SELECT * FROM leaprates").fetchall())
    births = [0]

    one_day = datetime.timedelta(days=1)
    for i in range(0, len(dates)-1):
        running_total = 0
        starting_date = dates[i]
        end_date = dates[i+1]
        i_date = starting_date

        while i_date < end_date:
            i_text = i_date.strftime('%Y%m%d')
            birth_total = year_births[i_date.year]
            key = int("2000" + i_text[4:])

            if calendar.isleap(i_date.year):
                birth_rate = leap_rates[key]
            else:
                birth_rate = birth_rates[key]

            day_births = birth_total*birth_rate
            running_total+= day_births
            i_date += one_day

        births.append(running_total)

    return dates, births

def get_average_births(type='average'):
    # Set up connection to database.
    connection = sqlite3.connect("../Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()
    births_per_group_number = []
    total_groups = []
    for x in range(40, 50):
        group_dates, group_numbers = get_group_numbers("groupnumbers", x, cursor)
        birth_dates, births = get_births(group_dates, cursor)
        total_groups.append(group_numbers)
        for i in range(0, len(birth_dates)):
            b = int(births[i])
            if b != 0:
                births_per_group_number.append(b)

    return (sum(births_per_group_number)/len(births_per_group_number))




if __name__ == "__main__":
    print(get_average_births())

