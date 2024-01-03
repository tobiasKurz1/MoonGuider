import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
button_pin = 17  # Change this to the actual GPIO pin you've connected the button to
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
