import pandas as pd
import matplotlib.pyplot as plt

# Define the filename of your Excel file
excel_file = "nicht_eingesteckt.xlsx"

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file, engine='openpyxl')

# Get the column headers
headers = list(df.columns)

# Extract data from columns 2, 3, 4, and 5
x_data = df.iloc[:, 0]  # First column as x-axis
y_data1 = df.iloc[:, 1]  # Second column for the first graph
y_data2 = df.iloc[:, 3]  # Fourth column for the second graph
y_data3 = df.iloc[:, 2]  # Third column for the third graph
y_data4 = df.iloc[:, 4]  # Fifth column for the fourth graph

# Create a single figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot the first graph on the top subplot
ax1.plot(x_data, y_data1, label=headers[1])
ax1.plot(x_data, y_data2, label=headers[3])
ax1.set_ylabel("Value")
ax1.set_title("First and Second Graph")
ax1.legend()
ax1.grid()

# Plot the second graph on the bottom subplot
ax2.plot(x_data, y_data3, label=headers[2])
ax2.plot(x_data, y_data4, label=headers[4])
ax2.set_xlabel(headers[0])
ax2.set_ylabel("Value")
ax2.set_title("Third and Fourth Graph")
ax2.legend()
ax2.grid()

# Automatically adjust y-axis limits for both subplots
ax1.set_ylim(min(min(y_data1), min(y_data2)), max(max(y_data1), max(y_data2)))
ax2.set_ylim(min(min(y_data3), min(y_data4)), max(max(y_data3), max(y_data4)))

plt.tight_layout()

# Show the plot
plt.show()