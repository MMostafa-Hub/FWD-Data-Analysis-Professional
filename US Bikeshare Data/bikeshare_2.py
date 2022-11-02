import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = [
    "JAN", "FEB", "MAR", "APRIL", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
    "NOV", "DEC"
]

DAYS = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']


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
    while True:
        city = input(f"Enter the city name in {tuple(CITY_DATA.keys())}\n").strip().lower()
        if city in CITY_DATA.keys(): break
        print("Please enter a valid city name")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(f"Enter the month in {tuple(MONTHS)} or all\n").strip().upper()
        if month in MONTHS or month == "ALL": break
        print("Please enter a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(f"Enter the day in {tuple(DAYS)} or all\n").strip().upper()
        if day in DAYS or day == "ALL": break
        print("Please enter a valid day")

    print('-' * 40, )
    print(f"You Picked {city}, {month}, {day}")
    print('-' * 40, )

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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.day
    
    df = df[df["day"] == DAYS.index(day) + 1] if day != "ALL" else df
    df = df[df["month"] == MONTHS.index(month) + 1] if month != "ALL" else df
    return df.drop(["month", "day"], axis=1)


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("the most common month: ",
          MONTHS[df["Start Time"].dt.month.value_counts().idxmax()])

    # display the most common day of week
    print("the most common day of week: ",
          DAYS[df["Start Time"].dt.day.value_counts().idxmax() % 7])

    # display the most common start hour
    print("the most common hour: ",
          df["Start Time"].dt.hour.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("the most commonly used start station: ",
          df["Start Station"].value_counts().idxmax())

    # display most commonly used end station
    print("the most commonly used end station: ",
          df["End Station"].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print(
        "the most frequent combination of start station and end station trip: ",
        pd.value_counts(df[["Start Station", "End Station"]].values.flatten()).idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["Trip Duration"] = pd.to_datetime(df["End Time"]) - pd.to_datetime(
        df["Start Time"])

    # display total travel time
    print("total travel time: ", df["Trip Duration"].sum())

    # display mean travel time
    print("mean travel time: ", df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if "User Type" in df.columns:    
        print("counts of user types:\n", df["User Type"].value_counts(), sep="")

    # Display counts of gender
    if "Gender" in df.columns:
        print("counts of gender:\n", df["Gender"].value_counts(), sep="")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("Year of birth stats: ")
        print("\tearliest: {}\n\tmost recent: {},\n\tmost common: {}".format(
            df["Birth Year"].min(), df["Birth Year"].max(),
            df["Birth Year"].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
