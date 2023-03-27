# This file is using the Area Number Function to input each area number and its corresponding state to the DB.

import sqlite3
from area_to_state import determine_state_from_area


def main():
    # Set up the connection
    connection = sqlite3.connect("../Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()

    # Loop through all the possible area codes and input the area code and their state into the database.
    for i in range(1, 1000):
        state = determine_state_from_area(i)
        cursor.execute("INSERT INTO areacodestates VALUES (" + str(i) + ", " + "'" + str(state) + "')")

    connection.commit()


if __name__ == "__main__":
    main()
