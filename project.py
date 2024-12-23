from collections import Counter
import heapq
import string
import pandas as pd
import math

# Define a Huffman Node
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison operators for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    # Create a priority queue with Huffman nodes
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    # Build the tree
    while len(priority_queue) > 1:
        # Extract two nodes with the lowest frequency
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        # Create a new internal node with combined frequency
        new_node = HuffmanNode(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right

        # Add the new node back to the priority queue
        heapq.heappush(priority_queue, new_node)

    # The remaining node is the root of the Huffman Tree
    return priority_queue[0]

def generate_huffman_codes(root, current_code="", codes={}):
    if root is None:
        return

    # If this is a leaf node, assign the code
    if root.char is not None:
        codes[root.char] = current_code
        return

    # Traverse left and right subtrees
    generate_huffman_codes(root.left, current_code + "0", codes)
    generate_huffman_codes(root.right, current_code + "1", codes)

    return codes

def analyze_text(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Normalize text: convert to lowercase, keep letters, digits, space, and dots
        allowed_chars = string.ascii_lowercase + string.digits + ' .'
        normalized_text = ''.join(char.lower() for char in text if char.lower() in allowed_chars)

        # Count the frequency of each character
        char_counts = Counter(normalized_text)

        # Replace the space character with the label "Space"
        if ' ' in char_counts:
            char_counts['Space'] = char_counts.pop(' ')

        # Calculate the total number of characters
        total_chars = sum(char_counts.values())

        # Calculate probabilities
        char_probabilities = {char: count / total_chars for char, count in char_counts.items()}

        # Build the Huffman Tree
        huffman_tree = build_huffman_tree(char_counts)

        # Generate Huffman Codes
        huffman_codes = generate_huffman_codes(huffman_tree)

        # Create a DataFrame for tabulation
        df = pd.DataFrame({
            'Character': list(char_counts.keys()),
            'Frequency': list(char_counts.values()),
            'Probability': list(char_probabilities.values()),
            'Huffman Code': [huffman_codes.get(char, '') for char in char_counts.keys()],
        })

        # Add a column for the length of each Huffman codeword
        df['Length of Codeword'] = df['Huffman Code'].apply(len)

        # Sort the DataFrame by Frequency in descending order
        df = df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)

        return df, char_counts, total_chars, char_probabilities, huffman_codes

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None, None, None, None, None

# Function to calculate the total number of bits for ASCII encoding
def calculate_ascii_bits(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Calculate the total number of bits for ASCII encoding
        # Each character in ASCII is encoded with 8 bits
        num_bits = len(text) * 8
        return num_bits

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None

# Path to the file
file_path = 'To Build A Fire.txt'

# Analyze the text and tabulate results
results_df, char_counts, total_chars, char_probabilities, huffman_codes = analyze_text(file_path)

if results_df is not None:
    print("Character Analysis with Huffman Codes:")
    print(results_df)
    # Optionally, save results to a CSV file
    results_df.to_csv('Character_Analysis_with_Huffman.csv', index=False)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Calculate the total number of bits needed to encode the full story using Huffman Code (Nhuffman)
    Nhuffman = sum(char_counts[char] * len(huffman_codes.get(char, "")) for char in char_counts)

    print(f"\nTotal number of bits needed to encode the story using Huffman Code (Nhuffman): {Nhuffman}")
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

    # Calculate and display the number of bits needed for ASCII encoding
    nascii = calculate_ascii_bits(file_path)
    if nascii is not None:
        print(f"The number of bits needed to encode the full story using ASCII (NASCII) is: {nascii}")
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

#-------------------------------------------------------------------------------------------------------------
# Find the entropy of the alphabet.

# Probabilities of the characters from the table
probabilities = [0.189933, 0.104734, 0.079137, 0.06138, 0.061003, 0.055964, 0.053431, 0.053108, 
                 0.048366, 0.040821, 0.039905, 0.030367, 0.021556, 0.021394, 0.021232, 0.02099, 
                 0.018269, 0.016706, 0.013041, 0.011344, 0.011155, 0.009592, 0.008191, 0.004823, 
                 0.001644, 0.000916, 0.000539, 0.000458]

# Calculate the entropy
entropy = -sum(p * math.log2(p) for p in probabilities)
print("The entropy of the alphabet:")
print("Entropy=", entropy)
print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

#----------------------------------------------------------------------------------------------------------------
# Find the average number of bits/character (L)

# Data
code_length = [2, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 8, 9, 10, 
               11, 11]

multiplication_result = [p * c for p, c in zip(probabilities, code_length)]

L = sum(m_r for m_r in multiplication_result)

print("The average number of bits/character:")
print("L=", L)
print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

if nascii is not None:
    # Calculate compression percentage
    compression_percentage = ((nascii - Nhuffman) / nascii) * 100
    print(f"The percentage of compression achieved by Huffman encoding compared to ASCII is: (({nascii} - {Nhuffman}) / {nascii}) * 100 = {compression_percentage:.2f}%")
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
