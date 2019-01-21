#! /usr/local/bin/python3
__version__ = '0.6'
__author__ = 'Chris Maenner'

import json
import logging
import sys

class CreateTemplates():
    def __init__(self, tmpList):
        """Class to work with Hootsuite Tools"""

        # Logging
        self.logger = logging.getLogger(__name__)

        # Variables
        self.loadedTemplates = {}
        self.templateKeys = []
        self.templates = tmpList if isinstance(tmpList, list) else []

    def create(self):
        """Create dictionary from templates folder"""

        # List of template names
        templates = self.templates

        # Load Sponsors JSON file
        while templates:

            # Load path of temple into string
            template = templates[0] if isinstance(templates, list) else ""

            # Get name of tamplate
            try:
                templateKey = str(template.split('/')[2].split('.')[0])
            except Exception as error:
                logging.error(f'Check to see if the following template is available {templates}: {error}')
                sys.exit(1)

            # Start creation of data structure
            self.loadedTemplates[templateKey] = False

            # Load key into for identifying dictionary key
            self.templateKeys.append(templateKey)

            # Load template into memory
            try:
                with open(template) as template:
                    templateLoad = json.load(template)
            except Exception as error:
                logging.error(f'Check to see if the following template is available {template}: {error}')
                sys.exit(1)

            # Add array of dictionaries into template key identifier {"templateKey": [{}, {}, {}]}
            if isinstance(templateLoad, list):
                self.loadedTemplates[templateKey] = templateLoad

            # Delete object from list
            if self.loadedTemplates[templateKey]:
                del templates[0]
