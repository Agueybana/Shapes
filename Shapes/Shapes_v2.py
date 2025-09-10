import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
import random
from colorsys import hls_to_rgb

# Global states
TRACE_ENABLED = False
RECORD_ENABLED = False
DATA_POINTS_ENABLED = False
PLOTTING_ENABLED = True
LAST_DATA = None
CURRENT_COLORS = []
DATA_TO_UNDO = []

def get_complementary_colors():
    h = random.random()
    colors = []
    for i in range(3):
        l = random.uniform(0.5, 0.75)
        s = 0.95
        rgb = hls_to_rgb((h + i / 2.5) % 1, l, s)
        colors.append(rgb)
    return colors

def plot_spiral(ax):
    global LAST_DATA, CURRENT_COLORS, DATA_TO_UNDO
    if not RECORD_ENABLED:
        ax.clear()

    random_multiplier = random.randint(1, 100)
    theta = np.linspace(0, 8 * np.pi, 20000)
    r = np.sin(random_multiplier * theta) * np.exp(-theta / 10)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    colors = CURRENT_COLORS if CURRENT_COLORS else get_complementary_colors()
    CURRENT_COLORS = colors
    cmap = ListedColormap(colors)

    DATA_TO_UNDO = []

    scatter = ax.scatter(x[:1], y[:1], s=5, c=theta[:1], cmap=cmap)
    ax.axis('equal')
    ax.axis('off')

    split_size = len(theta) // 500
    for i in range(1, len(theta), split_size):
        if not PLOTTING_ENABLED:
            break
        scatter.set_offsets(np.c_[x[i:i + split_size], y[i:i + split_size]])
        scatter.set_array(theta[i:i + split_size])
        if TRACE_ENABLED:
            line, = ax.plot(x[i - 1:i + split_size], y[i - 1:i + split_size], color=colors[i % 3], linewidth=0.5)
            DATA_TO_UNDO.append(line)
        if DATA_POINTS_ENABLED:
            sc = ax.scatter(x[i:i + split_size], y[i:i + split_size], s=5, c=theta[i:i + split_size], cmap=cmap)
            DATA_TO_UNDO.append(sc)
        plt.pause(0.02)

    LAST_DATA = (x, y, theta)
    DATA_TO_UNDO.append(scatter)
    update_color_button()
    plt.draw()

def update_color_button():
    for i, rect in enumerate(color_button_ax.patches):
        rect.set_facecolor(CURRENT_COLORS[i])

def next_pattern(event):
    global PLOTTING_ENABLED, DATA_TO_UNDO
    DATA_TO_UNDO = []
    PLOTTING_ENABLED = True
    plot_spiral(ax)

def trace(event):
    global TRACE_ENABLED
    TRACE_ENABLED = not TRACE_ENABLED
    trace_button.color = '0.85'
    fig.canvas.draw()

def record(event):
    global RECORD_ENABLED
    RECORD_ENABLED = not RECORD_ENABLED
    record_button.color = 'green' if RECORD_ENABLED else '0.85'
    fig.canvas.draw()

def new_color(event):
    global CURRENT_COLORS
    CURRENT_COLORS = get_complementary_colors()
    update_color_button()

def toggle_data_points(event):
    global DATA_POINTS_ENABLED
    DATA_POINTS_ENABLED = not DATA_POINTS_ENABLED
    data_points_button.color = '0.85'
    fig.canvas.draw()

def stop_plotting(event):
    global PLOTTING_ENABLED
    PLOTTING_ENABLED = not PLOTTING_ENABLED
    stop_button.label.set_text('RESUME' if not PLOTTING_ENABLED else 'STOP')
    fig.canvas.draw()

def undo(event):
    for obj in DATA_TO_UNDO:
        obj.remove()
    plt.draw()

def reset(event):
    global TRACE_ENABLED, RECORD_ENABLED, DATA_POINTS_ENABLED, PLOTTING_ENABLED, LAST_DATA, CURRENT_COLORS
    TRACE_ENABLED = False
    RECORD_ENABLED = False
    DATA_POINTS_ENABLED = False
    PLOTTING_ENABLED = True
    LAST_DATA = None
    CURRENT_COLORS = []
    ax.clear()
    ax.axis('off')
    plt.draw()

def print_plot(event):
    plt.savefig('temp_plot.png')
    plt.show()

number_of_buttons = 9
button_width = 0.08
button_spacing = (1.0 - number_of_buttons * button_width) / (number_of_buttons + 1)
button_positions = [button_spacing + i * (button_width + button_spacing) for i in range(number_of_buttons)]

# Create figure and axes
gs = GridSpec(2, 1, height_ratios=[1, 0.1])
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(gs[0])
ax.axis('off')

pattern_button_ax = plt.axes([button_positions[0], 0.01, button_width, 0.075])
pattern_button = Button(pattern_button_ax, 'NEXT\nPATTERN')
pattern_button.on_clicked(next_pattern)

record_button_ax = plt.axes([button_positions[1], 0.01, button_width, 0.075])
record_button = Button(record_button_ax, 'LOCK\nPATTERN')
record_button.on_clicked(record)

trace_button_ax = plt.axes([button_positions[2], 0.01, button_width, 0.075])
trace_button = Button(trace_button_ax, 'TRACE')
trace_button.on_clicked(trace)

data_points_button_ax = plt.axes([button_positions[3], 0.01, button_width, 0.075])
data_points_button = Button(data_points_button_ax, 'Dot\nTrail')
data_points_button.on_clicked(toggle_data_points)

stop_button_ax = plt.axes([button_positions[4], 0.01, button_width, 0.075])
stop_button = Button(stop_button_ax, 'STOP')
stop_button.on_clicked(stop_plotting)

undo_button_ax = plt.axes([button_positions[5], 0.01, button_width, 0.075])
undo_button = Button(undo_button_ax, 'UNDO')
undo_button.on_clicked(undo)

color_button_ax = plt.axes([button_positions[6], 0.01, button_width, 0.075])
color_button = Button(color_button_ax, '')
color_button.on_clicked(new_color)

reset_button_ax = plt.axes([button_positions[7], 0.01, button_width, 0.075])
reset_button = Button(reset_button_ax, 'RESET')
reset_button.on_clicked(reset)

print_button_ax = plt.axes([button_positions[8], 0.01, button_width, 0.075])
print_button = Button(print_button_ax, 'PRINT')
print_button.on_clicked(print_plot)

CURRENT_COLORS = get_complementary_colors()
for i in range(3):
    rect = plt.Rectangle((0, i/3), 1, 1/3, facecolor=CURRENT_COLORS[i], transform=color_button_ax.transAxes)
    color_button_ax.add_patch(rect)

plot_spiral(ax)
plt.show()
