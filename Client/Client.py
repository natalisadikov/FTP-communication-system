from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.l2 import Ether
import subprocess
# from getmac import get_mac_address

# Set up the network interface to use
conf.checkIPaddr = False
iface = "ens33"

# IP and port for DNS server
try:
    dns_server_ip = subprocess.check_output("route -n | grep 0.0.0.0",shell=True).split()[1].decode()
except Exception as e:
    print(e)
dns_server_port = 53

def get_mac(iface):
    try:
        result = subprocess.check_output(f"ifconfig | grep {iface}", shell=True).decode().split()[9]
        return result
    except Exception as e:
        print(e)
        return None

# DHCP discover
dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/ \
                 IP(src="0.0.0.0", dst="255.255.255.255")/ \
                 UDP(sport=68, dport=67)/ \
                 BOOTP(get_mac(iface), xid=RandInt())/ \
                 DHCP(options=[("message-type", "discover"), "end"])

# Send the packet and wait for response
try:
    answer, unanswer = srp(dhcp_discover, iface=iface, timeout=5, multi=True)
except Exception as e:
        print(e)

print("Send DHCP discover")
dhcp_offer = None
for pkt in answer:
    if pkt[1][DHCP].options[0][1] == 2:
        dhcp_offer = pkt[1]

if dhcp_offer is None:
    print("No DHCP offer")
else:
    print("Got DHCP offer")

offered_ip = dhcp_offer[BOOTP].yiaddr

# DHCP request
dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ \
               IP(src="0.0.0.0", dst="255.255.255.255")/ \
               UDP(sport=68, dport=67)/ \
               BOOTP(chaddr=dhcp_offer[BOOTP].chaddr)/ \
               DHCP(options=[("message-type", "request"),("requested_addr", offered_ip),("server_id", dhcp_offer[BOOTP].siaddr),"end"])

# Send the packet and wait for response
try:
    answer, unanswer = srp(dhcp_request, iface=iface, timeout=5, multi=True)
except Exception as e:
    print(e)

print("Send DHCP request")
dhcp_ack = None
for pkt in answer:
    if pkt[1][DHCP].options[0][1] == 5:
        dhcp_ack = pkt[1]

if dhcp_ack is None:
    print("No DHCP acknowledge")
else:
    print("Got DHCP acknowledge")

# DNS part

print("Starting DNS..")
dns_query_name = "application.com."
dns_query_type = "A"

# Query packet
dns_query = IP(dst=dns_server_ip) / \
            UDP(dport=dns_server_port) / \
            DNS(rd=1, qd=DNSQR(qname=dns_query_name, qtype=dns_query_type))

print("Sent dns_query")
# Send the packet and wait for response
try:
    dns_response = sr1(dns_query, verbose=0)
except Exception as e:
    print(e)

print("Got dns response")
# Print the IP
ip_for_domain = dns_response[DNSRR].rdata
print("IP from DNS server", ip_for_domain)


