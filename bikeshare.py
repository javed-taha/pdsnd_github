import time
import os
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

VALID_MONTHS = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
]

VALID_DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

SEPARATORS = {
    "sep1": "=" * 100,
    "sep2": "-" * 100,
    "sep3": "*" * 100,
}

ALL_OPTION = "all"
DATETIME_COLUMNS = ["Start Time", "End Time"]


def get_valid_input(prompt, valid_options, allow_all=True):
    """Get and validate user input.

    Args:
        prompt (str): The input prompt message to display to the user.
        valid_options (list[str]): A list of valid input options.
        allow_all (bool): Whether to allow 'all' as a valid input. Defaults to True.

    Returns:
        str: The validated user input.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in [valid_option.lower() for valid_option in valid_options]:
            return user_input
        if allow_all and (user_input == "" or user_input == ALL_OPTION):
            return ALL_OPTION
        print("Invalid input. Please try again.\n")


def get_filters():
    """Ask users to specify a city, month, and day to analyze.

    This function prompts the user to input a city, month, and day for data analysis.
    It validates the input against predefined lists of valid options.

    Returns:
        tuple[str, str, str]: A tuple containing:
            - city (str): Name of the city to analyze.
            - month (str): Name of the month to filter by, or "all" for no month filter.
            - day (str): Name of the day of week to filter by, or "all" for no day filter.
    """
    print("Hello! Let's explore some US bike share data!")
    print(SEPARATORS["sep3"], "\n")

    city = get_valid_input(
        prompt="Which city do you want to analyze?\n"
        f"Select from these cities only -> {', '.join(CITY_DATA.keys())}: ",
        valid_options=list(CITY_DATA.keys()),
        allow_all=False,
    )
    print(SEPARATORS["sep2"], "\n")

    month = get_valid_input(
        prompt="Which month do you want to filter by? Valid months are from "
        f"{VALID_MONTHS[0].title()} to {VALID_MONTHS[-1].title()}.\n"
        "Press Enter or type 'all' for the entire dataset, or provide a valid month: ",
        valid_options=VALID_MONTHS,
    )
    print(SEPARATORS["sep2"], "\n")

    day = get_valid_input(
        prompt="Which day do you want to filter by? Valid days are from "
        f"{VALID_DAYS[0].title()} to {VALID_DAYS[-1].title()}.\n"
        "Press Enter or type 'all' for the entire dataset, or provide a valid day: ",
        valid_options=VALID_DAYS,
    )
    print(SEPARATORS["sep1"])

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): The name of the city to analyze.
        month (str): Name of the month to filter dataset by, or "all" for no filter.
        day (str): Name of the day of week to filter dataset by, or "all" for no filter.

    Returns:
        pd.DataFrame: DataFrame containing city data filtered by month and day.

    Raises:
        FileNotFoundError: If the CSV file for the specified city is not found.
        ValueError: If an invalid city, month, or day name is provided.
    """
    filename = ""
    try:
        # Construct the file path
        filename = os.path.join("./data/", CITY_DATA[city.lower()])
        # Read the CSV file with specified date columns and index column
        df = pd.read_csv(filename, parse_dates=DATETIME_COLUMNS, index_col="Unnamed: 0")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filename}") from e
    except KeyError:
        raise ValueError(f"Invalid city name: {city}")
    except ValueError as e:
        if 'Missing column provided to "parse_dates"' in str(e):
            raise ValueError("Required column(s) missing in the CSV file.") from e
        else:
            raise
    except Exception as e:
        # Handle any other exception that may arise due to index_col
        if "Unnamed: 0" in str(e):
            raise ValueError(
                "Error with the specified index column 'Unnamed: 0'."
            ) from e
        else:
            raise

    # Add derived columns for month, day name, and trip description
    df["Month"] = df["Start Time"].dt.month_name()
    df["Day Name"] = df["Start Time"].dt.day_name()
    df["Trip"] = (
        df["Start Station"].astype(str).fillna("No Start Station")
        + " to "
        + df["End Station"].astype(str).fillna("No End Station")
    )

    def filter_by_period(df_input, col_name, period_name, period_input, valid_periods):
        """
        Filters the DataFrame by a specified period (month or day).

        Args:
            df_input (pd.DataFrame): Input DataFrame to be filtered.
            col_name (str): Column name in DataFrame to filter by.
            period_name (str): Name of the period (e.g., "month", "day").
            period_input (str): User-provided period value to filter by.
            valid_periods (list): List of valid period values.

        Returns:
            pd.DataFrame: Filtered DataFrame.

        Raises:
            ValueError: If the provided period value is invalid.
        """
        period_input = period_input.strip().lower()
        # Filter by period if applicable
        if period_input != ALL_OPTION:
            if period_input not in valid_periods:
                raise ValueError(f"Invalid {period_name}: {period_input}")
            df_output = df_input[df_input[col_name] == period_input.title()]
            return df_output
        else:
            return df_input

    # Filter the DataFrame by month and day
    df = filter_by_period(df, "Month", "month", month, VALID_MONTHS)
    df = filter_by_period(df, "Day Name", "day", day, VALID_DAYS)

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    This function calculates and prints the most common month, day of the week,
    and start hour for bike trips based on the provided DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing bike trip data.

    Raises:
        AttributeError: If expected columns are missing from the DataFrame.
        IndexError: If the DataFrame is empty or mode calculation fails.
    """
    start_time = time.time()
    print("\nCalculating the Most Frequent Times of Travel...")
    print(SEPARATORS["sep2"])

    try:
        # Calculate stats
        most_common_month = df["Month"].mode().iat[0]
        most_common_dow = df["Day Name"].mode().iat[0]
        most_common_start_hr = df["Start Time"].dt.hour.mode().iat[0]

        # Display most common period stats
        print(f"The most common month is {most_common_month}.")
        print(f"The most common day of week is {most_common_dow}.")
        print(f"The most common start hour is {most_common_start_hr}.")

    except (AttributeError, IndexError) as e:
        print(f"Error calculating time stats: {e}")

    finally:
        # Performance of function stats
        print(f"\nThis took {time.time() - start_time} seconds to run.")
        print(SEPARATORS["sep1"])


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    This function calculates and prints the most common start station,
    end station, and the most frequent trip (combination of start and end station).

    Args:
        df (pd.DataFrame): A DataFrame containing bike trip data.

    Raises:
        AttributeError: If expected columns are missing from the DataFrame.
        IndexError: If the DataFrame is empty or mode calculation fails.
    """
    start_time = time.time()
    print("\nCalculating the Most Popular Stations and Trip...")
    print(SEPARATORS["sep2"])

    try:
        # Calculate stats
        most_common_start_station = df["Start Station"].mode().iat[0]
        most_common_end_station = df["End Station"].mode().iat[0]
        most_frequent_trip = df["Trip"].mode().iat[0]

        # Display the most popular stations and trip
        print(f"The most commonly used start station is {most_common_start_station}.")
        print(f"The most commonly used end station is {most_common_end_station}.")
        print(f"The most frequent trip is {most_frequent_trip}.")

    except (AttributeError, IndexError) as e:
        print(f"Error calculating station stats: {e}")

    finally:
        # Performance of function stats
        print(f"\nThis took {time.time() - start_time} seconds to run.")
        print(SEPARATORS["sep1"])


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    This function calculates and prints the total travel time and mean travel time
    for all trips in the DataFrame. It uses numpy for calculations and a custom
    function to format the duration into a human-readable string.

    Args:
        df (pd.DataFrame): A DataFrame containing bike trip data.

    Raises:
        AttributeError: If the 'Trip Duration' column is missing from the DataFrame.
        IndexError: If the DataFrame is empty.
    """
    start_time = time.time()  # Record the start time of the function
    print("\nCalculating Trip Duration...")
    print(SEPARATORS["sep2"])

    def format_duration(seconds):
        """
        Converts a duration from seconds into a human-readable string.

        Args:
            seconds (float): Duration in seconds.

        Returns:
            str: Duration formatted as a human-readable string.
                - e.g., '1 day 2 hours 3 minutes 4 seconds'.
        """
        days = int(seconds // 86400)  # Calculate the number of days
        hours = int((seconds % 86400) // 3600)  # Calculate the number of hours
        minutes = int((seconds % 3600) // 60)  # Calculate the number of minutes
        seconds = int(round(seconds % 60))  # Calculate the remaining seconds

        duration = []  # Initialize an empty list to store duration components
        if days > 0:
            duration.append(f"{days} days")
        if hours > 0:
            duration.append(f"{hours} hours")
        if minutes > 0:
            duration.append(f"{minutes} minutes")
        # Display seconds if there are any or if no other units are available
        if seconds > 0 or not duration:
            duration.append(f"{seconds} seconds")

        return " ".join(duration)  # Join the duration components into a single string

    try:
        # Calculate statistics using numpy
        trip_durations = df["Trip Duration"].values  # Extract the trip duration values
        total_travel_time_seconds = float(
            np.sum(trip_durations)
        )  # Calculate total travel time
        mean_travel_time_seconds = float(
            np.mean(trip_durations)
        )  # Calculate mean travel time

        # Get formatted duration text
        total_travel_time_fmt = format_duration(
            total_travel_time_seconds
        )  # Format total travel time
        mean_travel_time_fmt = format_duration(
            mean_travel_time_seconds
        )  # Format mean travel time

        # Display the total and mean travel time
        print(f"The total travel time is {total_travel_time_fmt}.")
        print(f"The mean travel time is {mean_travel_time_fmt}.")

    except (AttributeError, IndexError) as e:
        # Handle exceptions and print an error message
        print(f"Error calculating trip duration stats: {e}")

    finally:
        # Print the time taken to run the function
        print(f"\nThis took {time.time() - start_time} seconds to run.")
        print(SEPARATORS["sep1"])


def user_stats(df):
    """
    Displays statistics on bike share users.

    This function calculates and prints various user statistics including:
    - Count of user types (if data available)
    - Count of genders (if data available)
    - Earliest, most recent, and most common birth year (if data available)

    The function handles potential missing columns and invalid data gracefully.

    Args:
        df (pd.DataFrame): A DataFrame containing bike trip data.

    Raises:
        AttributeError: If expected columns are missing from the DataFrame.
        IndexError: If the DataFrame is empty or calculations fail.
        ValueError: If birth year data contains invalid values.
    """
    start_time = time.time()
    print("\nCalculating Users Stats...")
    print(SEPARATORS["sep2"])

    try:
        # Calculate and Display User Stats
        if "User Type" in df.columns:
            user_type_counts = df["User Type"].value_counts()
            print(f"User Counts:\n{user_type_counts}\n")
        if "Gender" in df.columns:
            gender_counts = df["Gender"].value_counts()
            print(f"Gender Counts:\n{gender_counts}\n")
        if "Birth Year" in df.columns:
            birth_years = df["Birth Year"].dropna().values  # Remove NaN values

            try:
                earliest_birth_year = int(np.nanmin(birth_years))
                most_recent_birth_year = int(np.nanmax(birth_years))
                most_common_birth_year = int(df["Birth Year"].mode().iat[0])

                print(f"Earliest birth year: {earliest_birth_year}")
                print(f"Most recent birth year: {most_recent_birth_year}")
                print(f"Most common birth year: {most_common_birth_year}\n")
            except ValueError as ve:
                print(f"Error processing birth years: {ve}")
                print("Birth year data may contain invalid values.\n")

    except (AttributeError, IndexError) as e:
        print(f"Error calculating user stats: {e}")

    finally:
        # Performance of function stats
        print(f"\nThis took {time.time() - start_time} seconds to run.")
        print(SEPARATORS["sep1"])


def get_user_input(prompt, valid_responses):
    """
    Get and validate user input.

    This function prompts the user for input and validates it against a list of
    valid responses. It continues to prompt until a valid response is received.

    Args:
        prompt (str): The prompt to display to the user.
        valid_responses (list[str]): A list of valid responses to choose from.

    Returns:
        str: The validated user input string.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return response
        else:
            print(f"Invalid input. Please enter one of: {', '.join(valid_responses)}")


def wait_for_user():
    """
    Pause execution until the user presses Enter.

    This function displays a prompt and waits for the user to press Enter
    before allowing the program to continue execution.
    """
    input("\nPress Enter to continue...")


def display_raw_data(df):
    """
    Display 5 lines of raw data at a time based on user input.

    This function iteratively displays 5 rows of the DataFrame at a time,
    prompting the user after each display to continue or stop.

    Args:
        df (pd.DataFrame): The filtered dataframe containing bike share data.
    """
    row_index = 0
    while True:
        msg = "\nWould you like to see 5 lines of raw data? (y/n): "
        display_choice = get_user_input(prompt=msg, valid_responses=["y", "n"])

        if display_choice == "n":
            break

        print(df.iloc[row_index : row_index + 5].to_string())
        row_index += 5

        if row_index >= df.shape[0]:
            print("\nNo more data to display.")
            break


def user_action_menu(df):
    """
    Allow the user to choose an action to perform on the bike share data.

    This function presents a menu of analysis options to the user, including
    viewing raw data. It repeatedly prompts for user input and executes the
    chosen action until the user chooses to exit.

    Args:
        df (pd.DataFrame): A pandas dataframe containing the bike share data.
    """
    stats_funcs = [
        time_stats,
        station_stats,
        trip_duration_stats,
        user_stats,
    ]

    while True:
        print("\nAvailable actions:")
        for index, stats_func in enumerate(stats_funcs, 1):
            print(f"{index}. {stats_func.__name__.replace('_', ' ').title()}")
        raw_data_choice = len(stats_funcs) + 1
        exit_choice = len(stats_funcs) + 2
        print(f"{raw_data_choice}. View Raw Data")
        print(f"{exit_choice}. Exit")
        valid_choices = [str(i) for i in range(1, exit_choice + 1)]

        choice = get_user_input(
            f"\nChoose an analysis to run (1 to {len(stats_funcs)}) or"
            f" '{raw_data_choice}' to display raw data.\n"
            f"Press '{exit_choice}' to exit to the main program.\n"
            "Please enter your choice: ",
            valid_responses=valid_choices,
        )

        if choice == str(exit_choice):
            print("\nExiting analysis section. Going back to main program.")
            break
        elif choice == str(raw_data_choice):
            display_raw_data(df)
        else:
            # Call appropriate analysis function from stats_funcs list
            stats_funcs[int(choice) - 1](df)

            # Wait for user to review the stats
            wait_for_user()


def main():
    """
    Main function to run the bike share data analysis program.

    This function orchestrates the entire program flow. It repeatedly:
    1. Prompts for and gets filter criteria from the user.
    2. Loads and filters the data based on user input.
    3. Presents the user action menu for data analysis.
    4. Asks if the user wants to restart with new filters.

    The function handles exceptions and allows the user to restart or exit
    the program in case of errors.

    Raises:
        Exception: Any unexpected error that occurs during program execution.
    """
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            user_action_menu(df)

            if (
                get_user_input(
                    "\nDo you want to restart with new filters? (y/n): ", ["y", "n"]
                )
                == "n"
            ):
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            if (
                get_user_input(
                    "\nDo you want to restart the program? (y/n): ", ["y", "n"]
                )
                == "n"
            ):
                break

        print("\nRestarting the analysis with new filters. Please wait...")
        print(SEPARATORS["sep1"], "\n")

    # Once While loop is terminated this signals the end of the program
    exit_msg = (
        "\nExiting the program. Thank you for using the bike share data "
        "analysis program! Come back soon =)"
    )
    print(exit_msg)
    print(SEPARATORS["sep3"])


if __name__ == "__main__":
    main()
