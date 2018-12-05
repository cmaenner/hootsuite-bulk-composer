# Hootsuite Bulk Composer

A tool to help automate randomization of messages for the Hootsuite Bulk Composer

## How to load CSV file in Hootsuite

[Bulk Composer](https://help.hootsuite.com/hc/en-us/articles/222630868-Bulk-Composer)

![HowTo](./media/howto.gif)

## How to run Python script

MacOS setup for application:
> * brew install python
> * pip install pipenv
> * git clone https://github.com/bsidesphilly/hootsuite-bulk-composer.git
> * pipenv --python 3.7

    (hootsuite-bulk-composer-9dZPypKf) bash-3.2$ python main.py -h
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
                            Directory where the Hootsuite Builk Composer file is written to (default: ./tmp/)
      -oF OUTPUTFILENAME, --outputFileName OUTPUTFILENAME
                            Name of the Hootsuite Builk Composer CSV file (default: hbc)
      -oT OUTPUTFILETYPE, --outputFileType OUTPUTFILETYPE
                            Name of the Hootsuite Builk Composer CSV file type (default: csv)
