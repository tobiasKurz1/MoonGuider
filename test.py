import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = []
y1 = []
y2 = []



# This function is called periodically from FuncAnimation
def animate(i, x, y1, y2):
    
    buff = 100
    
    x = x[-buff:]
    y1 = y1[-buff:]
    y2 = y2[-buff:]
    
    
    # Draw x and y lists
    ax.clear()
    ax.plot(x, y1, label="y1")
    ax.plot(x, y2, label="y2")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TEst')
    plt.ylabel('Values')
    plt.legend()

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(x, y1, y2), interval=500)
def update_data():
    x.append(time.ctime())
    y1.append(np.random.random())
    y2.append(np.random.random())


# Main loop to update data
while True:
    update_data()
    plt.pause(1)  # Adjust the pause duration as needed