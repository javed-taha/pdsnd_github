import time
import os
import pandas as pd
import numpy as np
from typing import Callable

CITY_DATA: dict[str, str] = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

VALID_MONTHS: list[str] = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
]

VALID_DAYS: list[str] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

SEPARATORS: dict[str, str] = {
    "sep1": "=" * 100,
    "sep2": "-" * 100,
    "sep3": "*" * 100,
}

ALL_OPTION = "all"
DATETIME_COLUMNS = ["Start Time", "End Time"]


def get_valid_input(
    prompt: str, valid_options: list[str], allow_all: bool = True
) -> str:
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


def get_filters() -> tuple[str, str, str]:
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


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
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
        filename = os.path.join("./data/", CITY_DATA[city.lower()])
        df = pd.read_csv(filename, parse_dates=DATETIME_COLUMNS, index_col=0)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filename}") from e
    except KeyError:
        raise ValueError(f"Invalid city name: {city}")
    except ValueError as e:
        if 'Missing column provided to "parse_dates"' in str(e):
            raise ValueError("Required column(s) missing in the CSV file.") from e
        else:
            raise

    # Derived columns
    df["Month"] = df["Start Time"].dt.month_name()
    df["Day Name"] = df["Start Time"].dt.day_name()
    df["Trip"] = (
        df["Start Station"].astype(str).fillna("No Start Station")
        + " to "
        + df["End Station"].astype(str).fillna("No End Station")
    )

    def filter_by_period(
        df_input: pd.DataFrame,
        col_name: str,
        period_name: str,
        period_input: str,
        valid_periods: list[str],
    ) -> pd.DataFrame:
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
            df_output = df_input
            return df_output

    df = filter_by_period(df, "Month", "month", month, VALID_MONTHS)
    df = filter_by_period(df, "Day Name", "day", day, VALID_DAYS)

    return df


def time_stats(df: pd.DataFrame) -> None:
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
    print("\nCalculating the Most Frequent Times of Travel...")
    print(SEPARATORS["sep2"])
    start_time = time.time()

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
        print("\nThis took {} seconds.".format(time.time() - start_time))
        print(SEPARATORS["sep1"])


def station_stats(df: pd.DataFrame) -> None:
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
    print("\nCalculating the Most Popular Stations and Trip...")
    print(SEPARATORS["sep2"])
    start_time = time.time()

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
        print("\nThis took {} seconds.".format(time.time() - start_time))
        print(SEPARATORS["sep1"])


def trip_duration_stats(df: pd.DataFrame) -> None:
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
    print("\nCalculating Trip Duration...")
    print(SEPARATORS["sep2"])
    start_time = time.time()

    def format_duration(seconds: float) -> str:
        """
        Converts a duration from seconds into a human-readable string.

        Args:
            seconds (float): Duration in seconds.

        Returns:
            str: Duration formatted as a human-readable string
                - e.g., '1 day 2 hours 3 minutes 4 seconds'.
        """
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(round(seconds % 60))

        duration = []
        if days > 0:
            duration.append(f"{days} days")
        if hours > 0:
            duration.append(f"{hours} hours")
        if minutes > 0:
            duration.append(f"{minutes} minutes")
        # Displays seconds only if it's the only unit available
        if seconds > 0 or not duration:
            duration.append(f"{seconds} seconds")

        return " ".join(duration)

    try:
        # Calculate stats
        # Calculate stats using numpy
        trip_durations = df["Trip Duration"].values
        total_travel_time_seconds = float(np.sum(trip_durations))
        mean_travel_time_seconds = float(np.mean(trip_durations))

        total_travel_time_fmt = format_duration(total_travel_time_seconds)
        mean_travel_time_fmt = format_duration(mean_travel_time_seconds)

        # Display the total and mean travel time
        print(f"The total travel time is {total_travel_time_fmt}.")
        print(f"The mean travel time is {mean_travel_time_fmt}.")

    except (AttributeError, IndexError) as e:
        print(f"Error calculating trip duration stats: {e}")

    finally:
        # Performance of function stats
        print("\nThis took {} seconds.".format(time.time() - start_time))
        print(SEPARATORS["sep1"])


def user_stats(df: pd.DataFrame) -> None:
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
    print("\nCalculating Users Stats...")
    print(SEPARATORS["sep2"])
    start_time = time.time()

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
        print(f"This took {time.time() - start_time} seconds.")
        print(SEPARATORS["sep1"])


def get_user_input(prompt: str, valid_responses: list[str]) -> str:
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


def wait_for_user() -> None:
    """
    Pause execution until the user presses Enter.

    This function displays a prompt and waits for the user to press Enter
    before allowing the program to continue execution.
    """
    input("\nPress Enter to continue...")


def display_raw_data(df: pd.DataFrame) -> None:
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


def user_action_menu(df: pd.DataFrame) -> None:
    """
    Allow the user to choose an action to perform on the bike share data.

    This function presents a menu of analysis options to the user, including
    viewing raw data. It repeatedly prompts for user input and executes the
    chosen action until the user chooses to exit.

    Args:
        df (pd.DataFrame): A pandas dataframe containing the bike share data.
    """
    stat_function = Callable[[pd.DataFrame], None]
    stats_funcs: list[stat_function] = [
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


def main() -> None:
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
