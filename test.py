#import RPi.GPIO as GPIO
import pandas as pd
import time


data = ['asd','ffe','fef']
data2 = ['2asd','2ffe','2fef']
# Your existing dataframe
df1 = pd.DataFrame(data)

# Create a second dataframe for the new data
# Replace this with your actual data for the second sheet
df2 = pd.DataFrame(data2)

# Filename for the Excel file
filename = "your_filename_here"

# Using ExcelWriter to write to multiple sheets
with pd.ExcelWriter(f"Logs/{filename}.xlsx", engine='openpyxl') as writer:
    # Write the first dataframe to the first sheet
    df1.to_excel(writer, sheet_name=f'{time.ctime()[0:10]}', index=False, header=False)

    # Write the second dataframe to the second sheet
    # Replace 'SecondSheet' with your desired sheet name
    df2.to_excel(writer, sheet_name='SecondSheet', index=False, header=False)







"""
import config_loader as load

config = load.configuration()

#config.print_config()

if config.export_to_excel:
    print("lol")



"""





"""
# Set up GPIO
GPIO.setmode(GPIO.BCM)
button_pin = 16  # Change this to the actual GPIO pin you've connected the button to
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button pressed!")

# Set up event detection
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Press Ctrl+C to exit")
    while True:
        # Your main program can run here
        pass

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()
"""