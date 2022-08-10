import re
import csv
import os
import sqlite3

# Takes in the name of the file and cleans the data into an array of rows.
def get_data_highest_group_numbers(name_of_file):
    # Open the document and get the lines from it.
    with open(name_of_file) as f:
        lines = f.readlines()
    csv_rows = []


    for line in lines:
        if "ISSUED AS OF " in line:
            date = line[line.find("ISSUED AS OF ")+len("ISSUED AS OF "):]
            date = date[:len(date)-1]
            break
    date = date.split('/')

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
                    appender.append(item)
                    i+=1
                elif i == 1:
                    if "H" in item:
                        appender.append(item[:len(item)-1])
                        appender.append('*')
                    else:
                        appender.append(item)
                        appender.append('')
                    csv_rows.append(appender)
                    appender = []
                    i=0
    return csv_rows, date


# Takes in the name of the txt file from the SSA and exports a cleaned CSV of
# values to cleaned_(month)-(year).csv
def export_data_to_csv(name_of_file):

    # Create the fields at the top of the sheet
    fields = ['Area Number', "Group Number", "Latest Changes"]

    rows, date = get_data_highest_group_numbers(name_of_file)
    currentdir = os.getcwd()
    # Write the CSV
    filename = "cleaned_" + str(int(date[0])) + '-' + str(int(date[2])) + ".csv"
    os.chdir(r''+os.getcwd() + r'\SSN-Cleaned-Data')
    with open(filename, 'w', newline='') as csvfile:

        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    os.chdir(currentdir)


list_of_files = os.listdir(r''+os.getcwd() + r'\SSN-Raw-Data')
currentdir = str(os.getcwd())
for file in list_of_files:
    export_data_to_csv(os.path.join(currentdir, "SSN-Raw-Data", file))
