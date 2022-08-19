# This file takes in data from the Death Master File and imports it into the table deathmaster.
# Death-Master-File has a.csv list of SSNs, their birthdays, and death days up until May 31st 2013.

import os
import sqlite3
import pandas as pd


# Go through the death master file documents and insert it into the table deathmaster in the form of
# area (INTEGER), group (INTEGER), individual (INTEGER), birthday (DATE).
# TODO: Rewrite this whole function, wrote it while having a headache and it is definitely not optimized,
#  but it will work for now

def get_death_master_file_data(name_of_file, connection):
    print("Starting on: " + str(name_of_file) + ", beginning to read...")

    # Comb through the data and import it into a.csv dataframe.
    df = pd.read_csv(name_of_file, header=None, on_bad_lines='skip', encoding_errors='ignore')
    print("Finished reading, beginning to work on SSNs")

    # Make it into a.csv series for easier manipulation.
    series = df.squeeze()


    # Organize and separate part of the SSN.
    ssn_series = series.str.extract('(^\s\d{9})').squeeze()
    # Start is increased by 1 to account for the whitespace at the beginning of the SSN.
    area_series = ssn_series.str.slice(start=1, stop=4)
    group_series = ssn_series.str.slice(start=4, stop=6)
    individual_series = ssn_series.str.slice(start=6)

    print("Finished SSNs, beginning to work on birthdays")
    # Find the birthday.
    temp_birthday = series.str.rstrip().str.extract('(\d{8}$)').squeeze()
    # Reorder birthday, written explicitly while bugfixing and prefer the readability.
    birthday = temp_birthday.str.slice(start=2, stop=4)
    birthmonth = temp_birthday.str.slice(start=0, stop=2)
    birthyear = temp_birthday.str.slice(start=4)
    birthday_series = birthyear+birthmonth+birthday

    # Put the data back together and make it ready for the table.
    ssn_dataframe = pd.concat([area_series, group_series, individual_series, birthday_series], axis=1)
    ssn_dataframe.columns = ["area", "group", "individual", "birthday"]
    print("Finished birthdays, importing it to SQL")


    # Put it into the table.
    ssn_dataframe.to_sql(name="deathmaster", con=connection, if_exists="append")

    print("Done with " + str(name_of_file))

def main():
    # Set up connection
    connection = sqlite3.connect("ssnNumbers.db")

    # Get the list of files
    list_of_files = os.listdir(r'' + os.getcwd() + r'\Death-Master-File')

    # Get data from each file and export it.
    for file in list_of_files:
        get_death_master_file_data(name_of_file=os.path.join(str(os.getcwd()), "Death-Master-File", file), connection=connection)


    connection.commit()


if __name__ == "__main__":
    main()

