import numpy as np

# Generate a random 4D matrix
matrix = np.random.random((10, 3, 114, 500))

# Define the file name
file_name = "sample_data.npy"

# Save the matrix to .npy file
np.save(file_name, matrix)

print("Matrix saved to", file_name)