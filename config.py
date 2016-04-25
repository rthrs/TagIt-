"""
    Configuration file.
"""

# SPECTOGRAM
DATA_POINTS = 4096
NUM_OVER = 2048
FREQ = 10000

# FINDING PEAKS
AMP_MIN = 10
PEAK_NEIGHBORHOOD_SIZE = 20

# HASHING
NUM_OF_PEAKS = 15 # number of neighborhood peaks to consider
MAX_TIME_DIFF = 150 # maximum time difference

# RECOGNITION
THRESHOLD = 15
