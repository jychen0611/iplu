import os
import pybgpstream
import argparse

# Function to delete all .txt files in the current directory
def delete_txt_files():
    for file in os.listdir():
        if file.endswith(".txt"):
            os.remove(file)
            print(f"Deleted: {file}")

# Function to generate FIBs based on AS ID
def generate_fib_by_as(date, allow_duplicates=False):
    prefix_nexthop_pairs = []

    # Initialize the stream
    stream = pybgpstream.BGPStream(
        from_time=f"{date} 00:00:00",
        until_time=f"{date} 00:01:00 UTC",
        collectors=["route-views.sfmix"],
        record_type="ribs",
    )

    for elem in stream:
        record = elem.record
        bgp_elem = record.get_next_elem()
        while bgp_elem is not None:
            if bgp_elem.type == 'R':
                fields = bgp_elem.fields
                prefix = fields.get('prefix', None)
                nexthop = fields.get('next-hop', None)
                as_path = fields.get('as-path', None)
                if prefix and nexthop and as_path and ':' in prefix:
                    prefix_nexthop_pairs.append((prefix, nexthop, as_path))
            bgp_elem = record.get_next_elem()

    prefix_nexthop_pairs.sort(key=lambda pair: pair[0])

    # New logic depending on allow_duplicates
    as_fibs = {}

    for prefix, nexthop, as_path in prefix_nexthop_pairs:
        for as_id in as_path.split():
            if as_id not in as_fibs:
                as_fibs[as_id] = {} if not allow_duplicates else []
            if not allow_duplicates:
                if prefix not in as_fibs[as_id]:
                    as_fibs[as_id][prefix] = nexthop
            else:
                as_fibs[as_id].append((prefix, nexthop))

    # Write the FIBs
    for as_id, fib_data in as_fibs.items():
        entry_count = len(fib_data) if allow_duplicates else len(fib_data.keys())
        if entry_count > 90000:
            as_filename = f"{date}_AS_{as_id}.txt"
            with open(as_filename, "w") as file:
                if allow_duplicates:
                    for prefix, nexthop in fib_data:
                        file.write(f"{prefix} {nexthop}\n")
                else:
                    for prefix, nexthop in fib_data.items():
                        file.write(f"{prefix} {nexthop}\n")
            print(f"Generated: {as_filename}")
        else:
            print(f"Skipped AS_{as_id} (only {entry_count} entries)")

# Main CLI
parser = argparse.ArgumentParser(description="Process BGP updates.")
parser.add_argument('--delete', action='store_true', help="Delete all previously generated .txt files.")
parser.add_argument('--generate', action='store_true', help="Generate FIBs based on AS ID.")
parser.add_argument('--date', type=str, help="Specify the date for generating FIBs.", default="2024-12-19")
parser.add_argument('--allow-duplicates', action='store_true', help="Allow duplicate prefixes in FIBs.")
args = parser.parse_args()

if args.delete:
    delete_txt_files()

if args.generate:
    generate_fib_by_as(args.date, allow_duplicates=args.allow_duplicates)
