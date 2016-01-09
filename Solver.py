import sys
import getopt
import fileinput

"""
Quantcast Programming Question: Honeycomb Word Search

Input:
honeycomb.txt: Line 1: # of layers; Line 2+: Each layer (clockwise) rotating through graph
dictionary.txt: Each line contains a valid word for which the program is to search

Output:
Alphabetically sorted list of valid strings found in honeycomb (printed to stdout)

Run:
> python Solver.py honeycomb.txt dictionary.txt

Misc notes:
Cells cannot be used twice in the formation of a single string.
If a valid string can be found via multiple paths, print that string only once.

Approach summary:
1) Construct graph from honeycomb file:
    a) Separate graph into 6 triangles*, overlapping in line of nodes
        drawn from center node out to each corner of hexagon
    b) Each triangle's layer of edges proceeding outward = indexed range of each honeycomb layer
    c) For each pair of adjacent nodes in subarray layer, plus adjacent node in inner layer:
        set corresponding neighborship among nodes (these 3 nodes form a triangle)**
    d) Rotate triangle-wise through graph, changing only:
        i)  subarray indexing
        ii) which neighbor directions are set in each grouping

2) Search for each word in dictionary
    a) Use dictionary mapping first-letters of valid words to their respective words
    b) Also use dictionary mapping first-letters of valid words to nodes with that letter
    c) Use BFS: search for each word in graph
        i)   get hashed list of words for each given first-letter key
        ii)  get hashed list of nodes for each given first-letter key
        iii) perform BFS for each word in i) from each node in ii)

*   Boundaries of triangle 0: center node A extending up to L, A extending northeast to G
    Boundaries of triangle 1: A extending northeast to G, A extending southeast to X, etc.
**  In triangle 1: first grouping is B,C,A (A is innermost node);
    in next layer of triangle 1: U,A,B and A,N,C, etc.
"""

# Parse honeycomb.txt file for the layers
honeycomb = [list(item) for item in open(sys.argv[1]).read().splitlines()]

# Parse dictionary.txt file for words
word_list = [item for item in open(sys.argv[2]).read().splitlines()]

# Create dictionary mapping first letters to words
# Create dictionary mapping first letters to nodes
word_dict = {}
node_dict = {}

# Populate dictionaries
for word in word_list:
    first_letter = word[0]
    if first_letter not in word_dict:
        node_dict[first_letter] = []
        word_dict[first_letter] = [word]
    else:
        word_dict[first_letter].append(word)


# Define Node class, clockwise and counterclockwise helpers
class Node:
    """Node class represents hexagon graph's nodes"""
    def __init__(self, letter):
        self.letter = letter
        self.N  = None
        self.NE = None
        self.SE = None
        self.S  = None
        self.SW = None
        self.NW = None

    def get_letter(self):
        """Return node's letter"""
        return self.letter

    def get_neighbors(self):
        """Return a list of node's neighbors"""
        return [self.N, self.NE, self.SE, self.S, self.SW, self.NW]

    def assign_neighbors(self, direction, node):
        """Assign neighbor pairs between node and another node in a direction"""
        if direction == "N":
            self.N = node
            node.S = self
        elif direction == "NE":
            self.NE = node
            node.SW = self
        elif direction == "SE":
            self.SE = node
            node.NW = self
        elif direction == "S":
            self.S = node
            node.N = self
        elif direction == "SW":
            self.SW = node
            node.NE = self
        elif direction == "NW":
            self.NW = node
            node.SE = self

def clockwise(direction):
    """Return direction clockwise from input"""
    if direction == "N":
        return "NE"
    elif direction == "NE":
        return "SE"
    elif direction == "SE":
        return "S"
    elif direction == "S":
        return "SW"
    elif direction == "SW":
        return "NW"
    elif direction == "NW":
        return "N"

def counterclockwise(direction):
    """Return direction counterclockwise from input"""
    if direction == "N":
        return "NW"
    elif direction == "NE":
        return "N"
    elif direction == "SE":
        return "NE"
    elif direction == "S":
        return "SE"
    elif direction == "SW":
        return "S"
    elif direction == "NW":
        return "SW"


honeycomb_layers = []

# Create layers of graph:  lists of Nodes
for layer in honeycomb[1:]:
    node_layer = []
    for letter in layer:
        node = Node(letter)
        node_layer.append(node)
        if letter in word_dict.keys():
            node_dict[letter].append(node)
    honeycomb_layers.append(node_layer)

# Loop each enveloping layer around to its first element
for layer in honeycomb_layers[1:]:
    layer.append(layer[0])

# Set neighbors in graph
first_dxn = "S"
for triangle_index in range(6):
    for layer in honeycomb_layers[1:]:
        layer_index = honeycomb_layers.index(layer)
        start = triangle_index * (layer_index)
        end = start+layer_index
        for node in layer[start:end]:
            node_index = layer.index(node)
            sub_index = layer[start:end].index(node)

            next_node = layer[node_index+1]

            inner_start = triangle_index * (layer_index-1)
            inner_node = honeycomb_layers[layer_index-1][inner_start+sub_index]

            node.assign_neighbors(first_dxn, inner_node)
            node.assign_neighbors(counterclockwise(first_dxn), next_node)
            next_node.assign_neighbors(clockwise(first_dxn), inner_node)
    first_dxn = clockwise(first_dxn)

# Define the bfs method for this graph
def bfs(start, word):
    """BFS search for word in graph given a start node.

    Returns true if word is pathable in graph.

    queue   -- contains tuples of (node, letter_index of search word)
    visited -- maintains set of visited nodes
    """
    word_length = len(word)
    letter_index = 0
    next_letter = word[letter_index]

    # Keep track of which letter_index is sought from a given node
    visited, queue = set(), [(start, letter_index)]

    while queue:
        node, letter_index = queue.pop(0)
        if node and node not in visited:
            next_letter = word[letter_index]
            if node.get_letter() == next_letter:
                visited.add(node)
                # If last letter was just found, return True
                if letter_index+1 > word_length-1:
                    return True
                queue.extend([(neighbor, letter_index+1) for neighbor in node.get_neighbors()])
                next_letter = word[letter_index]

found_words = set([])

# Loop first-letter-wise through words + nodes with correct start letter
for (letter, words) in word_dict.items():
    for word in words:
        for node in node_dict[letter]:
            if bfs(node, word):
                found_words.add(word)
                break

# Sort output, then print
sorted_output = sorted(found_words)
for word in sorted_output:
    print(word)
