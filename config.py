"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import platform
import sys

# Cache expiration time, expressed in seconds (by default 12 hours -- 12 * 3600 seconds).
EXPIRE_AFTER = 12 * 3600

# NFQUEUE number for packet processing; this specifies which queue to use (by default queue number is 44).
NFQUEUE_NUM = 44

# IpTables chains to check. This script supports only the `filter` table (by default ['INPUT', 'OUTPUT'])
IPTABLES_CHAINS = ['INPUT', 'OUTPUT']

__python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
__arch = platform.machine()

# Spamhaus NFQUEUE Block version
VERSION = '0.0.1'

SPAMHAUS_DROP_URL = "https://www.spamhaus.org/drop/drop.txt"    # URL to get file 
DROPLIST_CACHE_FILE = "cache/DROPv4.txt"   # Cached DROP file from SpamHaus
LAST_FETCH_FILE = "cache/lastfetch.txt"    # Last fetch time in UNIX timestamp

REQUESTS_HEADERS = {
    'User-Agent': f'Mozilla/5.0 (Linux; {__arch}; Python {__python_version}; SpamhausNfqueueClient/{VERSION})'
}


if __name__ == '__main__':
    print(f'''\
{SPAMHAUS_DROP_URL=}
{DROPLIST_CACHE_FILE=}
{LAST_FETCH_FILE=}
{REQUESTS_HEADERS=}
{EXPIRE_AFTER=}
{NFQUEUE_NUM=}
''')
