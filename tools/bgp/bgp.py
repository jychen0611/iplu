import pybgpstream

date = "2024-12-19"

# Collect prefix and next-hop pairs
prefix_nexthop_pairs = []

# Initialize the stream with the desired time range and collectors
stream = pybgpstream.BGPStream(
    from_time= date + " 00:00:00", until_time= date + " 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",
)

# Iterate through the stream
for elem in stream:
    # Access the BGPRecord from the stream element
    record = elem.record
    
    # Iterate over each BGPElem in the record
    bgp_elem = record.get_next_elem()
    while bgp_elem is not None:
        # Only process 'announcement' type elements
        if bgp_elem.type == 'A':
            # Access the fields dictionary of the BGPElem object
            fields = bgp_elem.fields
            
            # Extract prefix, next-hop, and prefix length from the fields
            prefix = fields.get('prefix', 'N/A')
            nexthop = fields.get('next-hop', 'N/A')
            
            # If prefix exists, extract prefix length
            if prefix != 'N/A':
                # The prefix length is determined by the CIDR notation of the prefix
                prefixlen = prefix.split('/')[1] if '/' in prefix else 'N/A'
            else:
                prefixlen = 'N/A'
            
            # Output the extracted values
            # print(f"Prefix: {prefix}, Next-Hop: {nexthop}, Prefix Length: {prefixlen}")
            
            # Add the prefix and next-hop to the list if they are valid
            # Filter out only IPv6 prefixes (IPv6 contains ':')
            if prefix != 'N/A' and nexthop != 'N/A' and ':' in prefix:
                prefix_nexthop_pairs.append((prefix, nexthop))
        
        # Move to the next BGPElem in the record
        bgp_elem = record.get_next_elem()


# Sort the prefix and next-hop pairs lexicographically by the prefix
prefix_nexthop_pairs.sort(key=lambda pair: pair[0])

# Open the output file in write mode and write sorted data
with open(date + ".txt", "w") as file:
    for prefix, nexthop in prefix_nexthop_pairs:
        file.write(f"{prefix} {nexthop}\n")


