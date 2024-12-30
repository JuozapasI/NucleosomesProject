import numpy as np
import sys

segments_file = sys.argv[1]
scores_file = sys.argv[2]
output_file = sys.argv[3]

# Load data
segments = np.loadtxt(segments_file, dtype=int)
scores = np.loadtxt(scores_file, dtype=float)

no_segments = len(segments)

# Function to find maximum-sum contiguous window above the median
def peak(start, end):
    median = np.median(scores[start:end])
    max_sum = 0
    current_sum = 0
    peak_start = -1
    peak_end = -1
    tmp_start = 0

    for i in range(start, end):
        if scores[i] <= median:
            if current_sum > max_sum:
                max_sum = current_sum
                peak_start = tmp_start
                peak_end = i
            current_sum = 0
            tmp_start = i+1
        else:
            current_sum += scores[i]

    if current_sum > max_sum:
                max_sum = current_sum
                peak_start = tmp_start
                peak_end = end

    peak_centre = int((peak_start+peak_end)/2)

    return np.array([peak_start, peak_end, peak_centre, median], dtype=float)

peaks = []

for i in range(no_segments):
    length = segments[i,1] - segments[i,0]
    if length > 50 and length <= 450:
        highest_peak = np.array(peak(segments[i,0], segments[i,1]))
        peaks.append(highest_peak)

    #elif length > 150 and length <= 450:
    #    highest_peak = peak(segments[i,0], segments[i,1])
    #    peaks.append(highest_peak)

np.savetxt(output_file, peaks, fmt=["%d", "%d", "%d", "%.5f"])