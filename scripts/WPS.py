import numpy as np
import sys

bed_file_path = sys.argv[1]
output_file_path = sys.argv[2]
window = int(sys.argv[3])
chr_length = int(sys.argv[4])
half_window = window // 2
scores = np.zeros(chr_length)

with open(bed_file_path, "r") as file:
    for line in file:
        # Skip comments or headers if necessary
        if line.startswith("#") or line.strip() == "":
            continue

        # Split the line into columns
        columns = line.strip().split("\t")
        chrom, start, end = columns[:3]

        length = end - start
        if length <= window:
            scores[(start-half_window):(end+half_window)] -= 1
        else:
            scores[(start-half_window):(start+half_window)] -= 1
            scores[(start+half_window):(end-half_window)] += 1
            scores[(start+half_window):(end+half_window)] -= 1

np.savetxt(output_file_path, scores, fmt="%d")
