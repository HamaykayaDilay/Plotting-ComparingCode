import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os  # For extracting file names from paths

def select_file(title):
    """Helper function to select a file using a file dialog."""
    file_path = askopenfilename(initialdir= '/home', title=title, filetypes=[("Data Files", "*.dat"), ("All Files", "*.*")])
    if not file_path:
        print("No file selected. Exiting.")
        exit()
    return file_path

def load_data(file_path):
    """Helper function to load data from the file."""
    data = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        column_names = lines[2].strip().split()

    # Adjust column headers
    if len(column_names) != data.shape[1]:
        print(f"Warning: Column count mismatch in {file_path}. Adjusting headers to match data.")
        column_names = column_names[:data.shape[1]]
    data.columns = column_names

    # Ensure all data is numeric where applicable
    data = data.apply(pd.to_numeric, errors='coerce')
    return data

# Create a file dialog to select files
root = Tk()
root.withdraw()  # Hide the root window

file_path_1 = select_file("Select First Results File")
file_path_2 = select_file("Select Second Results File")

# Extract file names for labeling
file_name_1 = os.path.basename(file_path_1)
file_name_2 = os.path.basename(file_path_2)

# Load data from both files
data1 = load_data(file_path_1)
data2 = load_data(file_path_2)

# Specify X and Y columns and their custom labels
x_col_index = 2  # 3rd column (0-based index)
y_col_indices = [3, 4, 27,30]  # Specify desired Y columns (0-based indices)

# Custom labels for columns (adjust as needed)
column_labels = {
    2: "Flexion",
    3: "Internal Rotation",
    4: "Ab./Add.",
    27: "dp lat y",
    30: "dp med y",
}

# Plot the specified columns
x_col_1 = data1.iloc[2:, x_col_index]
x_col_2 = data2.iloc[2:, x_col_index]

for y_col_index in y_col_indices:
    y_col_1 = data1.iloc[2:, y_col_index]
    y_col_2 = data2.iloc[2:, y_col_index]

    x_label = column_labels.get(x_col_index, f"Column {x_col_index + 1}")
    y_label = column_labels.get(y_col_index, f"Column {y_col_index + 1}")

    plt.figure()
    plt.plot(x_col_1, y_col_1, marker='o', linestyle='-', label=f'{file_name_1} - {y_label}')
    plt.plot(x_col_2, y_col_2, marker='x', linestyle='--', label=f'{file_name_2} - {y_label}')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f'{x_label} vs {y_label} (Comparison of {file_name_1} and {file_name_2})')
    plt.legend()
    plt.grid(True)
    plt.show()
