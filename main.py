#! /usr/local/bin/python3
__version__ = '0.3'
__author__ = 'Chris Maenner'

# Standard Library
import argparse
import csv
import json
import logging
import pandas
import random
import sys
from datetime import date

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
    bulkComposerFile = f'{args.outputDir}{args.outputFileName}.{args.outputFileType}'
    dateRange = list(pandas.date_range(start='12/5/2018 08:00:00', end='12/10/2018 19:00:00', freq='30T'))
    formatter = '%(asctime)s %(levelname)s %(message)s'
    logLevel = logging.INFO
    
    # Hour to be posted by tiering
    tierByHours = [[8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [9, 11, 13, 15, 17, 19], [9, 12, 15]]

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

    # Verify object is a list before continuing
    if isinstance(sponsors, list):
        messages = hoot.verify_template(args.validMessageKeys, sponsors)
    else:
        messages = False

    # List of all messages
    if isinstance(messages, list):

        # Tiered lists
        try:
            tiering = [[int(value["Tier"]) for value in messages if int(value["Tier"]) in [0, 1]], [int(value["Tier"]) for value in messages if int(value["Tier"]) in [2]], [int(value["Tier"]) for value in messages if int(value["Tier"]) in [3]]]
        except Exception as error:
            logging.error(f'Something went wrong with creating list of tiers: {error}')
            sys.exit(1)

        # Loop through all 45 minute increments until inserted into dictionary
        while dateRange:

            # Grab date/time
            randomDateTime = str(dateRange[0])

            # Grab random sponsor
            message = random.choice(messages)
            tierLevel = int(message["Tier"])

            # Split date to get day of week in integer
            year, month, day, hour, minute, second = int(randomDateTime.split(' ')[0].split('-')[0]), int(randomDateTime.split(' ')[0].split('-')[1]), int(randomDateTime.split(' ')[0].split('-')[2]), int(randomDateTime.split(' ')[1].split(':')[0]), int(randomDateTime.split(' ')[1].split(':')[1]), int(randomDateTime.split(' ')[1].split(':')[2])

            # Return day of week as integer (0=Monday, 6=Sunday),
            dayOfWeek = date(year, month, day).weekday()

            # Start creating dictionary of unique date/time objects
            hoot.hootsuite_planner(tierLevel, tiering, hour, tierByHours, dayOfWeek, args.validMessageKeys, randomDateTime, message)

            # Delete object from list
            del dateRange[0]

        # Add Hootsuite Bulk Composer file
        with open(bulkComposerFile, 'a') as hbcFile:
            for randomDateTime, messages in hoot.hootsuitePlanner.items():
                message = [randomDateTime, hoot.hootsuite_message(messages["TwitterHandle"], messages["Name"], messages["Link"]), messages["Link"]]
                messageWriter = csv.writer(hbcFile, delimiter=hoot.delimiter, lineterminator='\n')
                messageWriter.writerow(message)

if __name__=="__main__": main()
