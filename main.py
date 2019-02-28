#!/usr/bin/env python3

import sys, os, csv, unicodedata
from datetime import datetime, timezone, timedelta

def main():
    input_file_path = sys.argv[1]
    try:
        with open(input_file_path) as csvinput:
            reader = csv.DictReader(csvinput)
            writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)

            writer.writeheader()

            for idx, row in enumerate(reader, start=1):
                try:
                    obj = row
                    obj['Timestamp'] = convert_timestamp(row['Timestamp'])
                    obj['ZIP'] = row['ZIP'].zfill(5)
                    obj['FullName'] = row['FullName'].upper()
                    obj['FooDuration'] = convert_duration(row['FooDuration'])
                    obj['BarDuration'] = convert_duration(row['BarDuration'])
                    obj['TotalDuration'] = obj['FooDuration'] + obj['BarDuration']
                    obj['Address'] = unicodedata.normalize('NFKD', row['Address'])
                    obj['Notes'] = unicodedata.normalize('NFKD', row['Notes'])
                    writer.writerow(obj)
                except:
                    print('Error processing row {}'.format(idx), file=sys.stderr)

    except FileNotFoundError:
        print('Cannot open file: {}'.format(input_file_path))


def convert_timestamp(input):
    # use simple timezones to avoid importing thrid party libraries.
    pacific_timezone = timezone(timedelta(hours=-7))
    central_timezone = timezone(timedelta(hours=-5))

    time_stamp_naive = datetime.strptime(input, '%m/%d/%y %I:%M:%S %p')
    time_stamp_pacific = time_stamp_naive.replace(tzinfo=pacific_timezone)
    return time_stamp_pacific.astimezone(central_timezone).isoformat()

def convert_duration(input):
    seconds = [3600,60,1,0.001]
    input = input.replace('.', ':')
    return sum([float(a)*b for a,b in list(zip(seconds, map(float, input.split(':'))))])

if __name__ == "__main__":
    main()