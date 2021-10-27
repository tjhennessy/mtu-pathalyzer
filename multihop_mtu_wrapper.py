import argparse
import csv
import sys
from ipaddress import ip_address, IPv4Address, IPv6Address

import pmtud
from scapy.all import sr1, IP, ICMP, RandShort

MAX_HOPS = 30

# TODO: stdout/stderr context management for optional suppression
# TODO: traceroute logic

def find_each_mtu(**kwargs):
    """
    Kicks off processing of mtu path discovery for each IPv4/v6 address
    specified in kwargs.
    
    Args:
    kwargs (dictionary): contains all arguments from parser
    """

    results = []
    if kwargs['file']:
        ip_list = _process_csv(kwargs['file'])
        for ip in ip_list:
            mtu = pmtud.find_mtu(kwargs['lower'],
                    kwargs['upper'],
                    kwargs['retry'],
                    kwargs['timeout'],
                    ip)
            results.append(f"{ip} mtu: {mtu}")
    
    if kwargs['path_discover']:
        # run traceroute for dest and store each ip
        hops = _traceroute(kwargs['dest_ip'])
        for ip in hops:
            mtu = pmtud.find_mtu(kwargs['lower'],
                kwargs['upper'],
                kwargs['retry'],
                kwargs['timeout'],
                ip)
            results.append(f"{ip} mtu: {mtu}")
    
    return results

def _traceroute(dest_ip):
    """
    Runs a traceroute using scapy to dest_ip and returns a list of
    ip addresses for each hop encountered.txt
    
    Solution adapted from https://montcs.bloomu.edu/VM-LAN/LAN20.asn.traceroutes.html
    
    Args:
    dest_ip (str): IP address of far end of trace
    """
    hops = []
    for n in range(1, MAX_HOPS):
        ip = IP(dst=dest_ip, ttl=n, id=RandShort())
        resp = sr1(ip/ICMP(), retry=1, timeout=3, verbose=False)
        hops.append(resp.src)
        if resp and resp.src == dest_ip:
            break
    return hops

def _process_csv(path):
    """
    Reads in the contents of a CSV file, performs basic validation, and
    returns a list of strings (IPv4/v6).
    
    Args:
        path (str): location of CSV file
    """
    list_of_ips = []
    # Create list of IPs from CSV file
    with open(path) as f:
        for line in csv.reader(f):
            for ip in line:
                if ip:
                    list_of_ips.append(ip.strip())
    
    for ip in list_of_ips:
        if not _validate_ip(ip):
            print("Error: Please make sure file contains only valid IP addresses")
            print(f"Error: {ip} not valid")
            sys.exit(1)
            
    return list_of_ips
    
def _isIPv4(ip):
    return type(ip_address(ip)) is IPv4Address

def _isIPv6(ip):
    return type(ip_address(ip)) is IPv6Address

def _validate_ip(ip):
    """
    Determines if ip parameter is a valid IPv4v6 address.
    
    Args:
        ip (str): possible IPv4v6 address
    """
    isValid = False
    try:
        if (_isIPv4(ip)) or (_isIPv6(ip)):
            isValid = True
    except ValueError:
        pass
    return isValid
    
def _extended_args():
    """
    Adds additional command line arguments for multihop sequences.
    Passes parser object to pmtud.py for arg processing.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="path to CSV file of IPv4/v6"
    )
    parser.add_argument(
        "-p", "--path_discover", type=bool, 
        help="toggle traceroute to find hops in path to dest",
        default=False
    )
    args_d = vars(pmtud._process_args(parser))
    return args_d


if __name__ == '__main__':
    args_d = _extended_args()
    print(find_each_mtu(**args_d))