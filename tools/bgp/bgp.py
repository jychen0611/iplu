import os
import pybgpstream
import argparse

# Function to delete all .txt files in the current directory
def delete_txt_files():
    for file in os.listdir():
        if file.endswith(".txt"):
            os.remove(file)
            print(f"Deleted: {file}")

# Function to generate the .txt file based on AS ID
def generate_fib_by_as(date):
    # Collect prefix and next-hop pairs
    prefix_nexthop_pairs = []

    # Initialize the stream with the desired time range and collectors
    stream = pybgpstream.BGPStream(
        from_time=f"{date} 00:00:00",
        until_time=f"{date} 00:01:00 UTC",
        collectors=["route-views.sfmix"], # route-views.sfmix.routeviews.org | FRR | IPv4/6 | San Francisco Metro IX, San Francisco, California
        record_type="ribs",
    )

    # Iterate through the stream
    for elem in stream:
        # Access the BGPRecord from the stream element
        record = elem.record

        # Iterate over each BGPElem in the record
        bgp_elem = record.get_next_elem()
        while bgp_elem is not None:
            # Only process 'RIB Entry' type elements
            if bgp_elem.type == 'R':
                # Access the fields dictionary of the BGPElem object
                fields = bgp_elem.fields
                
                # Extract prefix, next-hop, and as-path from the fields
                prefix = fields.get('prefix', None)
                nexthop = fields.get('next-hop', None)
                as_path = fields.get('as-path', None)
                
                # Validate and add prefix, next-hop, and as-path to the list
                if prefix and nexthop and as_path and ':' in prefix:
                    prefix_nexthop_pairs.append((prefix, nexthop, as_path))
            
            # Move to the next BGPElem in the record
            bgp_elem = record.get_next_elem()

    # Sort the prefix and next-hop pairs lexicographically by the prefix
    prefix_nexthop_pairs.sort(key=lambda pair: pair[0])

    # Generate FIB files based on AS ID
    as_fibs = {}
    for prefix, nexthop, as_path in prefix_nexthop_pairs:
        for as_id in as_path.split():
            if as_id not in as_fibs:
                as_fibs[as_id] = {}
            # Ensure only one next-hop per prefix
            if prefix not in as_fibs[as_id]:
                as_fibs[as_id][prefix] = nexthop

    # Write the FIBs to separate .txt files for each AS with more than 90,000 entries
    for as_id, fib_data in as_fibs.items():
        if len(fib_data) > 90000:  # Only generate FIB files for AS with more than 90,000 entries
            as_filename = f"{date}_AS_{as_id}.txt"
            with open(as_filename, "w") as file:
                for prefix, nexthop in fib_data.items():  # Use .items() for correct unpacking
                    file.write(f"{prefix} {nexthop}\n")
            print(f"Generated: {as_filename}")
        else:
            print(f"Skipped AS_{as_id} (only {len(fib_data)} entries)")
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process BGP updates.")
parser.add_argument('--delete', action='store_true', help="Delete all previously generated .txt files.")
parser.add_argument('--generate', action='store_true', help="Generate FIBs based on AS ID.")
parser.add_argument('--date', type=str, help="Specify the date for generating FIBs.", default="2024-12-19")
args = parser.parse_args()

# Execute based on user input
if args.delete:
    delete_txt_files()

if args.generate:
    if not args.date:
        print("Using default date 2024-12-19.")
        generate_fib_by_as(args.date)
    else:
        generate_fib_by_as(args.date)

