import requests
import logging

DAILY_URL = "https://russian-casualties.in.ua/api/v1/data/json/daily"
MONTHLY_URL = "https://russian-casualties.in.ua/api/v1/data/json/monthly"


def retrieve_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed")
        return None
    except ValueError as e:
        logging.error(f"Failed to parse JSON from {url}")
        return None


def find_total_count():
    days_table = retrieve_data(DAILY_URL)

    if not days_table:
        logging.error("Failed to retrieve JSON from the API")
        return -1

    days = days_table['data']

    if not days:
        logging.error("Failed to retrieve the data")
        return -1

    total_count = 0
    for day, counts in days.items():
        if "personnel" in counts:
            total_count += counts.get('personnel', 0)

    return total_count


def monthly_stats(month):
    function_name = "monthly_stats(month)"

    months_table = retrieve_data(MONTHLY_URL)

    if not months_table:
        logging.error(f"Failed to retrieve the JSON file from the API in {function_name}")
        return None, "Oops! Looks like something went wrong..."

    months = months_table['data']

    if not months:
        logging.error(f"Failed to retrieve data from the JSON file in {function_name}")
        return None, "Oops! Looks like something went wrong..."

    if month not in months:
        logging.error(f"Failed to find the specified date in {function_name}")
        return None, "Oops! It looks like there's no data available for the date you have entered."

    sought_month = months[month]

    return sought_month, None


def daily_stats(day):
    function_name = "daily_stats(day)"

    days_table = retrieve_data(DAILY_URL)

    if not days_table:
        logging.error(f"Failed to retrieve the JSON file from the API in {function_name}")
        return None, "Oops! Looks like something went wrong..."

    days = days_table['data']

    if not days:
        logging.error(f"Failed to retrieve data from the JSON file in {function_name}")
        return None, "Oops! Looks like something went wrong..."

    if day not in days:
        logging.error(f"Failed to find the specified date in {function_name}")
        return None, "Oops! It looks like there's no data available for the date you have entered."

    sought_day = days[day]

    return sought_day, None


def today_stats():
    days_table = retrieve_data(DAILY_URL)

    if not days_table:
        logging.error("Failed to access the API")
        return None

    days = days_table['data']

    if not days:
        logging.error("Failed to retrieve the data")
        return None

    summed_data = {key: 0 for key in days['2022.02.24']}
    new_data = {key: 0 for key in days['2022.02.24']}

    for day, values in days.items():
        for key, value in values.items():
            if key in summed_data:
                summed_data[key] += value

    last_day = list(days.keys())[-1]
    last_day_data = days[last_day]
    for key, value in last_day_data.items():
        new_data[key] += value

    return summed_data, new_data

