# iplu
Some IP address look up methods.

## tools

### Autonomous System (AS) FIB Generator

This script processes BGP RIB (Routing Information Base) data to generate FIBs (Forwarding Information Bases) for Autonomous Systems (AS) with significant routing information. The script provides the following functionalities:

* Generate FIB Files: Creates FIB files (.txt) for AS IDs with more than 90,000 routing entries.

* Delete Generated Files: Removes all previously generated .txt files.

#### Prerequisites

* Python 3.x installed.

* pybgpstream library installed.


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
    2001:1218:6002::/48 2001:de8:4::5:8511:1
    2001:1218:6004::/48 2001:de8:4::5:8511:1
    2001:1218:6009::/48 2001:de8:4::7713:1
    ```
