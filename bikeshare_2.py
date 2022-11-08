import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = ''
    day = ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        print("Please enter the city you want:\n 1-Chicago \t 2-New York City \t 3-Washington")
        print("Note that valid input is city name example you should enter Chicago or chicago")
        city = input(">>>").lower()
        check_city = city in CITY_DATA.keys()
        if not check_city:
            print("Opps... You entered a city that does not exist")

    # get user input for month (all, january, february, ... , june)
    MONTH_DATA = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'all'}
    month_number = 0
    while month_number not in MONTH_DATA.keys():
        print("Please enter the month number you want:\n 1:january\t 2:february\t 3:march\t 4:april\t 5:may\t "
              "6:june\t 7:all")
        print("Note that valid input is number example you want march you should enter number 3")
        try:
            month_number = int(input(">>>"))
            check_month = month_number in MONTH_DATA.keys()
            if not check_month:
                print("Opps... You entered a month number that does not exist or you enter letters instead of number")
                print("Please enter the month number again Note that the available month is 1, 2, 3, 4, 5, 6 , 7")
        except:
            print("You enter invalid value ... Please enter number only from 1 to 7")

    month = MONTH_DATA[month_number]
    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    while day not in DAY_DATA:
        print("Please enter the day you want:\n Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday and all")
        print("Note that valid input is day name example you want monday you should enter monday")
        day = input(">>>").lower()
        check_day = day in DAY_DATA
        if not check_day:
            print("Opps... You entered a invalid input")
            print(
                "Please enter name of the day again Note that the available day is Monday, Tuesday,..., Sunday and all")

    print("You have selected the data for a city: {}, Month: {} and day: {}".format(city.title(), month.title(),
                                                                                    day.title()))
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # create dataframe from file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column from object to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new column for month and day from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # return dataframe after all operation

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print("The most common month is {}".format(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day of week is {}".format(df['day_of_week'].mode()[0]))

    # create column for hour from Start Time
    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    print("The most common start hour is {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is {}".format(df['End Station'].mode()[0]))

    # create column for combination of start station and end station trip
    df['Start To End'] = df['Start Station'] + ' to ' + df['End Station']
    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip is {}".format(
        df['Start To End'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def convert_second(travel_time):
    seconds = travel_time % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return round(hour), round(minutes), round(seconds)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    hour, minutes, seconds = convert_second(total_travel)
    print("The total travel time is {} hours, {} minutes and {} seconds".format(hour, minutes, seconds))
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    hour2, minutes2, seconds2 = convert_second(mean_travel)
    print("The mean travel time is {} hours, {} minutes and {} seconds".format(hour2, minutes2, seconds2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The number of user types:\n{}".format(df['User Type'].value_counts()))
    # Because column gender and birth year doesn't exist in all data files
    try:
        # Display counts of gender
        print("The number of user types:\n{}".format(df['Gender'].value_counts()))
    except:
        print("The gender column doesn't exist in this file")

    try:
        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("The birth year column doesn't exist in this file")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    index_row = 0
    check_user = input("Do you want to see 5 rows of data? (Enter yes or no)\n").lower()
    while check_user == 'yes':
        print(tabulate(df.iloc[index_row:(index_row + 5)], headers = 'keys', tablefmt = 'psql'))
        index_row += 5
        check_user = input("Do you want to see the next 5 rows of data? (Enter yes or no)\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
