import json
from ipaddress import IPv4Address
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

conf.checkIPaddr = False
iface = "ens33"

# IP and lease time for DHCP server
dhcp_server = "127.0.0.1"
dhcp_lease_time = 86400

# Dictionary for uses IP's
leased_ips = {}

def load_config():
    try:
        with open('ips.json') as f:
            config = json.load(f)
            class_a = [IPv4Address(ip) for ip in config['classA']]
            class_b = [IPv4Address(ip) for ip in config['classB']]
            class_c = [IPv4Address(ip) for ip in config['classC']]
            return {'classA': class_a, 'classB': class_b, 'classC': class_c}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error in json file: {e}")
        return None

def allocate_ip(chaddr):
    global leased_ips
    config = load_config()
    for subnet, ip_pool in config.items():
        for ip in ip_pool:
            if ip not in leased_ips.values():
                leased_ips[chaddr] = ip
                return str(ip)
        break
    return None


def release_ip(chaddr):
    global leased_ips
    if chaddr in leased_ips:
        del leased_ips[chaddr]

def dhcp(packet):
    try:
        if packet[DHCP] and packet[DHCP].options[0][1] == 1:  # DHCP discover
            print("Got DHCP discover from", packet[Ether].src)
            client_source_addres = packet[Ether].src
            offered_ip = allocate_ip(client_source_addres)
            if offered_ip:
                dhcp_offer = Ether(src=get_if_hwaddr(conf.iface), dst='ff:ff:ff:ff:ff:ff')/ \
                            IP(src=dhcp_server, dst="255.255.255.255")/ \
                            UDP(sport=67, dport=68)/ \
                            BOOTP(op=2, yiaddr=offered_ip, siaddr=dhcp_server, chaddr=client_source_addres)/ \
                            DHCP(options=[("message-type", "offer"),("lease_time", dhcp_lease_time),("server_id", dhcp_server),("subnet_mask", "255.255.255.0"),"end"])
            sendp(dhcp_offer, iface=conf.iface)
            print("Sent DHCP offer to", packet[Ether].src, "with IP address", offered_ip)
        elif packet[DHCP] and packet[DHCP].options[0][1] == 3:  # DHCP request
            print("Got DHCP request from", packet[Ether].src)
            chaddr = packet[Ether].src
            requested_ip = packet[BOOTP].yiaddr
            if requested_ip == 0:
                requested_ip = packet[DHCP].options[2][1]

            dhcp_ack = Ether(dst=packet[Ether].src)/ \
                       IP(src=dhcp_server, dst="255.255.255.255")/ \
                       UDP(sport=67, dport=68)/ \
                       BOOTP(op=2, yiaddr=requested_ip, siaddr=dhcp_server, chaddr=chaddr)/ \
                       DHCP(options=[("message-type", "ack"),("lease_time", dhcp_lease_time),("server_id", dhcp_server),("subnet_mask", "255.255.255.0"),"end"])
            sendp(dhcp_ack, iface=conf.iface)
            print("Sent DHCP acknowledge to", packet[Ether].src)
    except:
        print("Error in DHCP server")

if __name__ == '__main__':
    print("sniffing DHCP packets")
    sniff( filter="udp and (port 67 or port 68)",prn = dhcp)

