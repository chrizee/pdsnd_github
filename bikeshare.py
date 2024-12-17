import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = None
    while True:
        city = input("Enter the name of the city you wish to analyse \n").lower()
        if city in CITY_DATA:
            break
        print("pls enter a valid city name (chicago, new york city or washington)\n")
    
    month = None
    while True:
        month = input("Enter the month you wish to analyse\n").lower()
        if month in months:
            break
        print("pls enter a valid month (january, february, march, april, may, june)\n")
    month = months.index(month) + 1
    
    day = None
    while True:
       try:
        day = int(input("Enter the day you wish to analyse as a number. (Monday=0, Sunday=6)\n"))
        if (day < 0 or day > 6):
            print("pls enter a valid day between 0 and 6\n")
        else: 
            break
       except:
        print("pls enter a valid day between 0 and 6 exception\n")
        
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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename, parse_dates=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    
    df = df[df['month'] == month]
    df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    month = df['month'].mode()[0]
    month_name = months[month - 1]
    print(f"The most common month is {month_name}")


    day = df['day_of_week'].mode()[0]
    day_name = days[day]
    print(f"The most common day is {day_name}")


    hour = df['hour'].mode()[0]
    print(f"The most common hour is {hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station is {start_station}")

    end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station is {end_station}")

    start_end = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print(f"Most frequent combination of start and end station is {start_end}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f'Total travel time is {total_travel_time}')
    
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Meanno travel time is {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)
    print('\n')
    
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    except:
        pass

    
    try:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print(f"The earliest birth year is {earliest}\n")
        print(f"The most recent birth year is {recent}\n")
        print(f"The most common birth year is {common}\n")    
    except:
        pass
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data. This displays 5 at a time and asks the user if they want to see more."""

    cnt = len(df)       
    response = input(f'Would you like to see raw data? There are {cnt} raw data. Enter yes or no.\n')
    index = 0
    while response.lower() == 'yes':
        last = index + 5
        if last >= cnt:
            last = cnt
        data = df[index:last]
        index += 5
        print(data)
        if last == cnt:
            print('That is all the raw data we have. Exiting')
            break
        response = input('Would you like to see more raw data? Enter yes or no.\n')
        
       
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
