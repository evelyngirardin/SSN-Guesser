import re
import csv
import os
import sqlite3
import datetime

# Takes in the name of the file and cleans the data into an array of rows.
def get_data_highest_group_numbers(name_of_file):
    # Open the document and get the lines from it.
    with open(name_of_file) as f:
        lines = f.readlines()
    value_rows = []


    for line in lines:
        if "ISSUED AS OF " in line:
            date = line[line.find("ISSUED AS OF ")+len("ISSUED AS OF "):]
            date = date[:len(date)-1]
            break
    date = date.split('/')
    print(name_of_file)
    print(date)
    date = datetime.datetime(2000+int(date[2]), int(date[0]), int(date[1]))

    # Cut to the first group number change and cut out the blank space at the
    # end.
    count = 0
    arewethereyet = False
    while not arewethereyet:
        arewethereyet = lines[count][0].isdigit()
        count += 1
    lines = lines[count-1:]

    # Get each line and remove the special text from each line. We change
    # the change marker to an H to ensure it remains.
    for line in lines:
        newline = line.replace('*', 'H')
        newline = re.sub(r"[^a-zA-Z0-9]+", ' ', newline)

        # Removes the empty entry at the end of each line.
        newline = newline[:len(newline)-1]
        newline = newline.split(' ')
        i=0
        appender = []
        for item in newline:
            if item != '':
                if i == 0:
                    appender.append(int(item))
                    i+=1
                elif i == 1:
                    if "H" in item:
                        appender.append(int(item[:len(item)-1]))
                        appender.append(True)
                    else:
                        appender.append(int(item))
                        appender.append(False)
                    value_rows.append(appender)
                    appender = []
                    i=0
    return value_rows, date

def export_data_to_sql(name_of_file, connection):
    cursor = connection.cursor()
    rows, date = get_data_highest_group_numbers(name_of_file)
    date = date.strftime('%Y%m%d')
    for row in rows:
        areaNumber = row[0]
        groupNumber = row[1]
        highest = row[2]
        if highest:
            highest = 1
        else:
            highest = 0
        imbtw = ", "
        cursor.execute("INSERT INTO groupnumbers VALUES (" + date + imbtw + str(areaNumber) + imbtw + str(groupNumber) + imbtw + str(highest) + ")")



list_of_files = os.listdir(r''+os.getcwd() + r'\SSN-Raw-Data')
currentdir = str(os.getcwd())
connection = sqlite3.connect("ssnNumbers.db")
for file in list_of_files:
    export_data_to_sql(os.path.join(currentdir, "SSN-Raw-Data", file), connection)
connection.commit()
