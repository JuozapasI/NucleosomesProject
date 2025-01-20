import numpy as np
import sys
from collections import defaultdict

if len(sys.argv) == 1:
    print("Usage: python peakCalling.py <segments> <scores> <output>")
    sys.exit(1)

segments_file = sys.argv[1]
scores_file = sys.argv[2]
output_file = sys.argv[3]


# Function to find maximum-sum contiguous window above the median
def peak(chrom, start, end):
    median = np.median(scores[chrom][start:end])
    max_sum = 0
    current_sum = 0
    peak_start = -1
    peak_end = -1
    tmp_start = start

    for i in range(start, end +1):
        if scores[chrom][i] <= median:
            if current_sum > max_sum:
                max_sum = current_sum
                peak_start = tmp_start
                peak_end = i - 1
            current_sum = 0
            tmp_start = i + 1
        else:
            current_sum += scores[chrom][i]

    if current_sum > max_sum:
        max_sum = current_sum
        peak_start = tmp_start
        peak_end = end
    
    if peak_start == -1:
        return [str(i) for i in [-1, -1, -1, -1, -1]]
    peak_centre = int((peak_start + peak_end) / 2)
    score = max(scores[chrom][(peak_start):(peak_end)]) - min(scores[chrom][start:end])
    return [str(i) for i in [chrom, peak_start, peak_end, peak_centre, score]]


print("Starting")
scores = defaultdict(list)  # Dictionary of lists
with open(scores_file, 'r') as file:
    print("Loading scores")
    for line in file:
        parts = line.strip().split("\t")  # Split the line by tab
        key = parts[0]                    # First column as key
        value = float(parts[3])           # Fourth column as value
        scores[key].append(value)         # Append value to the corresponding key
print("Scores loaded")

peaks = []
with open(segments_file, "r") as seg_file:
    c = 0
    for line in seg_file:
        c += 1
        if c % 100000 == 0:
            print(c, "segments done.")
        chrom, start, end = line.strip().split()
        start, end = int(start), int(end)

        length = end - start
        if length > 50 and length <= 450:
            highest_peak = peak(chrom, start, end)
            if int(highest_peak[2]) - int(highest_peak[1]) > 50 and int(highest_peak[2]) - int(highest_peak[1]) < 150:
                peaks.append(highest_peak)

with open(output_file, "w") as output:
    print("Writing output")
    for peak in peaks:
        output.write("\t".join(peak) + "\n")

print("Done.")
