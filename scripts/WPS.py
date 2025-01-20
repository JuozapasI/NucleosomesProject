import numpy as np
import sys

bed_file_path = sys.argv[1]
output_file_path = sys.argv[2]
window = int(sys.argv[3])
fasta_index = sys.argv[4]
half_window = window // 2

chr_lengths = {}

with open(fasta_index, "r") as file:
	for line in file:
		columns = line.split('\t')
		chr = columns[0]
		length = int(columns[1])
		chr_lengths[chr] = length

scores = { key: np.zeros(chr_lengths[key], dtype = int) for key in chr_lengths }

with open(bed_file_path, "r") as file:
    for line in file:
        # Split the line into columns
        columns = line.strip().split("\t")
        chrom = columns[0]
        start = int(columns[1])
        end = int(columns[2])

        length = end - start
        if length <= window:
            scores[chrom][(start-half_window):(end+half_window)] -= 1
        else:
            scores[chrom][(start-half_window):(start+half_window)] -= 1
            scores[chrom][(start+half_window):(end-half_window)] += 1
            scores[chrom][(end-half_window):(end+half_window)] -= 1



with open(output_file_path, "w") as file:
    for key, value_list in scores.items():
        for position, value in enumerate(value_list):
            file.write(f"{key}\t{position}\t{position}\t{value}\n")

