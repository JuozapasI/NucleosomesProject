import numpy as np
import sys

scores_file = sys.argv[1]
output_file = sys.argv[2]

current_segment = [-1, -1, -1]
below_zero_count = 0
prev_position = -1

with open(scores_file, "r") as file, open(output_file, "w") as output:
    for line in file:
        row = line.split("\t")
        chrom = row[0]
        position = int(row[1])
        score = float(row[3])

        if chrom != current_segment[0] and current_segment[1] != -1:
            current_segment[2] = prev_position
            if current_segment[2] - current_segment[1] > 50:
                output.write("\t".join([str(i) for i in current_segment]) + "\n")
            current_segment = [-1, -1, -1]
            below_zero_count = 0

        if score > 0:
            below_zero_count = 0
            if current_segment[1] == -1:
                current_segment[0] = chrom
                current_segment[1] = position
        else:
            if current_segment[1] != -1:
                if below_zero_count == 4:
                    current_segment[2] = position - 4
                    if current_segment[2] - current_segment[1] > 50:
                        output.write("\t".join([str(i) for i in current_segment]) + "\n")
                    current_segment = [-1, -1, -1]
                    below_zero_count = 0
                else:
                    below_zero_count += 1

        prev_position = position

