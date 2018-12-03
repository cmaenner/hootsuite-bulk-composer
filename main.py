#! /usr/local/bin/python3
__version__ = '0.1'
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
parser.add_argument('-oD', '--outputDir', default='/tmp/', type=str, help='Directory where the Hootsuite Builk Composer file is written to')
parser.add_argument('-oF', '--outputFileName', default='hbc', type=str, help='Name of the Hootsuite Builk Composer CSV file')


def main(sponsors=False):
    """Start ETL for Hootsuite Bulk Composer"""

    # Class to call argparser
    args = parser.parse_args()

    # Variables
    weekDays = {0: [], 1: [], 2: [], 3: [], 4: []}
    delimiter = u"\u002c"
    formatter = '%(asctime)s %(levelname)s %(message)s'
    logLevel = logging.INFO
    messages = False
    bulkComposerFile = f'{args.outputDir}{args.outputFileName}.csv'
    dateRange = list(pandas.date_range(start='12/6/2018 09:00:00', end='12/6/2018 19:00:00', freq='15T'))
    
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
        hoot = HootsuiteBulkComposer()
        messages = hoot.verify_template(args.validMessageKeys, sponsors)

    if isinstance(messages, list):
        while messages:
            with open(bulkComposerFile, 'a') as hootBulkComposerFile:
                randomDateTime = str(random.choice(dateRange))
                year, month, day = int(randomDateTime.split(' ')[0].split('-')[0]), int(randomDateTime.split(' ')[0].split('-')[1]), int(randomDateTime.split(' ')[0].split('-')[2])
                dayOfWeek = date(year, month, day).weekday()

                if int(messages[0]["Tier"]) == args.tiering:
                    message = [randomDateTime, hoot.hootsuite_message(messages[0]["Name"], messages[0]["Link"]), messages[0]["Link"]]
                    messageWriter = csv.writer(hootBulkComposerFile, delimiter=delimiter, lineterminator='\n')
                    messageWriter.writerow(message)
                    weekDays[dayOfWeek].append("x")

                if len(weekDays[dayOfWeek]) == args.numberOfMessages:
                    del messages[0]

                try:
                    threshold = len(weekDays[0]) + len(weekDays[1]) + len(weekDays[2]) + len(weekDays[3]) + len(weekDays[4])
                except:
                    threshold = 0
                
                if threshold == 25:
                    break

if __name__=="__main__": main()
