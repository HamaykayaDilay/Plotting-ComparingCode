from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as plt
import os

#This version can do more files than 2.



def select_files():
    """Select files one by one using a file dialog."""
    file_paths = []
    while True:
        file_path = askopenfilename( initialdir= '/home',
            title="Select a data file",
            filetypes=[("Data Files", "*.dat"), ("All Files", "*.*")]
        )
        if not file_path:
            print("No more files selected.")
            break  # Exit when the user cancels the file selection
        file_paths.append(file_path)
    if not file_paths:
        print("No files selected. Exiting.")
        exit()
    return file_paths

def load_data(file_path):
    """Helper function to load data from a file."""
    # Read the data file
    data = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        column_names = lines[2].strip().split()  # Adjust this index based on your file format

    # Adjust column headers
    if len(column_names) != data.shape[1]:
        print(f"Warning: Column count mismatch in {file_path}. Adjusting headers to match data.")
        column_names = column_names[:data.shape[1]]
    data.columns = column_names

    # Ensure all data is numeric where applicable
    data = data.apply(pd.to_numeric, errors='coerce')
    return data

# Create a Tkinter root window
root = Tk()
root.withdraw()  # Hide the root window

# Select and load files one by one
file_paths = select_files()
file_names = [os.path.basename(file_path) for file_path in file_paths]
data_list = [load_data(file_path) for file_path in file_paths]

# Specify X and Y columns and their custom labels
x_col_index = 2  # 3rd column (0-based index)
y_col_indices = [3, 4, 5, 6, 7]  # Specify desired Y columns (0-based indices)

# Custom labels for columns
column_labels = {
    2: "a",
    3: "b",
    4: "c ",
    5: "d",
    6: "e",
    7: "f",
}
# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the folder name
folder_name = "Results"

# Construct the absolute path to the folder
folder_path = os.path.join(script_dir, folder_name)

for y_col_index in y_col_indices:
    plt.figure()  # Create a new figure for each Y-column
    x_label = column_labels.get(x_col_index, f"Column {x_col_index + 1}")
    y_label = column_labels.get(y_col_index, f"Column {y_col_index + 1}")

    # Plot data from all files on the same graph
    for data, file_name in zip(data_list, file_names):
        x_col = data.iloc[:, x_col_index]
        y_col = data.iloc[:, y_col_index]
        plt.plot(x_col, y_col, marker='o', linestyle='-', label=f'{file_name} - {y_label}')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    title = f'{x_label} vs {y_label} (Comparison of Multiple Files)'
    plt.title(title)

    # Save the plot using a sanitized title as filename
    safe_title = title.replace(" ", "_").replace("(", "").replace(")", "")  # Remove spaces and special chars
    # Ensure the folder exists before saving
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Directory '{folder_name}' created successfully.")

    # Save the plot using a sanitized title as the filename
    safe_title = title.replace(" ", "_").replace("(", "").replace(")", "")  # Sanitize the title
    file_path = os.path.join(folder_path, f"{safe_title}.png")  # Construct the file path

    plt.savefig(file_path)  # Save the plot
    plt.legend()
    plt.grid(True)
    plt.show()
