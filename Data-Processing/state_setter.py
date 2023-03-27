# This file goes through a table, in specific deathmaster and through the column state,
# and then matches it to its corresponding state via area_to_state.py's function
# determine_from_area()

import sqlite3
from area_to_state import determine_state_from_area


# Go through each area code and update the table with the corresponding state. NOTE: area in deathmaster is text, not
# an integer.
def update_state(area_code, table_name, column_name, cursor):
    state = determine_state_from_area(area_code)
    print("UPDATE " + table_name + " SET " + column_name + " = " + state + " WHERE area = " + str(area_code))
    cursor.execute("UPDATE " + table_name + " SET " + column_name + "=" + "\'" + state + "\'" + " WHERE area =" + "\'" + str(area_code) + "\'")


def main():
    # Set up connection
    connection = sqlite3.connect("../Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()

    for i in range(1, 1000):
        update_state(i, "deathmaster", "state", cursor)

    connection.commit()


if __name__ == "__main__":
        main()