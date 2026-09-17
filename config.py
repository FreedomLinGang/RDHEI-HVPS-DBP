"""Default parameters used in the published paper.

The main experiments use seed 42 for both the XOR encryption key
and the random secret payload. Block size (s1, s2) = (4, 2) matches
the dynamic 4x4 / 2x2 partitioning described in the paper.
"""

# Encryption key and secret-data seed (paper default)
SEED = 42

# Dynamic block partitioning: 4x4 blocks, optionally split into 2x2
S1 = 4
S2 = 2

IMAGE_DIR = "./imgs"
RESULT_DIR = "./results"
OUTPUT_LOG = "./results/output.txt"
