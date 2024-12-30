import numpy as np
import sys

scores_file = sys.argv[1]
output = sys.argv[2]

# Load scores
scores = np.loadtxt(scores_file)

segments = []
current_segment = [-1, -1]
below_zero_count = 0


for i in range(len(scores)):
    if scores[i] > 0:
        if current_segment[0] == -1:
            current_segment[0] == i
    else:
        if current_segment[0] != -1:
            if below_zero_count == 4:
                current_segment[1] = i - 4
                segments.append(current_segment)
                current_segment = [-1, -1]
                below_zero_count = 0
            else:
                below_zero_count += 1

if current_segment[0] != -1:
    if current_segment[1] == -1:
        current_segment[1] = len(scores)
    segments.append(current_segment)

np.savetxt(output, segments, fmt="%d", delimiter=" ")