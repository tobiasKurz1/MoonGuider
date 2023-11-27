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
    
    xs = x[-buff:]
    y1s = y1[-buff:]
    y2s = y2[-buff:]
    
    
    # Draw x and y lists
    ax.clear()
    ax.plot(xs, y1s, label="y1")
    ax.plot(xs, y2s, label="y2")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TEst')
    plt.ylabel('Values')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(x, y1, y2), interval=500)
plt.show()

while True:
    x.append(time.ctime())
    y1.append(np.random.random())
    y2.append(np.random.random())
