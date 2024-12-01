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


def add_rulesv4():
    """Adds rules to specified chains. v4"""
    if 4 in config.ADDRESS_FAMILY:
        for chain in config.IPTABLES_CHAINS:
            subprocess.call(['iptables', '-A', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUEV4_NUM)])

def add_rulesv6():
    """Adds rules to specified chains. v6"""
    if 6 in config.ADDRESS_FAMILY:
        for chain in config.IPTABLES_CHAINS:
            subprocess.call(['ip6tables', '-A', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUEV6_NUM)])


def remove_rulesv4():
    """Removes rules from specified chains. v4"""
    print('Я чищу блять v4')
    if 4 in config.ADDRESS_FAMILY:
        for chain in config.IPTABLES_CHAINS:
            subprocess.call(['iptables', '-D', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUEV4_NUM)])

def remove_rulesv6():
    """Remove rules from specifed chains. v6"""
    print('Я чищу блять v6')
    if 6 in config.ADDRESS_FAMILY:
        for chain in config.IPTABLES_CHAINS:
            subprocess.call(['ip6tables', '-D', chain, '-j', 'NFQUEUE', '--queue-num', str(config.NFQUEUEV6_NUM)])

if __name__ == '__main__':
    remove_rulesv4()
    remove_rulesv6()