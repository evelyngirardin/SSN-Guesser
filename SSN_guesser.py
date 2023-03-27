# This file is doing some preliminary visualization of the highest group numbers for the area code of 41.

import datetime
import time
import sqlite3
import calendar


# Our current estimate of change in group number is 6850.355555555556
AREA_NUMBER_BIRTHS_AVERAGE = 6850.355555555556
INDIVIDUAL_NUMBER_ERROR = 2593-726-1561

def add_white_space(month):
    if len(str(month)) == 1:
        month = '0' + str(month)
    else:
        month = str(month)
    return month

def increase_month(year, month):
    if month == 12:
        end_year = year + 1
        end_month = 1
    else:
        end_year = year
        end_month = month + 1

    return end_year, end_month

def decrease_month(year, month):
    if month == 1:
        end_year = year - 1
        end_month = 12
    else:
        end_year = year
        end_month = month - 1

    return end_year, end_month

def process_boundries(pairs_of_dates, i):
    lower_year = str(pairs_of_dates[i][0])
    lower_month = add_white_space(pairs_of_dates[i][1])

    upper_year = str(pairs_of_dates[i + 1][0])
    upper_month = add_white_space(pairs_of_dates[i + 1][1])

    return lower_year, lower_month, upper_year, upper_month

def generate_sql_statement(year, month, end_year, end_month, cursor, name_of_table):
    day = '00'
    rows = cursor.execute("SELECT * FROM " + name_of_table + " WHERE date >= " + year + month + day +
                          " AND date < " + end_year + end_month + day + ' AND ' + 'areanumber < 50 AND areanumber > 39').fetchall()

    return rows

# Get the group numbers from the table name and format it for the graph.
def get_group_numbers(name_of_table, birth_date, cursor):
    end = datetime.date(2011, 6, 24)
    start = datetime.date(2003, 11, 3)
    rows = []
    if start <= birth_date <= end:
        birth_year = birth_date.year
        birth_month = birth_date.month
        pairs_of_dates = []

        if birth_year > 2003 or (birth_year == 2003 and birth_month > 11):
            prev_year, prev_month = decrease_month(birth_year, birth_month)
            pairs_of_dates.append([prev_year, prev_month])

        pairs_of_dates.append([birth_year, birth_month])

        if birth_year < 2011 or (birth_year==2011 and birth_month < 6):
            next_year, next_month = increase_month(birth_year, birth_month)
            pairs_of_dates.append([next_year, next_month])

        if birth_year < 2011 or (birth_year==2011 and birth_month+1 < 6):
            next_year, next_month = increase_month(birth_year, birth_month)
            final_year, final_month = increase_month(next_year, next_month)
            pairs_of_dates.append([final_year, final_month])

        for i in range(0, len(pairs_of_dates)-1):
            lower_year, lower_month, upper_year, upper_month = process_boundries(pairs_of_dates, i)
            rows.append(generate_sql_statement(lower_year, lower_month, upper_year, upper_month, cursor, name_of_table))

    else:
        if birth_date >= end:
            lower_year = end.year
            lower_month = end.month
            upper_year, upper_month = increase_month(lower_year, lower_month)
            pairs_of_dates = [[lower_year, lower_month], [upper_year, upper_month]]

            lower_year, lower_month, upper_year, upper_month = process_boundries(pairs_of_dates, 0)

            rows.append(generate_sql_statement(lower_year, lower_month, upper_year, upper_month, cursor, name_of_table))

        elif birth_date < start:
            lower_year = start.year
            lower_month = start.month
            upper_year, upper_month = increase_month(lower_year, lower_month)
            pairs_of_dates = [[lower_year, lower_month], [upper_year, upper_month]]

            lower_year, lower_month, upper_year, upper_month = process_boundries(pairs_of_dates, 0)

            rows.append(generate_sql_statement(lower_year, lower_month, upper_year, upper_month, cursor, name_of_table))

    return rows

def return_greatest_record(row):
    highest = 0
    record_to_return = row[0]
    for record in row:
        if record[2] >= highest:
            highest = record[2]
            record_to_return = record
    return record_to_return

def get_births(dates, cursor):
    # Collect data and set up return variables.
    year_births = dict(cursor.execute("SELECT * FROM births").fetchall())
    birth_rates = dict(cursor.execute("SELECT * FROM birthrates").fetchall())
    leap_rates = dict(cursor.execute("SELECT * FROM leaprates").fetchall())
    births = []

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
            running_total += day_births
            i_date += one_day

        births.append(running_total)

    return dates, births

def guess_ssn_from_birth_date(birth_date, cursor):
    rows = get_group_numbers("groupnumbers", birth_date, cursor)
    greatest_records = []
    necessary_dates = [birth_date]

    for row in rows:
        if row!=[]:
            greatest_record = return_greatest_record(row)
            greatest_records.append(greatest_record)
            year = int(str(greatest_record[0])[:4])
            month = int(str(greatest_record[0])[4:6])
            day = int(str(greatest_record[0])[6:])

            date = datetime.date(year, month, day)
            necessary_dates.append(date)

    necessary_dates.sort()
    dates, births = get_births(necessary_dates, cursor)

    index_of_birthday = necessary_dates.index(birth_date)
    births_before_birthday = sum(births[:index_of_birthday])
    births_after_birthday = sum(births[index_of_birthday:])

    if index_of_birthday != len(greatest_records):
        record_before_birthday = greatest_records[index_of_birthday-1]
        record_after_birthday = greatest_records[index_of_birthday]

        before_area = record_before_birthday[1]
        before_group = record_before_birthday[2]

        after_area = record_after_birthday[1]
        after_group = record_after_birthday[2]
    else:
        record_before_birthday = greatest_records[index_of_birthday - 1]

        before_area = record_before_birthday[1]
        before_group = record_before_birthday[2]

        after_area = before_area
        after_group = before_group

    if after_area == before_area:
        area_guess = after_area
        holder = -1

    else:
        if births_before_birthday < births_after_birthday:
            area_guess = before_area
            holder = -1
        else:
            area_guess = after_area
            holder = 1

    if before_group == after_group:
        group_guess = after_group

    else:
        if births_before_birthday < births_after_birthday:
            group_guess = before_group
        else:
            group_guess = after_group

    # I think to fix this I need to make a histogram of the individual numbers that appear within the deathmaster file.
    if holder == 1:
        individual_guess = int(9999*(1 - births_after_birthday/AREA_NUMBER_BIRTHS_AVERAGE))-INDIVIDUAL_NUMBER_ERROR
    else:
        individual_guess = int(9999*(births_before_birthday/AREA_NUMBER_BIRTHS_AVERAGE))-INDIVIDUAL_NUMBER_ERROR

    individual_guess_range = range(individual_guess-500, individual_guess+500)

    return area_guess, group_guess, individual_guess, individual_guess_range

def main():
    connection = sqlite3.connect("C:/Users/jacob/PycharmProjects/SSN-Guesser/Death-Master-File-Data/ssnNumbers.db")
    cursor = connection.cursor()
    records = cursor.execute("SELECT birthyear, birthmonth, birthday, area, deathmaster.'group', individual " +
                             "FROM deathmaster WHERE birthyear > 2004 AND birthyear < 2010 AND STATE = 'CT'").fetchall()
    total_individual_error = 0
    ssr = 0
    sst = 0
    average_individual = 0
    guesses_within_range = 0
    correct_area = 0
    correct_group = 0

    for record in records:
        average_individual += record[5]

    average_individual = average_individual/len(records)

    for record in records:
        birth_date = datetime.date(record[0], record[1], record[2])
        area = record[3]
        group = record[4]
        individual = record[5]
        area_guess, group_guess, individual_guess, individual_guess_range = guess_ssn_from_birth_date(birth_date,
                                                                                                      cursor)
        total_individual_error += (individual - individual_guess)
        ssr += pow(individual - individual_guess, 2)
        sst += pow(individual - average_individual, 2)
        if individual in individual_guess_range:
            guesses_within_range+=1

        if area == area_guess:
            correct_area+=1

        if group == group_guess:
            correct_group+=1

    r2 = 1 - (ssr/sst)
    print("Average Individual Error: " + str(total_individual_error/len(records)))
    print("Percent of Guesses within Range: " + str(guesses_within_range/len(records)))
    print("R^2: " + str(r2))
    print("Correct Area: " + str(correct_area) + " | " + str(correct_area/len(records)))
    print("Correct Group: " + str(correct_group) + " | " + str(correct_group/len(records)))






if __name__ == "__main__":
    main()

