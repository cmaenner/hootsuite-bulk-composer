#! /usr/local/bin/python3
__version__ = '0.5'
__author__ = 'Chris Maenner'

import csv
import json
import logging
import random
import sys
from collections import OrderedDict
from pathlib import Path
from pprint import pprint

class HootsuiteBulkComposer():
    def __init__(self):
        """Class to work with Hootsuite Tools"""
        
        # Logging
        self.logger = logging.getLogger(__name__)

        # Variables
        self.delimiter = u"\u002c"
        self.weekDays = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.hashtags = ' '.join(["#bsidesphilly", "#bsidesphillysponsors"])
        self.hootsuitePlanner = OrderedDict()
        self.hspCounter = {}

    def hootsuite_bulk_composer_generator(self, dateRange):
        """Create object of scheduled posts"""
        for key in dateRange:
            self.hootsuitePlanner[str(key)] = {}

    def hootsuite_message(self, handle=False, name=False, link=False):
        """Generate dymanic message for Hootsuite"""
        if name in ["Point3"]:
            message = f'The community would like to thank {name} for sponsoring BSidesPhilly 3 as well as supporting our CTF this year. Registration for the CTF will be held at the conference. Head over to {link} for details about {handle} {self.hashtags[1]}'
        elif handle:
            message = f'The community would like to thank {name} for sponsoring BSidesPhilly 3. Your contributions mean a lot! Please feel free to head over to {link} for details {handle} {self.hashtags}'
        else:
            message = f'The community would like to thank {name} for sponsoring BSidesPhilly 3. Your contributions mean a lot! Please feel free to head over to {link} for details {self.hashtags}'
        return message

    def path_creation(self, outputDir):
        """Create directory if doesn't exist"""

        # Return if path exists
        if Path(outputDir).is_dir():
            return

        # Create path if doesn't exist
        try:
            Path(outputDir).mkdir(mode=0o750, parents=True, exist_ok=True)
        except Exception as error:
            self.logger.error(f'Failed to make directory "{outputDir}" due to the following: {error}')
            sys.exit(1)
    
    def verify_template_object(self, key, message):
        """Verify message object is a dictionary"""
        try:
            value = message[key]
        except:
            value = ""
        return value

    def verify_template(self, verifiedKeys, messages, index=0):
        """Check to see if valid keys exist"""

        # Return if message is not a list
        if not isinstance(messages, list):
            return

        # Run list generator to verify valid keys in template
        return [{validKey: self.verify_template_object(validKey, message) for validKey in verifiedKeys for key, value in message.items()} for message in messages]

    def hootsuite_planner_insert(self, randomDateTime, sponsorName, validMessageKeys, message):
        """Insert sponsor into dictionary to prepare Hootsuite Planner"""

        # Insert sponsor name
        self.hootsuitePlanner[randomDateTime][sponsorName] = {}

        # Create dictionary of unique date/time
        for key in validMessageKeys:
                self.hootsuitePlanner[randomDateTime][sponsorName][key] = message[key]

    def hootsuite_planner(self, tierLevel, tiering, hour, tierByHours, dayOfWeek, validMessageKeys, randomDateTime, message, randomYMD, sponsorName="", valid=True):
        """Create ordered dictionary of date/time objects"""

        # Check to see if date & time value was updated
        if len(self.hootsuitePlanner[randomDateTime].keys()) > 0:
            return False

        # Get sponsor name
        try:
            sponsorName = message["Name"]
        except Exception as error:
            self.logger.error(f'Please check to see if the "Name" key is in "./templates/sponsors.json": {error}')
            return False

        # Keep track of posts per day
        if randomYMD not in [ymd.split(" ")[0] for ymd in self.hspCounter.keys()]:
            try:
                self.hspCounter[randomYMD] = {}
            except:
                pass

        # Check to see if sponsor was added to threshold counter
        try:
            sponsorNameList = self.hspCounter[randomYMD][sponsorName]
        except:
            sponsorNameList = False

        # Create new sponsor threshold counter object
        if isinstance(sponsorNameList, bool):
            self.hspCounter[randomYMD][sponsorName] = []

        # Add counter for sponsor threshold counter object
        self.hspCounter[randomYMD][sponsorName].append(0)

        # Sponsors threshold was met for the day
        if len(self.hspCounter[randomYMD][sponsorName]) > 2:
            return False

        # Tier 3 sponsorship for Tues, Thur
        if tierLevel in tiering[1] and hour in tierByHours[1] and dayOfWeek in [1, 3]:
            # Insert sponsor name
            self.hootsuite_planner_insert(randomDateTime, sponsorName, validMessageKeys, message)
        else:
            # Insert sponsor name
            self.hootsuite_planner_insert(randomDateTime, sponsorName, validMessageKeys, message)

        # Return boolean statement to remove value from list
        return valid
