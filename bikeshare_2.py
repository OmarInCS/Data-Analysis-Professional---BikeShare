import time
import pandas as pd
import numpy as np
from datetime import datetime


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ("All", "January", "February", "March", "April", "May", "June", "July", "August", 
                   "September", "October", "November", "December")

days_list = ("All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


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
    city = input("[+] Enter a city (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:
        print("[-] Invalid input, try again")
        city = input("[+] Enter a city (chicago, new york city, washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    
    
    month = input("[+] Enter a month (all, january, february, ... , june): ").capitalize()
    while month not in months_list:
        print("[-] Invalid input, try again")
        month = input("[+] Enter a month (all, january, february, ... , june): ").capitalize()
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input("[+] Enter a day (all, Monday, Tuesday, ... , Sunday): ").capitalize()
    while day not in days_list:
        print("[-] Invalid input, try again")
        day = input("[+] Enter a day (all, Monday, Tuesday, ... , Sunday): ").capitalize()


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
    
    df = pd.read_csv(CITY_DATA[city])
    df = df.iloc[:,1:] # remove first column
    df["Start Time"] = df["Start Time"].apply(lambda st: datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
    df["End Time"] = df["End Time"].apply(lambda st: datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))
    

    
    if month != "All":
        month = months_list.index(month)
        condition = df["Start Time"].apply(lambda st: st.month == month)
        df = df[condition]
        
    if day != "All":
        condition = df["Start Time"].apply(lambda st: st.strftime("%A") == day)
        df = df[condition]
     

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df["Start Time"].apply(lambda st: st.strftime("%B")).mode()[0]
    print(f"[+] Most common month: {month}")


    # display the most common day of week
    day = df["Start Time"].apply(lambda st: st.strftime("%A")).mode()[0]
    print(f"[+] Most common day of week: {day}")


    # display the most common start hour
    hour = df["Start Time"].apply(lambda st: st.strftime("%H")).mode()[0]
    print(f"[+] Most common start hour: {hour}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station = df["Start Station"].mode()[0]
    print(f"[+] Most commonly used start station: {station}")


    # display most commonly used end station
    station = df["End Station"].mode()[0]
    print(f"[+] Most commonly used end station: {station}")


    # display most frequent combination of start station and end station trip
    path = df[["Start Station", "End Station"]].mode()
    print(f"[+] Most frequent combination of start station and end station trip:")
    print(f"\t[*] Start: {path['Start Station'][0]},\n\t[*] End: {path['End Station'][0]}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_minutes, total_seconds = divmod(df["Trip Duration"].mean(), 60)
    print(f"[+] Mean travel time: {total_minutes} min {total_seconds:.2f} sec")


    # display mean travel time
    total_minutes, total_seconds = divmod(df["Trip Duration"].sum(), 60)
    total_hours, total_minutes = divmod(total_minutes, 60)
    total_days, total_hours = divmod(total_hours, 24)
    print(f"[+] Total travel time: {total_days} days {total_hours}:{total_minutes}:{total_seconds}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types_count = df["User Type"].value_counts()
    print("[+] Counts of user types:")
    for i, count in enumerate(types_count):
        print(f"\t[{i+1}] {types_count.index[i]:20s}: {count}")


    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print("\n[+] Counts of gender:")
        for i, count in enumerate(gender_count):
            print(f"\t[{i+1}] {gender_count.index[i]:20s}: {count}")



    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df["Birth Year"].min()
        recent_year = df["Birth Year"].max()
        common_year = df["Birth Year"].mode()[0]
        
        print("\n[+] Earliest year of birth:\t", int(earliest_year))
        print("[+] Most recent year of birth:\t", int(recent_year))
        print("[+] Most common year of birth:\t", int(common_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays bikesshare data 5 rows by 5 rows upon user request."""
    
    choice = input("[+] do you want to see raw data? (yes or no): ")
    start_idx = 0
    
    while choice != "no":
        if choice == "yes":
            end_idx = start_idx + 5
            print(df[start_idx:end_idx])
            start_idx = end_idx
            choice = input("[+] do you want to see more 5 lines of raw data? (yes or no): ")
        else:
            print("[-] Invalid Input")
            choice = input("[+] do you want to see raw data? (yes or no): ")
            


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
