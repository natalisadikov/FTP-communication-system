from scapy.all import *
from scapy.layers.dns import DNS, DNSRR, DNSQR
from scapy.layers.inet import UDP, IP
import subprocess

# IP and port for the DNS server
dns_server_ip = subprocess.check_output("route -n | grep 0.0.0.0",shell=True).split()[1].decode()
dns_server_port = 53

dns_records = {
    "michael.com.": "175.181.241.96",
    "natali.com.": "119.195.95.25",
    "application.com.": "192.85.32.10"
}

def dns(packet):
    try:
        # Check if it's a query packet
        if DNS in packet and packet[DNS].opcode == 0 and packet[DNS].ancount == 0:
            print("Got DNS query")
            dns_query_name = packet[DNSQR].qname.decode()

            if dns_query_name in dns_records:
                ip_address = dns_records[dns_query_name]
                # Response packet
                dns_response = IP(dst=packet[IP].src, src=dns_server_ip) / \
                                UDP(dport=packet[UDP].sport, sport=dns_server_port) / \
                                DNS(id=packet[DNS].id, qr=1, qd=packet[DNS].qd, \
                                    an=DNSRR(rrname=dns_query_name, ttl=60, rdata=ip_address))

                send(dns_response, verbose=0)
                print("Send DNS response")
    except:
        print("Error in DNS server")

if __name__ == '__main__':
    try:
        print("Sniffing DNS packets")
        sniff(filter="udp port 53", prn=dns)
    except:
        print("Can't sniff")
