"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import ipaddress
import time
import sys

import requests

import config


def fetch_droplist(SPAMHAUS_DROP_URL: str, DROPLIST_CACHE_FILE: str, LAST_FETCH_FILE: str) -> bool:
    response = requests.get(SPAMHAUS_DROP_URL, headers=config.REQUESTS_HEADERS)

    if response.status_code != 200:
        print(f'Can\'t fetch {SPAMHAUS_DROP_URL}', file=sys.stderr)
        return False
    
    content = response.content

    try:
        with open(DROPLIST_CACHE_FILE, 'w', encoding='utf-8') as file:
            file.write(content.decode())
    except (FileNotFoundError, ValueError) as ex:
        print(f'Error while trying write {DROPLIST_CACHE_FILE}: {ex}', file=sys.stderr)
        return False
    
    try:
        current_time = int(time.time())
        current_time = str(current_time)
        with open(LAST_FETCH_FILE, 'w', encoding='utf-8') as file:
            file.write(current_time)
    except (FileNotFoundError, ValueError) as ex:
        print(f'Exception while trying write {LAST_FETCH_FILE}: {ex}', file=sys.stderr)
        return False

    return True


def parse_blocklist(DROPLIST_FILE: str) -> list[ipaddress.IPv4Network|ipaddress.IPv6Network]:
    with open(DROPLIST_FILE, 'r', encoding='utf-8') as file:
        raw_content = file.read()
    raw_content_lines = raw_content.split('\n')

    content_lines = [line for line in raw_content_lines if not line.startswith(';')]

    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].split(';')[0].strip() # Delete comments and whitespace
    
    ip_networks = [ipaddress.ip_network(line) for line in content_lines if line != '']

    return ip_networks


def fetch_and_parse_all_by_config() -> dict[int, list | None]:
    ret = {
        4: None,
        6: None
    }


    if 4 in config.ADDRESS_FAMILY:
        # Try read LAST_FETCHV4_FILE
        try:
            with open(config.LAST_FETCHV4_FILE, 'r', encoding='utf-8') as file:
                last_fetchv4 = int(file.read())
        except (FileNotFoundError, ValueError) as e:
            last_fetchv4 = 0
            with open(config.LAST_FETCHV4_FILE, 'w', encoding='utf-8') as file:
                file.write('0')
            print(f'Cannot open file or convert content to int. File created. Error: {e}', file=sys.stderr)
        
        # If expired, fetch fresh file
        if (last_fetchv4 + config.EXPIRE_AFTER) < int(time.time()):
            print('Fetching fresh drov4list...')
            fetch_droplist(config.SPAMHAUS_DROPV4_URL, config.DROPLISTV4_CACHE_FILE, config.LAST_FETCHV4_FILE)
        
        v4blocklist = parse_blocklist(config.DROPLISTV4_CACHE_FILE)
        ret[4] = v4blocklist

    
    if 6 in config.ADDRESS_FAMILY:
        # Try read LAST_FETCHV6_FILE
        try:
            with open(config.LAST_FETCHV6_FILE, 'r', encoding='utf-8') as file:
                last_fetchv6 = int(file.read())
        except (FileNotFoundError, ValueError) as e:
            last_fetchv6 = 0
            with open(config.LAST_FETCHV6_FILE, 'w', encoding='utf-8') as file:
                file.write('0')
            print(f'Cannot open file or convert content to int. File created. Error: {e}', file=sys.stderr)
        
        # If expired, fetch fresh file
        if (last_fetchv6 + config.EXPIRE_AFTER) < int(time.time()):
            print('Fetching fresh drov6list...')
            fetch_droplist(config.SPAMHAUS_DROPV6_URL, config.DROPLISTV6_CACHE_FILE, config.LAST_FETCHV6_FILE)
        
        v6blocklist = parse_blocklist(config.DROPLISTV6_CACHE_FILE)
        ret[6] = v6blocklist

    return ret