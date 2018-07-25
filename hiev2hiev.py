#!/usr/bin/env python3
"""
Transfer data (and associated metadata) from one HIEv instance to another

"""

__author__ = "Gerard Devine"
__version__ = "0.1.0"
__license__ = "MIT"


import os
import shutil
import hievpy as hp
from datetime import datetime


# -- Open log file for writing and append date/time stamp into file for a new entry
logfile = 'log.txt'
log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), logfile), 'a')
log.write('\n\n------------  Begin: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'  ------------ \n')

# Set the URLs/IPs of the source and destination HIEv
hiev_source = 'https://hiev.westernsydney.edu.au/'
hiev_dest = 'https://hortgh.westernsydney.edu.au/'
# Set the API token for both the source and destination HIEv
api_token_source = os.environ['HIEV_API_KEY']
api_token_dest = os.environ['HIEV_API_KEY']


# Get the current path
cwd = os.getcwd()


# Check if necessary folders are in place and create if not
if not os.path.exists(os.path.join(cwd, 'Data')):
    os.mkdir(os.path.join(cwd, 'Data'))
if not os.path.exists(os.path.join(cwd, 'Backups')):
    os.mkdir(os.path.join(cwd, 'Backups'))


data_dir = os.path.join(cwd, 'Data')
backups_dir = os.path.join(cwd, 'Backups')


# Search the source HIEv and, in turn, download each file and metadata matching the search params
log.write(f'\n*Info: Searching {hiev_source}....')
orig_records = hp.search(api_token_source, base_hiev=hiev_source, from_date="2017-03-15", to_date="2017-03-16", facilities=['10'])
log.write(f'\n*Info: Found {len(orig_records)} matching files')


for orig_record in orig_records:
    filename = orig_record['filename']
    log.write(f'\n*Info: Downloading file {filename} locally...')
    hp.download(api_token_source, orig_record, path=data_dir)

    # Set path of file (i.e the file just downloaded) to be uploaded
    filenamepath = os.path.join(data_dir, orig_record['filename'])

    # Set metadata variables for upload (i.e replicating those of the file just downloaded)
    # metadata = {'creator_email': orig_record['creator'],
    metadata = {'creator_email': 'g.devine@westernsydney.edu.au',
                'description': orig_record['file_processing_description'],
                # 'experiment_id': orig_record['experiment_id'],
                'experiment_id': '2',
                'contributor_names[]': orig_record['contributors'],
                'type': orig_record['file_processing_status']}

    log.write(f'\n*Info: Uploading file {filename} to new HIEv...')
    hp.upload(api_token_dest, filenamepath, metadata, base_url=hiev_dest)


log.write(f'\n*Info: Completed \n')