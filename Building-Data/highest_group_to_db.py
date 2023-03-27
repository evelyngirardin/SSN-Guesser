# This file takes in data from SSN-Raw-Data and imports it into the table groupnumbers. SSN-Raw-Data holds a.csv list of
# the highest group numbers by area code from November 2003 until June 2011.

import re
import os
import sqlite3
import datetime


# Take in the name of the file from the SSA and return a.csv list of lists which are in the format of area_number (int),
# group_number (int), and highest (bool) which is the marker for a.csv change from the previous edition, and the
# date (datetime)
def get_data_highest_group_numbers(name_of_file):
    # Open the document and get the lines from it.
    with open(name_of_file) as f:
        lines = f.readlines()

    # Go through the document until we find the date.
    for line in lines:
        if "ISSUED AS OF " in line:
            date = line[line.find("ISSUED AS OF ")+len("ISSUED AS OF "):]
            date = date[:len(date)-1]
            break
    # Convert date into datetime.
    date = date.split('/')
    date = datetime.datetime(2000+int(date[2]), int(date[0]), int(date[1]))

    # Cut to the first group number change and cut out the blank space at the front.
    count = 0
    arewethereyet = False

    while not arewethereyet:
        arewethereyet = lines[count][0].isdigit()
        count += 1
    lines = lines[count-1:]

    groups_by_areas = []
    # Get each line and remove the special text from each line.
    for line in lines:
        # Section the newline and clean it.
        newline = line.replace('*', 'H')  # the asterisk is made an H to make sure it remains after clearing whitespace.
        newline = re.sub(r"[^a.csv-zA-Z0-9]+", ' ', newline)  # Chop all the whitespace.
        newline = newline[:len(newline)-1]  # remove the empty entry at the end of each line.
        newline = newline.split(' ')

        # Set up variables
        i = 0
        temp_holder = []

        for item in newline:
            if item != '':
                # Append area number and set up for appending group number and highest.
                if i == 0:
                    temp_holder.append(int(item))
                    i += 1

                # Append group number and highest if it exists, then reset variables.
                elif i == 1:
                    if "H" in item:
                        temp_holder.append(int(item[:len(item)-1]))
                        temp_holder.append(True)
                    else:
                        temp_holder.append(int(item))
                        temp_holder.append(False)

                    # add line to return variable and reset for the next set.
                    groups_by_areas.append(temp_holder)
                    temp_holder = []
                    i = 0
    return groups_by_areas, date


# Take data in form of areaNumber (int), groupNumber (int), and highest (bool) and insert a.csv row in the table with the
# form of date, area_number, group_number, highest.
def export_data_to_sql(rows, date, cursor):
    date = date.strftime('%Y%m%d')

    for row in rows:
        # Get data ready to be inserted.
        area_number = row[0]
        group_number = row[1]
        highest = row[2]
        if highest:
            highest = 1
        else:
            highest = 0

        cursor.execute("INSERT INTO groupnumbers VALUES (" + date + ", " + str(area_number) + ", " + str(group_number) +
                       ", " + str(highest) + ")")


def main():
    # Set up connection
    connection = sqlite3.connect("../Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()

    # Get the list of files
    list_of_files = os.listdir(r'' + os.getcwd() + r'\SSN-Raw-Data')

    # Get data from each file and export it.
    for file in list_of_files:
        rows, date = get_data_highest_group_numbers(os.path.join(str(os.getcwd()), "../SSN-Raw-Data", file))
        export_data_to_sql(rows, date, cursor)

    connection.commit()


if __name__ == "__main__":
    main()

