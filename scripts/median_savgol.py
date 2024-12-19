import numpy as np
import sys
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter

# Load the data
file = sys.argv[1]
output = sys.argv[2]

data = np.loadtxt(file, delimiter=",")

#  Parameters
window_size = 1000  
savitzky_golay_window = 21  
savitzky_golay_order = 2

# Step 1: Adjust to a running median of zero
median_adjusted_data = data - median_filter(data, size=window_size)

# Step 2: Smooth using a Savitzky-Golay filter
smoothed_data = savgol_filter(median_adjusted_data, savitzky_golay_window, savitzky_golay_order)

# Save the processed data to a new CSV file
np.savetxt(output, smoothed_data, delimiter=",")
