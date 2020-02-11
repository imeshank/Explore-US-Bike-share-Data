import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Would you like to see data for Chicago, New York, or Washington?\n").strip().lower()
    #checks whether user input a correct city
    while (city.lower() not in CITY_DATA):
        city = input("Please enter a correct city: Chicago, New York, or Washington?\n").strip().lower()

    #get user input for filter
    filter = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter\n").strip().lower()
    month = 'all'
    day = 'all'

    if(filter == 'month' or filter == 'both'):
        # get user input for month (all, january, february, ... , june)
        month = input("Which month? January, February, March, April, May, June? Please type out the full month name\n").strip().lower()
        while month.lower() not in months:
            month = input("Please enter a correct month? January, February, March, April, May, June? Please type out the full month name\n").strip().lower()

    if(filter == 'day' or filter == 'both'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday? Please type out the full name\n").strip().lower()
        while day.lower() not in days:
            day = input("Please enter a correct day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday? Please type out the full name\n").strip().lower()


    print("\nData are filtered by,  City: {},   Month: {},   Day: {}\n".format(city.title(), month.title(), day.title()))


    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':
        # TO DO: display the most common month and it's frequency
        most_common_month = int(df['month'].mode())
        count = df['month'].value_counts()[most_common_month]
        print("Most common month of travel: {}     Count:{}".format(months[most_common_month-1].title(), count))

    if day == 'all':
        # TO DO: display the most common day of week and it's frequency
        most_common_day = str(df['day_of_week'].mode()[0])
        count = df['day_of_week'].value_counts()[most_common_day]
        print("Most common day of travel: {}      Count:{}".format(most_common_day, count))

    # TO DO: display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common start hour (from 0 to 23) and it's frequency
    most_common_start_hour = df['hour'].mode()[0]
    count = df['hour'].value_counts()[most_common_start_hour]
    print("Most common start hour for travel: {}      Count:{}".format(most_common_start_hour, count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts()[start_station]
    print("Most commonly used start station is: {}      Count:{}".format(start_station, count))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    count = df['End Station'].value_counts()[end_station]
    print("Most commonly used end station is: {}      Count:{}".format(end_station, count))

    # TO DO: display most frequent combination of start station and end station trip
    df['Complete trip'] = df['Start Station']+ '+' +df['End Station']
    most_common_bike_route = df['Complete trip'].mode()[0]
    count = df['Complete trip'].value_counts()[most_common_bike_route]
    print("Most frequent combination of start and end stations: \n{}(Start station) and {}(End station)      Count:{}".format(most_common_bike_route.split('+')[0],most_common_bike_route.split('+')[1], count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    count = df['Trip Duration'].count()
    print("Total travel time: {}      Count:{}".format(total_time, count))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time: {}".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    subscriber_count = df['User Type'].value_counts()['Subscriber']
    customer_count = df['User Type'].value_counts()['Customer']
    print("Subscriber user count: {}     Customer user count: {}".format(subscriber_count, customer_count))

    if city != 'washington':
        # TO DO: Display counts of gender
        male_count = df['Gender'].value_counts()['Male']
        female_count = df['Gender'].value_counts()['Female']
        print("Male user count: {}     Female user count: {}".format(male_count, female_count))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth of users: {} \nMost recent year of birth of users: {} \nMost common year of birth if users: {}".format(earliest_birth_year, recent_birth_year, common_birth_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_stats(df):
    """ Display individual trip data"""
    counter = 0

    display_data = input("Would you like to view individual trip data? Type 'yes' or 'no'\n")
    while display_data.lower().strip() == 'yes':
        df = df[counter:counter+5]
        # get indexes of the dataframe, here assumed all dataframe rows have value for 'Start Station'
        indexes = df.index[df['Start Station'] != ' '].tolist()

        for i in indexes:
            print("\n")
            print(df.loc[i])
        display_data = input("\nWould you like to view MORE individual trip data? Type 'yes' or 'no'\n")
        if display_data.lower().strip() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_trip_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
	main()
