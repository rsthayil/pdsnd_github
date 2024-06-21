import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    def city_input():
        valid_cities = ['chicago', 'new york city', 'washington']
        while True:
            city = input("Please enter a city name (Chicago, New York City, Washington): ").lower()
            if city in valid_cities:
                return city
            else:
                print("Invalid input. Please enter a valid city name.")

    city = city_input()

    # get user input for month (all, january, february, ... , june)
    def month_input():
        valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        while True:
            month = input("Please enter a month (January, February, ... , June) or 'all' for all months: ").lower()
            if month in valid_months:
                return month
            else:
                print("Invalid input. Please enter a valid month or 'all'.")

    month = month_input()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    def day_input():
        valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            day = input(
                "Please enter a day of the week (Monday, Tuesday, ... , Sunday) or 'all' for all days: ").lower()
            if day in valid_days:
                return day
            else:
                print("Invalid input. Please enter a valid day or 'all'.")

    day = day_input()

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
    # Load data into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month_index = df['month'].mode()[0]
    most_common_month = months[most_common_month_index - 1]
    print('Most common month:', most_common_month)

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_common_day_index = df['day_of_week'].mode()[0]
    most_common_day = days[most_common_day_index - 1]
    print('Most common day of week:', most_common_day)

    # Extract hour from the 'Start Time' column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common End Station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print('Most common trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_seconds = df['Trip Duration'].sum()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("Total travel time is : {} hours, {} minutes, and {} seconds".format(hours, minutes, seconds))

    # display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    mean_minutes, mean_seconds = divmod(mean_seconds, 60)
    print("Mean travel time is : {} minutes, and {} seconds".format(mean_minutes, mean_seconds))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User type counts: \n", user_types)

    # Display counts of gender
    if 'Gender' not in df.columns:
        print("Gender data is not available in the dataset.")
        return

    gender_counts = df['Gender'].value_counts()
    print("Gender counts: \n", gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("Birth Year data is not available in the dataset.")
        return

    earliest_year = int(df['Birth Year'].min())
    print("Earliest birth year:", earliest_year)

    most_recent_year = int(df['Birth Year'].max())
    print("Most recent birth year:", most_recent_year)

    most_common_year = int(df['Birth Year'].mode()[0])
    print("Most common birth year:", most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data_display(df):
    """Displays 5 lines of raw data from the dataframe upon user request."""
    start_loc = 0  # Start at the beginning of the dataframe
    while True:
        show_data = input("Would you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_data == 'yes':
            end_loc = start_loc + 5  # Set the end location for slicing the dataframe
            print(df.iloc[start_loc:end_loc])  # Display the next 5 rows from the dataframe
            start_loc += 5  # Increment the start location for the next slice
            if end_loc > len(df):
                print("You've reached the end of the data.")
                break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
