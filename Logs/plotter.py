import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the current working directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))

# Get a list of all Excel files in the script's directory
excel_files = [file for file in os.listdir(script_directory) if file.endswith(".xlsx")]

# Sort the Excel files by modification date in descending order
excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(script_directory, x)), reverse=True)

# Select the most recently modified Excel file
if excel_files:
    excel_file = os.path.join(script_directory, excel_files[0])
else:
    print("No Excel files found in the script's directory.")
    exit()

# Extract the file name (without extension) from the excel_file path
file_name = os.path.splitext(os.path.basename(excel_file))[0]

# Read the selected Excel file into a DataFrame
df = pd.read_excel(excel_file, engine='openpyxl')

# Get the column headers
headers = list(df.columns)

# Create a single figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

# Extract data from columns 2, 3, 4, and 5
x_data = df.iloc[:, 0] - df.iloc[0, 0]  # First column as x-axis
y_data1 = df.iloc[:, 1]  # Second column for the first graph
y_data2 = df.iloc[:, 3]  # Fourth column for the second graph
y_data3 = df.iloc[:, 2]  # Third column for the third graph
y_data4 = df.iloc[:, 4]  # Fifth column for the fourth graph

# Plot the first graph on the top subplot
ax1.plot(x_data, y_data1, label=headers[1])
ax1.plot(x_data, y_data2, label=headers[3])
ax1.set_ylabel("Pixels")
ax1.legend()
ax1.grid()

# Plot the second graph on the bottom subplot
ax2.plot(x_data, y_data3, label=headers[2])
ax2.plot(x_data, y_data4, label=headers[4])
ax2.set_xlabel(headers[0] + " [s]")
ax2.set_ylabel("Pixels")
ax2.legend()
ax2.grid()

# Automatically adjust y-axis limits for both subplots
ax1.set_ylim(min(min(y_data1), min(y_data2)), max(max(y_data1), max(y_data2)))
ax2.set_ylim(min(min(y_data3), min(y_data4)), max(max(y_data3), max(y_data4)))
ax1.set_xlim(min(x_data), max(x_data))

# Set the title for the entire sheet
fig.suptitle(file_name+".xlsx", fontsize=16)

# Adjust spacing between subplots
plt.tight_layout()

# Save the entire sheet plot to a file with the same name as the Excel file
plt.savefig(os.path.join(script_directory, f"{file_name}.png"))

# Show the plot
plt.show()
