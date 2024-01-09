import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the current working directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))

#####



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


"""

####
file_name = "log_24-01-09_20-02"
excel_file = file_name + ".xlsx"

####

"""


# Read the selected Excel file into a DataFrame
df = pd.read_excel(excel_file, sheet_name=0, engine='openpyxl')  # First sheet for the data

# Get the text from the "NOTE" cell in the second sheet
notes_df = pd.read_excel(excel_file, sheet_name=1, engine='openpyxl')  # Second sheet for the note
note_cell = notes_df.loc[notes_df.iloc[:, 0] == "NOTE"].iloc[0, 1]

# Get the column headers
headers = list(df.columns)

# Create a single figure with three subplots (the third one is for the text box)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [1, 1, 0.2]})

# Extract data from columns 2, 3, 4, and 5
x_data = df.iloc[:, 0] - df.iloc[0, 0]  # First column as x-axis
y_data1 = df.iloc[:, 1]  # Second column for the first graph
y_data2 = df.iloc[:, 3]  # Fourth column for the second graph
y_data3 = df.iloc[:, 2]  # Third column for the third graph
y_data4 = df.iloc[:, 4]  # Fifth column for the fourth graph

lst = x_data
# Calculate info like average fps and max and min
average_time = (sum(abs(lst[i] - lst[i - 1]) for i in range(1, len(lst)))) / (len(lst) - 1)
fps = 1 / average_time
data_range = []
for data in [y_data1, y_data2, y_data3, y_data4]:
    data_range.append(max(data[int(len(data)//-2):]) - min(data[int(len(data)//-2):]))

infotext = f"Range {headers[1]}: {data_range[0]}; Range {headers[2]}: {data_range[2]}\nRange {headers[3]}: {data_range[1]:.2f}; Range {headers[4]}: {data_range[3]:.2f}\nAverage FPS:{fps:.2f}"



# Plot the first graph on the top subplot
ax1.plot(x_data, y_data1, label=headers[1])
ax1.plot(x_data, y_data2, label=headers[3])
ax1.set_ylabel("Pixels")
ax1.legend()
ax1.grid()

# Plot the second graph on the middle subplot
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
ax2.set_xlim(min(x_data), max(x_data))

# Set the title for the entire sheet
fig.suptitle(file_name + ".xlsx", fontsize=16)

# Use the third subplot ax3 for the text box, remove its axes
ax3.axis('off')
ax3.text(0.5, 0.5, str(note_cell) + f"\n{infotext}", ha='center', va='center', fontsize=12, wrap=True)

# Adjust spacing between subplots
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect as necessary

# Save the entire sheet plot to a file with the same name as the Excel file
plt.savefig(os.path.join(script_directory, f"{file_name}.png"))

# Show the plot
plt.show()
