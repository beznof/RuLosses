import re

def validate_format_month(month):
    return bool(re.match(r"^\d{4}\.\d{2}$", month))


def validate_format_day(day):
    return bool(re.match(r"^\d{4}\.\d{2}\.\d{2}$", day))