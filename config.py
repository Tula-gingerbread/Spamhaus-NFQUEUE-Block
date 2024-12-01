"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import platform
import sys

# Cache expiration time, expressed in seconds (default is 12 hours -- 12 * 3600 seconds). Must be at least 3600 seconds.
EXPIRE_AFTER = 12 * 3600

# NFQUEUE number for packet processing; this specifies which queue to use (default queue number is 44 for v4 and 66 for v6). Must be a positive number.
NFQUEUEV4_NUM = 44
NFQUEUEV6_NUM = 66

# IpTables chains to check. Must be a tuple or list. This script supports only the `filter` table (default is ('INPUT', 'OUTPUT')). Must not be empty.
IPTABLES_CHAINS = ('INPUT', 'OUTPUT')

# Address family. A tuple or list that must contain 4 and/or 6 (default is (4, 6)). Must contain 1 or 2 elements
ADDRESS_FAMILY = (4, 6)



# ------- Dont touch -------

__python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
__arch = platform.machine()

# Spamhaus NFQUEUE Block version
VERSION = '0.0.2'

SPAMHAUS_DROPV4_URL  =  "https://www.spamhaus.org/drop/drop.txt"    # URL to get v4 file 
SPAMHAUS_DROPV6_URL = "https://www.spamhaus.org/drop/dropv6.txt"  # URL to get v6 file
DROPLISTV4_CACHE_FILE = "cache/DROPv4.txt"   # Cached DROPv4 file from SpamHaus
DROPLISTV6_CACHE_FILE = "cache/DROPv6.txt"   # Cached DROPv6 file from SpamHaus
LAST_FETCHV4_FILE = "cache/lastfetchv4.txt"    # Last fetch time for v4 in UNIX timestamp
LAST_FETCHV6_FILE = "cache/lastfetchv6.txt"    # Last fetch time for v6 in UNIX timestamp


REQUESTS_HEADERS = {
    'User-Agent': f'Mozilla/5.0 (Linux; {__arch}; Python {__python_version}; SpamhausNfqueueClient/{VERSION})'
}


# -------- Begin checks -------- #

# --- EXPIRE_AFTER check ---
if not isinstance(EXPIRE_AFTER, int) or EXPIRE_AFTER < 3600:
    print('EXPIRE_AFTER must be an int and at least 3600 seconds.', file=sys.stderr)
    sys.exit(2)

# --- NFQUEUEv4_NUM check --- #
if not isinstance(NFQUEUEV4_NUM, int) or NFQUEUEV4_NUM < 0:
    print('NFQUEUEV4_NUM must be a positive integer or 0.', file=sys.stderr)
    sys.exit(2)

# --- NFQUEUEV6_NUM check --- #
if not isinstance(NFQUEUEV6_NUM, int) or NFQUEUEV6_NUM < 0:
    print('NFQUEUEV6_NUM must be a positive integer or 0.', file=sys.stderr)
    sys.exit(2)

# --- IPTABLES_CHAINS check --- #
if not isinstance(IPTABLES_CHAINS, (tuple, list)) or not IPTABLES_CHAINS:
    print('IPTABLES_CHAINS must be a non-empty tuple or list.', file=sys.stderr)
    sys.exit(2)

# --- ADDRESS_FAMILY check --- #
if not isinstance(ADDRESS_FAMILY, (list, tuple)) or 0 < len(ADDRESS_FAMILY) < 2:
    print('ADDRESS_FAMILY must be list or tuple with one or two elements', file=sys.stderr)
    sys.exit(2)

for item in ADDRESS_FAMILY:
    if item not in [4, 6]:
        print('ADDRESS_FAMILY must contain only integers 4 or 6 with no repitions', file=sys.stderr)
        sys.exit(2)

if ADDRESS_FAMILY[0] == ADDRESS_FAMILY[1]:
    print('ADDRESS_FAMILY must contain only integers 4 or 6 with no repitions', file=sys.stderr)
    sys.exit(2)

# -------- End checks -------- #

if __name__ == '__main__':
    print(f'''\
{SPAMHAUS_DROPV4_URL=}
{DROPLISTV4_CACHE_FILE=}

{SPAMHAUS_DROPV6_URL=}
{DROPLISTV6_CACHE_FILE=}

{NFQUEUEV4_NUM=}
{NFQUEUEV6_NUM=}

{LAST_FETCHV4_FILE=}
{LAST_FETCHV6_FILE=}


{REQUESTS_HEADERS=}
{EXPIRE_AFTER=}
{IPTABLES_CHAINS=}
''')
