#! /usr/local/bin/python3
__version__ = '0.5'
__author__ = 'Chris Maenner'

# Standard Library
import argparse
import csv
import json
import logging
import pandas
import random
import sys
from datetime import date, datetime

# Custom Modules
from modules.hootsuite_tooling import HootsuiteBulkComposer

# Poistional Arguments
parser = argparse.ArgumentParser(prog='main.py', usage='python %(prog)s', description="A tool to help automate randomization of messages for the Hootsuite Bulk Composer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Optional arguements
parser.add_argument('-d', '--debug', action='store_true', help='Turn on debug mode')
parser.add_argument('-t', '--tiering', default=0, type=int, help='Specify tier to generate dates')
parser.add_argument('-sT', '--template', default='./templates/sponsors.json', help='Specify which template to use')
parser.add_argument('-vK', '--validMessageKeys', default=["Link", "Name", "Tier", "TwitterHandle"], type=list, help='Valid message keys for template')
parser.add_argument('-nod', '--numberOfDays', default=5, type=int, help='How many days messages are to post, starting from current day')
parser.add_argument('-nom', '--numberOfMessages', default=5, type=int, help='How many messages posted per day')
parser.add_argument('-oD', '--outputDir', default='./tmp/', type=str, help='Directory where the Hootsuite Builk Composer file is written to')
parser.add_argument('-oF', '--outputFileName', default='hbc', type=str, help='Name of the Hootsuite Builk Composer CSV file')
parser.add_argument('-oT', '--outputFileType', default='csv', type=str, help='Name of the Hootsuite Builk Composer CSV file type')

def main(sponsors=False):
    """Start ETL for Hootsuite Bulk Composer"""

    # Class variables
    args = parser.parse_args()
    hoot = HootsuiteBulkComposer()

    # Variables
    dateRange = list(pandas.date_range(start='1/11/2019 08:00:00', end='1/11/2019 19:00:00', freq='30T'))
    formatter = '%(asctime)s %(levelname)s %(message)s'
    logLevel = logging.INFO
    
    # Hour to be posted by tiering
    tierByHours = [[8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [9, 12, 15]]

    # Turn on debugging
    if args.debug:
        logLevel = logging.DEBUG

    # Enable Logging
    logging.basicConfig(format=formatter, datefmt='%m/%d/%Y %I:%M:%S %p', stream=sys.stdout, level=logLevel)
    logging.getLogger(__name__)

    # Load Sponsors JSON file
    try:
        with open(args.template) as template:
            sponsors = json.load(template)
    except Exception as error:
        logging.error(f'Check to see if the following template is available {args.template}: {error}')
        sys.exit(1)

    # Create Hootsuite Bulk Composer dictionary
    if isinstance(sponsors, list):
        hoot.hootsuite_bulk_composer_generator(dateRange)

    # Verify object is a list before continuing
    if isinstance(sponsors, list):
        messages = hoot.verify_template(args.validMessageKeys, sponsors)
    else:
        messages = False

    # List of all messages
    if isinstance(messages, list):

        # Tiered lists
        try:
            tiering = [[int(value["Tier"]) for value in messages if int(value["Tier"]) in [0, 1, 2]], [int(value["Tier"]) for value in messages if int(value["Tier"]) in [3]]]
        except Exception as error:
            logging.error(f'Something went wrong with creating list of tiers: {error}')
            sys.exit(1)

        # Loop through all 30 minute increments until inserted into dictionary
        while dateRange:

            # Grab date/time
            randomDateTime = str(dateRange[0])

            # Grab random sponsor
            message = random.choice(messages)
            tierLevel = int(message["Tier"])

            # Split date to get day of week in integer
            year, month, day, hour, minute, second = randomDateTime.split(' ')[0].split('-')[0], randomDateTime.split(' ')[0].split('-')[1], randomDateTime.split(' ')[0].split('-')[2], randomDateTime.split(' ')[1].split(':')[0], randomDateTime.split(' ')[1].split(':')[1], randomDateTime.split(' ')[1].split(':')[2]
            randomYMD = f'{year}-{month}-{day}'
            ymd = f'{year}{month}{day}'

            # Return day of week as integer (0=Monday, 6=Sunday),
            dayOfWeek = date(int(year), int(month), int(day)).weekday()

            # Start updating dictionary of unique date/time objects
            planner = hoot.hootsuite_planner(tierLevel, tiering, hour, tierByHours, dayOfWeek, args.validMessageKeys, randomDateTime, message, randomYMD)

            # Delete object from list
            if planner:
                del dateRange[0]

        # Add Hootsuite Bulk Composer file
        with open(f'{args.outputDir}{ymd}_{args.outputFileName}.{args.outputFileType}', 'a') as hbcFile:
            for randomDateTime, sponsorObj in hoot.hootsuitePlanner.items():
                sponsorName = "".join([key for key in sponsorObj.keys()])
                messages = sponsorObj[sponsorName]
                message = [randomDateTime, hoot.hootsuite_message(messages["TwitterHandle"], messages["Name"], messages["Link"]), messages["Link"]]
                messageWriter = csv.writer(hbcFile, delimiter=hoot.delimiter, lineterminator='\n')
                messageWriter.writerow(message)

if __name__=="__main__": main()
