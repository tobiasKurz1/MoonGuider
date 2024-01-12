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
file_name = "log_24-01-11_15-50"
excel_file = file_name + ".xlsx"

####
"""



# Read the selected Excel file into a DataFrame
df = pd.read_excel(excel_file, sheet_name=0, engine='openpyxl')  # First sheet for the data

df2 = pd.read_excel(excel_file, sheet_name=1, engine='openpyxl')  # Second sheet for the data

# Get the text from the "NOTE" cell in the second sheet
notes_df = pd.read_excel(excel_file, sheet_name=2, engine='openpyxl')  # Third sheet for the note
note_cell = notes_df.loc[notes_df.iloc[:, 0] == "NOTE"].iloc[0, 1]

# Get the column headers
headers = list(df.columns)
headers2 = list(df2.columns)

# Create a single figure with three subplots (the third one is for the text box)
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(19, 17), gridspec_kw={'height_ratios': [1, 0.3, 1, 0.3, 0.2]})
bar_width = 0.1


# Extract data from columns 2, 3, 4, and 5
x_data = df.iloc[:, 0] - df.iloc[0, 0]  # First column as x-axis
y_data1 = df.iloc[:, 1]  # Second column for the first graph
y_data2 = df.iloc[:, 3]  # Fourth column for the second graph
y_data3 = df.iloc[:, 2]  # Third column for the third graph
y_data4 = df.iloc[:, 4]  # Fifth column for the fourth graph
x_dev = df.iloc[:, 5]  # ax6
y_dev = df.iloc[:, 6]  # ax7

lst = x_data
# Calculate info like average fps and max and min
average_time = (sum(abs(lst[i] - lst[i - 1]) for i in range(1, len(lst)))) / (len(lst) - 1)
fps = 1 / average_time
data_range = []
for data in [y_data1, y_data2, y_data3, y_data4]:
    data_range.append(max(data[int(len(data)//-2):]) - min(data[int(len(data)//-2):]))

infotext = f"Range {headers[1]}: {data_range[0]}; Range {headers[2]}: {data_range[2]}\nRange {headers[3]}: {data_range[1]:.2f}; Range {headers[4]}: {data_range[3]:.2f}\nAverage FPS:{fps:.2f}"

# get activity data
x_data2 = df2.iloc[:, 0] - df2.iloc[0, 0] # x-Axis of activity data
y_duration = df2.iloc[:, 1]
y_direction = df2.iloc[:, 2]
ud_x = []
ud_duration = []
ud_direction = []
rl_x = []
rl_duration = []
rl_direction = []

for x, y_dur, y_dir in zip(x_data2, y_duration, y_direction):
    if y_dir in ['right', 'left']:
        rl_x.append(x)
        rl_duration.append(y_dur)
        rl_direction.append(y_dir)
    else:
        ud_x.append(x)
        ud_duration.append(y_dur)
        ud_direction.append(y_dir)
        

# Plot the first graph on the top subplot
ax1.plot(x_data, y_data1, label=headers[1], alpha = 0.3)
ax1.plot(x_data, y_data2, label=headers[3])
ax1.set_ylabel("Pixels")

max_abs_y = max(abs(min(min(list(x_dev),list(y_dev)))), abs(max(max(list(x_dev), list(y_dev)))))
ax6 = ax1.twinx()
ax6.plot(x_data, x_dev, label=headers[5])
ax6.set_ylabel("Pixels")
ax6.set_ylim(-max_abs_y, max_abs_y)
ax6.set_yscale('symlog')

ax1.legend()
ax6.grid()

# Plot the first activity graph
bars1 = ax2.bar(rl_x, rl_duration, width=bar_width, color=['red' if d == 'right' else 'blue' for d in rl_direction])
ax2.set_xlabel(headers2[0] + " [s]")
ax2.set_ylabel(headers2[1] + " [s]")
legend_elements1 = [
    plt.Line2D([0], [0], color='red', lw=4, label='Right'),
    plt.Line2D([0], [0], color='blue', lw=4, label='Left')]
ax2.legend(handles=legend_elements1)
ax2.grid()
ax2.grid(axis='x')

#ax2.set_title('Custom Width Bar Chart for ax2')

# Plot the second activity graph
bars2 = ax4.bar(ud_x, ud_duration, width=bar_width, color=['red' if d == 'down' else 'blue' for d in ud_direction])
ax4.set_xlabel(headers2[0] + " [s]")
ax4.set_ylabel(headers2[1] + " [s]")
legend_elements2 = [
    plt.Line2D([0], [0], color='red', lw=4, label='Down'),
    plt.Line2D([0], [0], color='blue', lw=4, label='Up')]
ax4.legend(handles=legend_elements2)
ax4.grid(axis='x')
#ax4.set_title('Custom Width Bar Chart for ax2')


# Plot the second graph on the second big subplot
ax3.plot(x_data, y_data3, label=headers[2], alpha = 0.3)
ax3.plot(x_data, y_data4, label=headers[4])
ax3.set_xlabel(headers[0] + " [s]")
ax3.set_ylabel("Pixels")

ax7 = ax3.twinx()
ax7.plot(x_data, y_dev, label=headers[6])
ax7.set_ylabel("Pixels")
ax7.set_ylim(-max_abs_y, max_abs_y)
ax7.set_yscale('symlog')


ax3.legend()
ax7.grid()

# Automatically adjust y-axis limits for both subplots
ax1.set_ylim(min(min(y_data1), min(y_data2)), max(max(y_data1), max(y_data2)))
ax3.set_ylim(min(min(y_data3), min(y_data4)), max(max(y_data3), max(y_data4)))
ax1.set_xlim(min(x_data), max(x_data))
ax2.set_xlim(min(x_data), max(x_data))
ax3.set_xlim(min(x_data), max(x_data))
ax4.set_xlim(min(x_data), max(x_data))

# Set the title for the entire sheet
fig.suptitle(file_name + ".xlsx", fontsize=16)

# Use the third subplot ax3 for the text box, remove its axes
ax5.axis('off')
ax5.text(0.5, 0.5, str(note_cell) + f"\n{infotext}", ha='center', va='center', fontsize=12, wrap=True)

# Adjust spacing between subplots
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect as necessary

# Save the entire sheet plot to a file with the same name as the Excel file
plt.savefig(os.path.join(script_directory, f"{file_name}.png"))

# Show the plot
plt.show()
