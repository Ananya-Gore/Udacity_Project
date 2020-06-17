import time
import pandas as pd
import numpy as np
from statistics import mode

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# choice class is defined to include the data from the user in the form of choices to laid him towards required data
def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return choice

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nEnter the name of city from chicago, new york city, washington to explore bike share data\n:").lower()

    while city.lower() not in ['chicago', 'new york city', 'washington']:
        city = input( "Entered invalid city name, please enter a valid city name\n:").lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter the name of month from January, February, March, April, May and June\n:").lower()

    while month.lower() not in ['january','february','march','april','may','june']:
        month = input('Entered month is invalid, please enter a valid month\n:').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the Days from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday\n:").lower()

    while day.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = input('Entered day is invalid, please enter a valid day\n:').lower()

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
    # convert  start time column to datetime column
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #  create new columns from start time column by extracting month and days of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    #filter by day of week
    if day !=  'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month: {}'.format(popular_month))

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day: {}'.format(popular_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = mode(df['hour'])
    print('Most common Start hour: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('Most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['trip_combination'] = df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most frequent start and end station is : {}\n'.format(df['trip_combination'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Trip duration stats will display the total time of travel as well as mean travel time
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df['Trip Duration'].sum()
    print('\nTotal Travel time : {}'.format(total))


    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()
    print('\nMean Travel time : {}'.format(mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_total = df['User Type'].value_counts()
    print('\nCount of user by types:\n{} '.format(user_types_total))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCount of gender by categories:\n{} '.format(gender_counts))


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest Year:', Earliest_Year)
        recent_Year = df['Birth Year'].max()
        print('\nRecent Year:', recent_Year)
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year Of Birth:', Most_Common_Year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    
    raw_data_view = input('To view the raw data, Enter y : yes or n : no \n>')
    raw_data_view.lower()

    if raw_data_view == 'y':
    
        # sort data by column
        if mark_place == 0:
            sort_df = choice("\nHow would you like to sort the way the data is "
                             "displayed in the dataframe? Hit Enter to view "
                             "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                             "[td] Trip Duration\n [ss] Start Station\n "
                             "[es] End Station\n\n>",
                             ('st', 'et', 'td', 'ss', 'es', ''))

            asc_or_desc = choice("\nWould you like it to be sorted ascending or "
                                 "descending? \n [a] Ascending\n [d] Descending"
                                 "\n\n>",
                                 ('a', 'd'))

            if asc_or_desc == 'a':
                asc_or_desc = True
            elif asc_or_desc == 'd':
                asc_or_desc = False

            if sort_df == 'st':
                df = df.sort_values(['Start Time'], ascending=asc_or_desc)
            elif sort_df == 'et':
                df = df.sort_values(['End Time'], ascending=asc_or_desc)
            elif sort_df == 'td':
                df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
            elif sort_df == 'ss':
                df = df.sort_values(['Start Station'], ascending=asc_or_desc)
            elif sort_df == 'es':
                df = df.sort_values(['End Station'], ascending=asc_or_desc)
            elif sort_df == '':
                pass

        # each loop displays 5 lines of raw data
        while True:
            for i in range(mark_place, len(df.index)):
                print("\n")
                print(df.iloc[mark_place:mark_place+5].to_string())
                print("\n")
                mark_place += 5

                if choice("Do you want to keep printing raw data?"
                          "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                    continue
                else:
                    print("\nThanks for viewing the Raw data !!!")
                    break
            break

    return mark_place
     
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        mark_place=0
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        mark_place = raw_data(df, mark_place)

        restart = input('\nWould you like to restart? Enter y : yes or n : no.\n>')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
