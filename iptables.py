"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 

Code comment: this code adds rules for iptables (I do not know how configure nft)"""

import os
import subprocess
import sys

import config

if os.name != 'posix':   # Check OS
    print('Run on Linux', file=sys.stderr)
    sys.exit(2)

if os.getuid() != 0:    # Check user
    print('Run as root (UID 0)', file=sys.stderr)
    sys.exit(2)


def add_rules():
    """Adds rules to INPUT and FORWARD chains"""
    for chain in config.IPTABLES_CHAINS:
        subprocess.call(['iptables', '-A', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUE_NUM)])


def remove_rules():
    """Removes rules from INPUT and FORWARD chains"""
    for chain in config.IPTABLES_CHAINS:
        subprocess.call(['iptables', '-D', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUE_NUM)])