# iplu
Some IP address look up methods.

## tools

### BGPStream FIB Generator

This script processes BGP Routing Information Base (RIB) snapshots from the `route-views.sfmix` collector to generate Forwarding Information Base (FIB) files categorized by Autonomous System (AS) ID. The `route-views.sfmix` collector provides routing data from the San Francisco Metro Internet Exchange (SFMIX), located in San Francisco, California.

#### Features

1. **Generate FIB Files**:
   - Extracts routing information from the `route-views.sfmix` RIB collector.
   - Groups prefixes and next-hops by AS ID.
   - Only generates files for AS IDs with more than 90,000 entries.
   - This script primarily focuses on **IPv6** prefixes observed in the RIB data provided by route-views.sfmix. Adjustments can be made to include IPv4 data or other collectors if needed.

2. **Delete Generated Files**:
   - Deletes all `.txt` files in the current directory.

#### Prerequisites

* Python 3.x installed.

* pybgpstream library installed.

* Internet connection to access BGP collectors

#### Usage

Run the script with the following options:

* Generate FIB Files

    This option processes RIB data and generates FIB files for AS IDs with more than 90,000 routing entries. Each file contains IPv6 prefix and next-hop information for the corresponding AS.

    ```shell
    $ python3 bgp.py --generate --date XXXX-YY-ZZ
    ```

* Delete Generated Files

    This option deletes all .txt files generated in previous runs to free up disk space.

    ```shell
    $ python3 bgp.py --delete
    ```



#### Input Data:

Collects BGP data for a specified time range, and filters IPv6 prefixes (`:` in prefix).

#### Output:

* Generates XXXX-YY-ZZ_AS_<AS_ID>.txt files containing prefix nexthop pairs.

* Only includes AS IDs with more than 90,000 entries.


* Each generated .txt file contains the following format:

    <`prefix`> <`next-hop`>

    e.g.

    For `2024-12-19_AS_174.txt`:
    ```
    2001:1201:10::/48 2001:504:30::ba02:253:1
    2001:1201::/48 2001:504:30::ba06:4289:1
    2001:1203:1000::/36 2001:504:30::ba06:4289:1
    ```
