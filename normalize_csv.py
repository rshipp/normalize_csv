#!/usr/bin/env python3
"""Normalize CSVs in the expected format.

Usage:

    ./normalize_csv.py < FILENAME
"""

import io
import sys
import csv
import datetime


import pytz


# Time conversion.
MILLI_TO_MICRO = 1000


def normalize_duration(duration):
    """Convert HH:MM:SS.ms duration to floating point seconds.

    :param str duration: HH:MM:SS.ms representation of a time duration.
    :returns: Floating point representation of total duration (seconds.ms).
    :rtype: float
    """
    hours, minutes, seconds = duration.split(':')
    seconds, milliseconds = seconds.split('.')
    return datetime.timedelta(hours=int(hours), minutes=int(minutes),
                              seconds=int(seconds),
                              microseconds=int(milliseconds)*MILLI_TO_MICRO
                              ).total_seconds()


def normalize_row(row):
    """Parse cell values and return normalized results.

    :param dict row: Input data in {'ColumnName': 'value'} format.
    :returns: Normalized output row.
    :rtype: list
    """
    # Timestamp
    # Convert from US/Pacific time to US/Eastern and format as ISO-8601.
    timestamp = datetime.datetime.strptime(row['Timestamp'],
                                           '%m/%d/%y %I:%M:%S %p')
    pacific_timestamp = pytz.timezone('US/Pacific').localize(timestamp)
    eastern_isoformat = pacific_timestamp.astimezone(
        pytz.timezone('US/Eastern')).isoformat()

    # Address
    address = row['Address']

    # ZIP
    # Format as 5 digits, padding the left with 0 as needed.
    # Note: This does not validate that the length of zip is exactly 5.
    zip_code = row['ZIP'].zfill(5)

    # FullName
    # Convert to uppercase.
    full_name = row['FullName'].upper()

    # FooDuration
    # Convert duration from HH:MM:SS.MS to a floating point seconds format.
    foo_duration = normalize_duration(row['FooDuration'])

    # BarDuration
    bar_duration = normalize_duration(row['BarDuration'])

    # TotalDuration
    # Sum of FooDuration and BarDuration.
    # Note: rounding total to 3 decimal places to avoid floating point
    # arithmetic error in nonsignificant digits.
    total_duration = round(foo_duration + bar_duration, 3)

    # Notes
    # Free form text input by end-users; don't modify.
    notes = row['Notes']

    return [
        eastern_isoformat,
        address,
        zip_code,
        full_name,
        foo_duration,
        bar_duration,
        total_duration,
        notes,
    ]


def normalize_csv(in_file, out_file):
    """Parse input CSV file, normalize, and write to output CSV file."""
    reader = csv.DictReader(in_file)
    writer = csv.writer(out_file)
    for row in reader:
        try:
            writer.writerow(normalize_row(row))
        except ValueError as e:
            # Faled to parse a cell value; print to stderr and drop the row.
            sys.stderr.write('Parse error: {e}\n'.format(e=e))


if __name__ == "__main__":
    # Open stdin and stdout with UTF-8, use the unicode replacement character
    # for any encoding errors.
    normalize_csv(io.open(0, 'r', encoding='utf-8', errors='replace'),
                  io.open(1, 'w', encoding='utf-8', errors='replace'))
