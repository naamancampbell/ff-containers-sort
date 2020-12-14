import sys

min_python = (3, 6)
if sys.version_info < min_python:
    sys.exit('ERROR: Python %s.%s or later is required.\n' % min_python)

import argparse
import getpass
import json
import os
import platform
import re
import time

from datetime import datetime
from glob import glob
from pathlib import Path
from shutil import copyfile

###############################################################################
## ff-containers-sort - sorts Firefox Containers
##
## Usage: python ff_containers_sort.py [--no-sort] [--manual]
##
## Requires: Python 3.6+
##            - f-strings will generate SyntaxError on older versions
##
## Author: Naaman Campbell
##         12 December 2020
##
## Version: 1.4.1 | 2020-12-14 - NC | Support multiple Firefox profiles
##          See CHANGELOG.md for full details
##
## Sources:
##  - Python version detection  - https://bit.ly/2Wbr9U0
##  - Remove files after x days - https://bit.ly/3qLCpVm
##  - Firefox profile paths     - https://bit.ly/344SDzl
##
###############################################################################


def sort_containers(conf_filename, sort, manual):
    conf_dir = os.path.dirname(conf_filename)

    # backup config
    timestamp = time.strftime('%Y%m%d-%H%M%S', time.localtime())
    backup_prefix = 'ff_containers_sort'
    backup_filename = os.path.join(
        conf_dir, f'{backup_prefix}-{timestamp}.json'
    )
    copyfile(conf_filename, backup_filename)

    # remove backups older than 7 days
    for backup in glob(f'{conf_dir}/{backup_prefix}-*.json'):
        file_created = os.path.getctime(backup)
        file_age = datetime.today() - datetime.fromtimestamp(file_created)
        if file_age.days > 7:
            os.remove(backup)

    with open(conf_filename) as conf_file:
        conf = json.load(conf_file)

    public_identities = [i for i in conf['identities'] if i['public']]

    if sort:
        # only sort custom identities
        default_identities = [i for i in public_identities if not i.get('name')]
        custom_identities = [i for i in public_identities if i.get('name')]
        custom_identities.sort(key=lambda i: i['name'])
        public_identities = default_identities + custom_identities

    public_identities_count = len(public_identities)

    if manual:
        print('Firefox Containers:')
        for index, item in enumerate(public_identities, start=1):
            if item.get('name'):
                item_name = item['name']
            else:
                # standard identities
                regex = r'userContext(.*)\.accesskey'
                match = re.match(regex, item['accessKey'])
                if match:
                    item_name = match.group(1)
                else:
                    item_name = 'N/A'
            print(f'{index}: {item_name}')

        # generate number range as a string
        initial_list = list(range(1, (public_identities_count + 1)))
        initial_list = [str(i) for i in initial_list]
        initial_list = ', '.join(initial_list)

        new_order = input(
            '\nEdit the following list to set new container order:\n'
            + initial_list
            + '\n\n'
        )

        try:
            new_order = new_order.split(', ')
        except:
            sys.exit('Unable to convert to Python list')

        # sort public identities
        public_identities = [public_identities[int(i) - 1] for i in new_order]

    # determine reserved ids for private identities
    private_identities = [i for i in conf['identities'] if not i['public']]
    reserved_ids = [
        item['userContextId']
        for item in private_identities
        if item['userContextId'] < public_identities_count
    ]

    # generate list of ids with reserved ids removed
    public_ids = list(
        range(1, (public_identities_count + 1) + len(reserved_ids))
    )
    for resv_id in reserved_ids:
        public_ids.remove(resv_id)

    # re-number 'public' Container objects
    for item in public_identities:
        public_ids.reverse()
        item['userContextId'] = public_ids.pop()

    conf['identities'] = public_identities + private_identities

    with open(conf_filename, 'w') as conf_file:
        json.dump(conf, conf_file)

    print('Restart Firefox to reload updated Containers config:')
    print(conf_filename)


def locate_config(sort, manual):
    # default Firefox profile paths
    user = getpass.getuser()
    ff_paths = {
        'Linux': f'/home/{user}/.mozilla/firefox',
        'Windows': f'C:/Users/{user}/AppData/Roaming/Mozilla/Firefox/Profiles',
        'Darwin': f'/Users/{user}/Library/Application Support/Firefox/Profiles',
    }

    try:
        platform_name = platform.system()
        ff_dir = ff_paths[platform_name]
    except KeyError:
        sys.exit(f'Unsupported platform: {platform_name}')

    # locate config file
    conf_glob = os.path.join(ff_dir, '**', 'containers.json')
    conf_filenames = glob(conf_glob, recursive=True)

    if len(conf_filenames) > 1:
        print('\nMultiple Firefox profiles found:\n')
        for file_num, filename in enumerate(conf_filenames, start=1):
            conf_dir = os.path.dirname(filename)
            conf_dirname = os.path.basename(conf_dir)
            print(f'{file_num}) {conf_dirname}')
        profile = input(
            '\nEnter profile number to sort Containers\n'
            + '(or enter A to sort all profiles): '
        )
        print('')
        if profile == 'A':
            for conf_filename in conf_filenames:
                sort_containers(conf_filename, sort, manual)
        elif profile.isnumeric() and int(profile) <= len(conf_filenames):
            sort_containers(conf_filenames[int(profile) - 1], sort, manual)
        else:
            sys.exit('\nERROR: Unsupported option')
    else:
        # single profile
        sort_containers(conf_filenames[0], sort, manual)


def main():
    command_description = '''
        Sorts and re-numbers Firefox Containers config objects in the
        Firefox containers.json config file
    '''

    argparser = argparse.ArgumentParser(description=command_description)

    argparser.add_argument(
        '-n',
        '--no-sort',
        dest='sort',
        action='store_false',
        help='Disable sorting',
    )

    argparser.add_argument(
        '-m',
        '--manual',
        dest='manual',
        action='store_true',
        help='Manual sorting',
    )

    argresults = argparser.parse_args()

    sort = argresults.sort
    manual = argresults.manual

    locate_config(sort, manual)


if __name__ == '__main__':
    main()