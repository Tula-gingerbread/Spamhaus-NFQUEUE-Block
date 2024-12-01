"""
This file is part of Spamhaus NFQUEUE Block.

Spamhaus NFQUEUE Block is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Spamhaus NFQUEUE Block is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Spamhaus NFQUEUE Block. If not, see <https://www.gnu.org/licenses/>. 
"""

import os
import sys
import ipaddress
import threading

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
util_res = util.fetch_and_parse_all_by_config()

if util_res[4] is not None:
    blocked_networksv4 = set(util_res[4])

if util_res[6] is not None:
    blocked_networksv6 = set(util_res[6])

del util_res

# ---------- End init ----------


def packetv4_handler(packet: netfilterqueue.Packet):
    """Process IPv4 packet"""
    # Get IP packet from Ethernet II packet
    ip_packet = scapy.IP(packet.get_payload()) # type: ignore

    if ip_packet.version == 4:   # Check version
        src_ip = ipaddress.ip_address(ip_packet.src)  # Get source address
        dst_ip = ipaddress.ip_address(ip_packet.dst)
        # Check is source/destination address in any blocked network
        for net in blocked_networksv4:
            if src_ip in net:  # Source
                print(f"DROP packet from {src_ip}")
                packet.drop()
                return
            if dst_ip in net:  # destination
                print(f"DROP packet to {dst_ip}")
                packet.drop()
                return
        

    packet.accept()

def packetv6_handler(packet: netfilterqueue.Packet):
    """Process IPv6 packet"""
    # Get IP packet from Ethernet II packet
    ip_packet = scapy.IPv6(packet.get_payload()) # type: ignore

    if ip_packet.version == 6:   # Check version
        src_ip = ipaddress.ip_address(ip_packet.src)  # Get source address
        dst_ip = ipaddress.ip_address(ip_packet.dst)
        # Check is source/destination address in any blocked network
        for net in blocked_networksv6:
            if src_ip in net:  # Source
                print(f"DROP packet from {src_ip}")
                packet.drop()
                return
            if dst_ip in net:  # destination
                print(f"DROP packet to {dst_ip}")
                packet.drop()
                return

    packet.accept()


def mainv4() -> None:
    """Create and bind NFQUEUE processor. Then add iptables rules. Then run processor. On CTRL + C  or exception unbind NFQUEUE and remove iptables rules. v4 version"""
    nfqueue = netfilterqueue.NetfilterQueue()
    
    try:
        nfqueue.bind(config.NFQUEUEV4_NUM, packetv4_handler)
        iptables.add_rulesv4()
        print('Begin NFQUEUE v4 processing')
        nfqueue.run()
    except Exception as ex:
        print(f'Unknown error: {ex}', file=sys.stderr)
    finally:
        print('Stop NFQUEUE v4 processing')
        nfqueue.unbind()

def mainv6() -> None:
    """Create and bind NFQUEUE processor. Then add iptables rules. Then run processor. On CTRL + C  or exception unbind NFQUEUE and remove iptables rules. v6 version"""
    nfqueue = netfilterqueue.NetfilterQueue()
    
    try:
        nfqueue.bind(config.NFQUEUEV6_NUM, packetv6_handler)
        iptables.add_rulesv6()
        print('Begin NFQUEUE v6 processing')
        nfqueue.run()
    except Exception as ex:
        print(f'Unknown error: {ex}', file=sys.stderr)
    finally:
        print('Stop NFQUEUE v6 processing')
        nfqueue.unbind()

def real_main():
    if len(config.ADDRESS_FAMILY) == 1:
        if config.ADDRESS_FAMILY[0] == 4:
            mainv4()
            iptables.remove_rulesv4()
            return
        
        mainv6()
        iptables.remove_rulesv6()
        return

    # Create two threads to handle v4 and v6
    thread_v4 = threading.Thread(target=mainv4)
    thread_v6 = threading.Thread(target=mainv6)
    
    # Start both threads
    thread_v4.start()
    thread_v6.start()
    try:
        # Wait for both threads to complete
        thread_v4.join()
        thread_v6.join()
    finally:
        iptables.remove_rulesv4()
        iptables.remove_rulesv6()


if __name__ == '__main__':
    real_main()