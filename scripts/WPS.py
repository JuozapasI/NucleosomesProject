import numpy as np
import sys

bed_file_path = sys.argv[1]
output_file_path = sys.argv[2]
window = int(sys.argv[3])
chr_length = int(sys.argv[4])
half_window = window // 2
scores = np.zeros(chr_length, dtype=int)

with open(bed_file_path, "r") as file:
    for line in file:
        # Split the line into columns
        columns = line.strip().split("\t")
        chrom = columns[0]
        start = int(columns[1])
        end = int(columns[2])

        length = end - start
        if length <= window:
            scores[(start-half_window):(end+half_window)] -= 1
        else:
            scores[(start-half_window):(start+half_window)] -= 1
            scores[(start+half_window):(end-half_window)] += 1
            scores[(end-half_window):(end+half_window)] -= 1

np.savetxt(output_file_path, scores, fmt="%d")
