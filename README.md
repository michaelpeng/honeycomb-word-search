# Honeycomb Word Search
Search for words in a honeycomb structure

##Overview
####Input:
* honeycomb.txt: Line 1: # of layers; Line 2+: Each layer (clockwise) rotating through graph
* dictionary.txt: Each line contains a valid word for which the program is to search

####Output:
Alphabetically sorted list of valid strings found in honeycomb (printed to stdout)

####Run:
`$ python Solver.py honeycomb.txt dictionary.txt`

####Misc notes:
* Cells cannot be used twice in the formation of a single string.
* If a valid string can be found via multiple paths, print that string only once.

##Approach summary:
1. Construct graph from honeycomb file:
    1. Separate graph into 6 triangles<sup>*</sup>, overlapping in line of nodes drawn from center node out to each corner of hexagon
    2. Each triangle's layer of edges proceeding outward = indexed range of each honeycomb layer
    3. For each pair of adjacent nodes in subarray layer, plus adjacent node in inner layer: set corresponding neighborship among nodes (these 3 nodes form a triangle)<sup>**</sup>
    4. Rotate triangle-wise through graph, changing only:
        1. Subarray indexing
        2. Which neighbor directions are set in each grouping
2. Search for each word in dictionary
    1. Use dictionary mapping first-letters of valid words to their respective words
    2. Also use dictionary mapping first-letters of valid words to nodes with that letter
    3. Use BFS: search for each word in graph
        1. Get hashed list of words for each given first-letter key
        2. Get hashed list of nodes for each given first-letter key
        3. Perform BFS for each word in i) from each node in ii)

\* Boundaries of triangle 0: center node A extending up to L, A extending northeast to G. Boundaries of triangle 1: A extending northeast to G, A extending southeast to X, etc.

\*\* In triangle 1: first grouping is B,C,A (A is innermost node); in next layer of triangle 1: U,A,B and A,N,C, etc.
