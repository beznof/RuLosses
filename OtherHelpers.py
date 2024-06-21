from datetime import datetime
import pytz


def datetime_formatted_in_kyiv():
    kyiv_timezone = pytz.timezone('Europe/Kyiv')
    kyiv_now = datetime.now(tz=kyiv_timezone)
    kyiv_formatted = kyiv_now.strftime('%B %d, %Y')
    return kyiv_formatted


def datetime_in_kyiv():
    kyiv_timezone = pytz.timezone('Europe/Kyiv')
    kyiv_now = datetime.now(tz=kyiv_timezone)
    kyiv_formatted = kyiv_now.strftime('%Y.%m.%d')
    return kyiv_formatted

def format_monthly_date(date):
    date_object = datetime.strptime(date,'%Y.%m')
    date_formatted = date_object.strftime('%B %Y')
    return date_formatted

def format_daily_date(date):
    date_object = datetime.strptime(date,'%Y.%m.%d')
    date_formatted = date_object.strftime('%B %d, %Y')
    return date_formatted