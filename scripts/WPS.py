import numpy as np

bed_file_path = ""
output_file_path = ""
window = 120
half_window = window // 2
chr_length = 0
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
            scores[start:end] -= 1
        else:
            scores[start:(start+half_window)] -= 1
            scores[(start+half_window):(end-half_window)] += 1
            scores[(start+half_window):end] -= 1
                   
np.savetxt(output_file_path, scores, fmt="%d")