"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import os
import sys
import ipaddress
import time

import netfilterqueue
import scapy.all as scapy

import config
import iptables
import util


if __name__ == '__main__':    # Display note about license
    print('Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\nYou should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>.', end='\n\n', file=sys.stderr)


# ---------- Checks ----------
if os.name != 'posix':  # Check OS
    print('Run on Linux', file=sys.stderr)
    sys.exit(2)

if (os.getuid() != 0) or (not util.has_cap_net_admin()):  # Check user
    print('Run as root (UID 0) or with CAP_NET_ADMIN', file=sys.stderr)
    sys.exit(2)
# ---------- End checks ----------


# ---------- Init ----------
# Check last fetch time
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
    util.fetch_droplist(config.SPAMHAUS_DROPV6_URL, config.DROPLISTV6_CACHE_FILE, config.LAST_FETCHV6_FILE)

# Get set ( for O(1) ) of blocked networks
blocked_networks = set(util.parse_blocklist(config.DROPLISTV6_CACHE_FILE)) 

# ---------- End init ----------


def packet_handler(packet: netfilterqueue.Packet) -> None:
    """Process IPv6 packet"""
    # Get IP packet from Ethernet II packet
    ip_packet = scapy.IP(packet.get_payload()) # type: ignore

    if ip_packet.version == 4:   # Check version
        src_ip = ipaddress.ip_address(ip_packet.src)  # Get source address
        dst_ip = ipaddress.ip_address(ip_packet.dst)  # Get destination address
        # Check is source/destination address in any blocked network
        for net in blocked_networks:
            if src_ip in net:  # Source
                print(f"DROP packet from {src_ip}")
                packet.drop()
                return
            if dst_ip in net:  # Destination
                print(f"DROP packet to {dst_ip}")
                packet.drop()
                return
        
    packet.accept()


def main() -> None:
    """Create and bind NFQUEUE processor. Then add iptables rules. Then run processor. On CTRL + C  or exception unbind NFQUEUE and remove iptables rules. v6 version"""
    nfqueue = netfilterqueue.NetfilterQueue()
    
    try:
        nfqueue.bind(config.NFQUEUEV6_NUM, packet_handler)
        iptables.add_rulesv6()
        print('Begin NFQUEUE v6 processing')
        nfqueue.run()
    except Exception as ex:
        print(f'Unknown error: {ex}', file=sys.stderr)
    finally:
        print('Stop NFQUEUE v6 processing')
        iptables.remove_rulesv6()
        nfqueue.unbind()

if __name__ == '__main__':
    main()