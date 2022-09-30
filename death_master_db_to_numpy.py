import datetime

import numpy as np
import sqlite3
import pandas as pd
import pandas.io.sql as psql

def main():
    connection = sqlite3.connect("Death-Master-File-Data/ssnNumbers.db")
    print('Fetching Data')
    sql = '''
                    SELECT *
                    FROM deathmaster 
                    WHERE birthdate > 1940000 AND state != 'NotIssued'
                    ''' # The 1940 cutoff is arbitrary but hopefully gets past most people who were born earlier than
                         # the SSN program started.
    df = psql.read_sql(sql, connection)
    print("Read, converting dataframe to numpy")
    df = df.to_numpy()
    np.save('Death-Master-File-Data/formatted_data', df)

if __name__ == '__main__':
    main()