import matplotlib.pyplot as plt
from collections import Counter

# Read dataset
def read_prefixes(filename):
    prefixes = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():  # skip empty lines
                parts = line.strip().split()
                prefixes.append(parts[0])  # take only the left part (prefix)
    return prefixes

def plot_frequency(prefixes, top_n=30):
    counter = Counter(prefixes)
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    # Only take top N
    top_items = sorted_items[:top_n]
    labels, counts = zip(*top_items)

    plt.figure(figsize=(12, 6))
    plt.bar(range(len(labels)), counts)
    plt.xticks(range(len(labels)), labels, rotation=90, fontsize=8)
    plt.xlabel('Prefix')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Prefix Frequency Distribution')
    plt.tight_layout()
    plt.show()

# Main
if __name__ == "__main__":
    # Replace 'dataset.txt' with your actual file name
    filename = '2024-12-19_AS_397131.txt'
    prefixes = read_prefixes(filename)
    plot_frequency(prefixes, top_n=100)