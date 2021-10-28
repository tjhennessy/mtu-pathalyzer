# mtu-pathalyzer
Determines the MTU size for a sequence of IP addresses or all IP addresses between source and destination IP addresses.

Shout out to nickrusso42518 for the core logic behind the mtu discovery. Please visit his github page and leave him a
star https://github.com/nickrusso42518/net-tools/tree/master/path_mtu_discovery.

## Setup

```bash
$ cd mtu-pathalyzer-
$ chmod 755 run.sh
```

## Usage

### Help / Options Overview
```bash
$ ./run.sh --help
usage: multihop_mtu_wrapper.py [-h] [-f FILE] [-p] [-l LOWER] [-u UPPER] [-r RETRY] [-t TIMEOUT] [-e EXPECTED_MTU] [-d DEST_IP]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to CSV file of IPv4/v6
  -p, --path_discover   toggle traceroute to find hops in path to dest
  -l LOWER, --lower LOWER
                        lower bound MTU in bytes
  -u UPPER, --upper UPPER
                        upper bound MTU in bytes
  -r RETRY, --retry RETRY
                        per-MTU probe retries
  -t TIMEOUT, --timeout TIMEOUT
                        probe timeout in seconds
  -e EXPECTED_MTU, --expected_mtu EXPECTED_MTU
                        MTU value to verify
  -d DEST_IP, --dest_ip DEST_IP
                        target IPv4/v6
```

### Single IP Address MTU Discovery

```bash
$ ./run.sh -d 8.8.4.4
8.8.4.4: MTU 5140 (lower 1280 / upper 9000) ... FAIL!
8.8.4.4: MTU 3209 (lower 1280 / upper 5139) ... FAIL!
8.8.4.4: MTU 2244 (lower 1280 / upper 3208) ... FAIL!
8.8.4.4: MTU 1761 (lower 1280 / upper 2243) ... FAIL!
8.8.4.4: MTU 1520 (lower 1280 / upper 1760) ... FAIL!
8.8.4.4: MTU 1399 (lower 1280 / upper 1519) ... OK!
8.8.4.4: MTU 1459 (lower 1400 / upper 1519) ... OK!
8.8.4.4: MTU 1489 (lower 1460 / upper 1519) ... OK!
8.8.4.4: MTU 1504 (lower 1490 / upper 1519) ... FAIL!
8.8.4.4: MTU 1496 (lower 1490 / upper 1503) ... OK!
8.8.4.4: MTU 1500 (lower 1497 / upper 1503) ... OK!
8.8.4.4: MTU 1502 (lower 1501 / upper 1503) ... FAIL!
8.8.4.4: MTU 1501 (lower 1501 / upper 1501) ... FAIL!


Results: 
['8.8.4.4 mtu: 1500']
```

### Run MTU Discovery for every IP Address Between You and Destination

Note: ./run.sh --path_discover -d 8.8.4.4 could also be used

```bash
$ ./run.sh -p -d 8.8.4.4

----stdout intentionally removed for brevity----

Results: 
['192.168.4.1 mtu: 1500', '192.168.0.1 mtu: 1500', '24.42.128.1 mtu: 1500', '143.59.254.96 mtu: 1500', '24.96.198.18 mtu: 1500', '216.186.180.250 mtu: 1500', '143.59.255.198 mtu: 1500', '75.76.35.44 mtu: 1500', '69.73.2.31 mtu: 1500', '172.253.71.61 mtu: 1500', '216.239.43.25 mtu: 1500', '8.8.4.4 mtu: 1500']
```

### Run MTU Discovery Using File with IP Addresses

```bash
$ ./run.sh -f file.csv

---stdout intentionally removed for brevity----

Results: 
['142.250.191.132 mtu: 1500', '8.8.8.8 mtu: 1500', '8.8.4.4 mtu: 1500']
```

## Notes

The file and path_discover options should not be used together. If they are
used together then only the path_discover results will be returned.

When using the traceroute option (-p/--path_discover):

<ul>
    <li>If MAX_HOPS (30) is exceeded route will not be complete</li>
    <li>Only uses valid IP addresses, so if filtering occurs along the route and 
    those hops will not be included</li>
</ul>
