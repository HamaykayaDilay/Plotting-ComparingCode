#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:50:01 2024

@author: dhamaykaya
"""
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Create a file dialog to select the file
root = Tk()
root.withdraw()  # Hide the root window
file_path = askopenfilename(title="Select Results File", filetypes=[("Data Files", "*.dat"), ("All Files", "*.*")])

if not file_path:
    print("No file selected. Exiting.")
    exit()

# Load the file while skipping comment lines (#)
data = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)

# Use the 3rd row (index 2) as column headers
with open(file_path, 'r') as file:
    lines = file.readlines()
    column_names = lines[2].strip().split()

# Adjust column headers
if len(column_names) != data.shape[1]:
    print("Warning: Column count mismatch. Adjusting headers to match data.")
    column_names = column_names[:data.shape[1]]
data.columns = column_names

# Ensure all data is numeric where applicable
data = data.apply(pd.to_numeric, errors='coerce')

# Specify X and Y columns and their custom labels
x_col_index = 2  # 3rd column (0-based index)
y_col_indices = [3, 4, 22]  # Specify desired Y columns (0-based indices)

# Custom labels for columns (adjust as needed)
column_labels = {
    2: "Flexion",
    3: "Angles",
    4: "Internal Rotation",
    22: "Rolling Lateral",
}

# Plot the specified columns
x_col = data.iloc[:, x_col_index]
for y_col_index in y_col_indices:
    y_col = data.iloc[:, y_col_index]
    x_label = column_labels.get(x_col_index, f"Column {x_col_index + 1}")
    y_label = column_labels.get(y_col_index, f"Column {y_col_index + 1}")
    plt.figure()
    plt.plot(x_col, y_col, marker='o', linestyle='-', label=y_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f'{x_label} vs {y_label}')
    plt.legend()
    plt.grid(True)
    plt.show()
