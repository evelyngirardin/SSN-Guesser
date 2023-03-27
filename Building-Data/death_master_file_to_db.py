# This file takes in data from the Death Master File and imports it into the table deathmaster.
# Death-Master-File has a.csv list of SSNs, their birthdays, and death days up until May 31st 2013.

import os
import sqlite3
import pandas as pd
import numpy as np

# TODO: Day and month are backwards in the database.
# Go through the death master file documents and insert it into the table deathmaster in the form of
# index (integer), area (INTEGER), group (INTEGER), individual (INTEGER), birthyear (INT),
# birthmonth (INT), birthday(INT).
def get_death_master_file_data(name_of_file, connection):
    print("Starting on: " + str(name_of_file) + ", beginning to read...")

    # Comb through the data and import it into a.csv dataframe.
    df = pd.read_csv(name_of_file, header=None, on_bad_lines='skip', encoding_errors='ignore')
    print("Finished reading, beginning to work on separating SSNs and birthdays")

    # Make it into a csv series for easier manipulation.
    series = df.squeeze()

    # Split out SSNs and Birthdays
    ssn_series = series.str.extract('(^\s\d{9})').squeeze()
    temp_birthday = series.str.rstrip().str.extract('(\d{8}$)').squeeze()

    print("Finished separating, creating temporary dataframe for manipulation.")

    ssn_series = pd.to_numeric(ssn_series, errors='coerce')
    temp_birthday = pd.to_numeric(temp_birthday, errors='coerce')
    holder_dataframe = pd.concat([ssn_series, temp_birthday], axis=1)
    holder_dataframe.columns = ["ssn", "birthday"]
    # Drop error based rows, convert to an integer to ensure no floats, convert back to a string for manipulation
    holder_dataframe = holder_dataframe.dropna(axis=0).astype(int).astype(str)

    print("Created temporary frame, generating SSN dataframes")
    # Split out parts of the SSN so they are separate for SQL
    individual = holder_dataframe['ssn'].str[-4:].astype(int)
    group = holder_dataframe['ssn'].str[-6:-4].astype(int)
    area = holder_dataframe['ssn'].str[:-6].astype(int)

    print("Finished SSNs, working on birthdays.")
    # Due to the earlier conversion, have to break out the birthday and put it back together in datetime format

    # Split birthday
    birthyear = holder_dataframe['birthday'].str[-4:].astype(int, errors='ignore')
    birthmonth = holder_dataframe['birthday'].str[-6:-4].astype(int, errors='ignore')
    birthday = holder_dataframe['birthday'].str[:-6].astype(int, errors='ignore')

    # Convert from parts to dates
 #   birthdate = pd.concat([birthyear, birthmonth, birthday], axis=1)
  #  birthdate.columns = ["year", "month", 'day']
   # birthdate.replace('', np.nan, inplace=True)
    #birthdate = birthdate.dropna()
    #birthdate = birthdate.astype(int)
    #birthdate = pd.to_datetime(birthdate, errors='ignore')
    #birthdate = birthdate.dropna()

    print("Finished birthday, creating full dataframe for SQL")
    # Put it all together now
    full_data = pd.concat([area, group, individual, birthyear, birthmonth, birthday], axis=1)
    full_data.columns = ['area', 'group', 'individual', 'birthyear', 'birthmonth', 'birthday']

    print("Dataframe made, importing to SQL")
    # Put it into the table.
    full_data.to_sql(name="deathmaster", con=connection, if_exists="append")

    print("Done with " + str(name_of_file))


def main():
    # Set up connection
    connection = sqlite3.connect("../Death-Master-File-Data/ssnNumbers.db")

    # Get the list of files
    list_of_files = os.listdir(r'' + os.getcwd() + r'\Death-Master-File')

    # Get data from each file and export it.
    for file in list_of_files:
        get_death_master_file_data(name_of_file=os.path.join(str(os.getcwd()), "Death-Master-File", file), connection=connection)

    connection.commit()


if __name__ == "__main__":
    main()

