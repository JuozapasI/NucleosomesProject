import numpy as np
import sys
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from itertools import groupby

# Load file paths
file = sys.argv[1]
output = sys.argv[2]

#  Parameters
window_size = 1000  
savitzky_golay_window = 21  
savitzky_golay_order = 2

# Function to process scores for a single chromosome
def process_scores(scores):
    # Step 1: Adjust to a running median of zero
    median_adjusted = scores - median_filter(scores, size=window_size)
    # Step 2: Smooth using a Savitzky-Golay filter
    smoothed = savgol_filter(median_adjusted, savitzky_golay_window, savitzky_golay_order)
    return smoothed

def process_file_by_chromosome(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        # Group lines by chromosome
        for chrom, lines in groupby(infile, key=lambda line: line.split("\t")[0]):
            # Read lines for the current chromosome
            chrom_data = [line.strip().split("\t") for line in lines]
            scores = np.array([float(row[3]) for row in chrom_data])  # Fourth column

            # Process scores
            adjusted_scores = process_scores(scores)

            # Write updated data to the output file
            for i, row in enumerate(chrom_data):
                row[3] = f"{adjusted_scores[i]:.5f}"  # Update the score
                outfile.write("\t".join(row) + "\n")

process_file_by_chromosome(file, output)
