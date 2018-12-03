#! /usr/local/bin/python3
__version__ = '0.1'
__author__ = 'Chris Maenner'

import json
import logging
import sys
from pathlib import Path

class HootsuiteBulkComposer():
    def __init__(self):
        """Class to work with Hootsuite Tools"""
        
        # Logging
        self.logger = logging.getLogger(__name__)

    def hootsuite_message(self, name=False, link=False):
        """Generate dymanic message for Hootsuite"""
        message = f'The community would like to thank {name} for sponsoring BSidesPhilly 3. Your contributions mean a lot! Please feel free to head over to {link} for details'
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

        if not isinstance(messages, list):
            return

        # Run list generator to verify valid keys in template
        return [{validKey: self.verify_template_object(validKey, message) for validKey in verifiedKeys for key, value in message.items()} for message in messages]
