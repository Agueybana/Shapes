import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random

def plot_spiral(ax, color_map='viridis'):
    ax.clear()  # Clear current axes

    # Generating a random number between 1 and 10
    random_multiplier = random.randint(1, 10)

    # Generating the data
    theta = np.linspace(0, 4 * np.pi, 10000)
    r = np.sin(random_multiplier * theta) * np.exp(-theta/10)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Plotting the graph
    split_size = len(theta) // 100
    for i in range(0, len(theta), split_size):
        ax.scatter(x[i:i+split_size], y[i:i+split_size], s=5, c=theta[i:i+split_size], cmap=color_map)
        ax.axis('equal')
        plt.pause(0.1)  # Pause for a brief moment between plot updates

    plt.draw()  # Redraw the figure

def replay(event):
    plot_spiral(ax)

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 7))
fig.canvas.manager.full_screen_toggle()  # Toggle full screen

# Position the button
replay_button_ax = plt.axes([0.8, 0.01, 0.1, 0.075])
replay_button = Button(replay_button_ax, 'REPLAY')
replay_button.on_clicked(replay)

# Plot the spiral for the first time
plot_spiral(ax)
plt.show()