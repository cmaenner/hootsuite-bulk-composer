# Hootsuite Bulk Composer

A tool to help automate randomization of messages for the Hootsuite Bulk Composer

## TODO:

• Better documentation on how to use (I promise)

## How to use

    (hootsuite-bulk-composer)$ python main.py -h
    usage: python main.py

    A tool to help automate randomization of messages for the Hootsuite Bulk
    Composer

    optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           Turn on debug mode (default: False)
    -t TIERING, --tiering TIERING
                            Specify tier to generate dates (default: 0)
    -sT TEMPLATE, --template TEMPLATE
                            Specify which template to use (default: ./templates/sponsors.json)
    -vK VALIDMESSAGEKEYS, --validMessageKeys VALIDMESSAGEKEYS
                            Valid message keys for template (default: ['Link', 'Name', 'Tier', 'TwitterHandle'])
    -nod NUMBEROFDAYS, --numberOfDays NUMBEROFDAYS
                            How many days messages are to post, starting from current day (default: 5)
    -nom NUMBEROFMESSAGES, --numberOfMessages NUMBEROFMESSAGES
                            How many messages posted per day (default: 5)
    -oD OUTPUTDIR, --outputDir OUTPUTDIR
                            Directory where the Hootsuite Builk Composer file is written to (default: /tmp/)
    -oF OUTPUTFILENAME, --outputFileName OUTPUTFILENAME
                            Name of the Hootsuite Builk Composer CSV file (default: hbc)
