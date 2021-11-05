import argparse
import csv
import sys
from ipaddress import ip_address, IPv4Address, IPv6Address

import pmtud
from scapy.all import sr1, IP, ICMP, RandShort

MAX_HOPS = 30

# TODO: stdout/stderr context management for optional suppression

def find_each_mtu(**kwargs):
    """
    Kicks off processing of mtu path discovery for each IPv4/v6 address
    specified in kwargs.
    
    Note: the file and path_discover options should not be used together
    if they are then only the path_discover results will be returned.
    
    Args:
        kwargs (dictionary): contains all arguments from parser

    Returns:
        list: strings of the form "ip mtu"
    """

    ip_list = []
    if kwargs['file']:
        ip_list = _process_csv(kwargs['file'])
    
    if kwargs['path_discover']:
        # run traceroute for dest and store each ip
        ip_list = _traceroute(kwargs['dest_ip'])
    
    if len(ip_list) < 1:
        # case where just destination ip given
        # TODO: need to make sure IP is valid before appending
        ip_list.append(kwargs['dest_ip'])

    results = _get_results(kwargs['lower'],
                kwargs['upper'],
                kwargs['retry'],
                kwargs['timeout'],
                ip_list)

    return results

def _get_results(lower, upper, retry, timeout, ip_list):
    """
    Takes a list of IP addresses and finds the mtu for each returning a
    list of key value pairs (ip: mtu). If
    
    Args:
        lower (int): lower bound mtu size
        upper (int): upper bound mtu size
        retry (int): number of packets to send to destination ip address
        timeout (int): waiting period before aborting attempt
        ip_list (list): IP address strings
    
    Returns:
        list: strings of the form "ip mtu"
    """

    results = []
    for ip in ip_list:
        mtu = pmtud.find_mtu(lower,
                upper,
                retry,
                timeout,
                ip)

        results.append(f"{ip} mtu: {mtu}")

    return results

def _traceroute(dest_ip):
    """
    Runs a traceroute using scapy to dest_ip and returns a list of
    ip addresses for each hop encountered.
    
    Note: only adds valid IP addresses, so if filtering occurs along
    the route and does not return an IP that hop will not be included.
    
    Note: if MAX_HOPS is exceeded route will not be complete.
    
    Solution adapted from https://montcs.bloomu.edu/VM-LAN/LAN20.asn.traceroutes.html
    
    Args:
        dest_ip (str): IP address of far end of trace
        
    Returns:
        list: ip address strings
    """

    hops = []
    for n in range(1, MAX_HOPS+1):
        ip = IP(dst=dest_ip, ttl=n, id=RandShort())
        resp = sr1(ip/ICMP(), retry=1, timeout=3, verbose=False)
        if resp and _is_valid_ip(resp.src):
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
    with open(path) as f:
        for line in csv.reader(f):
            for ip in line:
                if ip:
                    list_of_ips.append(ip.strip())
    
    for ip in list_of_ips:
        if not _is_valid_ip(ip):
            print("Error: Please make sure file contains only valid IP addresses")
            print(f"Error: {ip} not valid")
            sys.exit(1)
            
    return list_of_ips

def _isIPv4(ip):
    """
    Determines if ip is valid IPv4 address.
    
    Args:
        ip (str): possible IP address

    Returns:
        bool: True when ip is IPv4 address False otherwise
    """
    return type(ip_address(ip)) is IPv4Address

def _isIPv6(ip):
    """
    Determines if ip is IPv6 address

    Args:
        ip (str): possible IP address

    Returns:
        bool: True when ip is IPv6 address False otherwise
    """
    return type(ip_address(ip)) is IPv6Address

def _is_valid_ip(ip):
    """
    Determines if ip parameter is a valid IPv4v6 address.

    Args:
        ip (str): possible IPv4v6 address

    Returns:
        bool: True when ip is valid IPv4/v6 False otherwise
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
        "-p", "--path_discover", action='store_true',
        help="toggle traceroute to find hops in path to dest"
    )

    args_d = vars(pmtud._process_args(parser))

    return args_d


if __name__ == '__main__':
    args_d = _extended_args()
    results = find_each_mtu(**args_d)
    print("\n\nResults: ")
    print(results)