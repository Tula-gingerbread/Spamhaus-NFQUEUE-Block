"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import os
import sys
import time
import ipaddress

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

if os.getuid() != 0:  # Check user
    print('Run as root (UID 0)', file=sys.stderr)
    sys.exit(2)
# ---------- End checks ----------


# ---------- Init ----------
# Check last fetch time
try:
    with open(config.LAST_FETCH_FILE, 'r', encoding='utf-8') as file:
        last_fetch = int(file.read())
except (FileNotFoundError, ValueError) as e:
    last_fetch = 0
    with open(config.LAST_FETCH_FILE, 'w', encoding='utf-8') as file:
        file.write('0')
    print(f'Cannot open file or convert content to int. File created. Error: {e}', file=sys.stderr)

# If expired, fetch fresh file
if (last_fetch + config.EXPIRE_AFTER) < int(time.time()):
    print('Fetching fresh drov4list...')
    util.fetch_dropv4list()

print('Parsing blockv4list...')
blocked_networks = util.parse_ipv4()
# ---------- End init ----------


def packetv4_handler(packet: netfilterqueue.Packet):
    """Process IPv4 packet"""
    # Get IP packet from Ethernet II packet
    ip_packet = scapy.IP(packet.get_payload()) # type: ignore

    if ip_packet.version == 4:   # Check version
        src_ip = ipaddress.ip_address(ip_packet.src)  # Get source address
        dst_ip = ipaddress.ip_address(ip_packet.dst)
        # Check is source/destanation address in any blocked network
        for net in blocked_networks:
            if src_ip in net:  # Source
                print(f"DROP packet from {src_ip}")
                packet.drop()
                return
            if dst_ip in net:  # Destanation
                print(f"DROP packet to {dst_ip}")
                packet.drop()
                return
        

    packet.accept()


def main() -> None:
    """Create and bind NFQUEUE processor. Then add iptables rules. Then run processor. On CTRL + C  or exception unbind NFQUEUE and remove iptables rules"""
    nfqueue = netfilterqueue.NetfilterQueue()
    
    try:
        nfqueue.bind(config.NFQUEUE_NUM, packetv4_handler)
        iptables.add_rules()
        print('Begin NFQUEUE processing')
        nfqueue.run()
    except KeyboardInterrupt:
        print('KeyboardInterrupt', file=sys.stderr)
    except Exception as ex:
        print(f'Unknown error: {ex}', file=sys.stderr)
    finally:
        print('Stop NFQUEUE processing')
        nfqueue.unbind()
        iptables.remove_rules()


if __name__ == '__main__':
    main()