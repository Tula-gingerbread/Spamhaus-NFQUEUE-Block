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

def has_cap_net_admin():
    try:
        with open('/proc/self/status', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('CapEff:'):
                    cap_eff = int(line.split()[1], 16)
                    return (cap_eff & (1 << 12)) != 0  # 12 is CAP_NET_ADMIN
    except (IOError, ValueError) as e:
        print(f"Error reading /proc/self/status: {e}")
    return False
