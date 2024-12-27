from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_period_to_dates(time_period):
    """
    Converts a time period string (e.g., '3y', '2m', '1w') into 
    starting and ending dates using the dateutil library.

    Args:
        time_period: A string representing the time period. 
                     Supported units: 'y' (years), 'm' (months), 'w' (weeks), 'd' (days).

    Returns:
        A tuple containing the starting and ending dates as datetime objects.
        Returns None if the input format is invalid.
    """

    if not time_period or not isinstance(time_period, str):
        return None

    try:
        value = int(time_period[:-1])
        unit = time_period[-1]
    except (ValueError, IndexError):
        return None

    today = datetime.now()

    if unit == 'y':
        delta = relativedelta(years=value)
    elif unit == 'm':
        delta = relativedelta(months=value)
    elif unit == 'w':
        delta = relativedelta(weeks=value)
    elif unit == 'd':
        delta = relativedelta(days=value)
    else:
        return None

    end_date = today - delta
    return end_date, today

if __name__ == "__main__":
    time_period = "55d"
    starting_date, ending_date = time_period_to_dates(time_period)
    print("Time period set to ", time_period)
    print("Starting date: ", starting_date)
    print("Ending date: ", ending_date)