import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons, CheckButtons
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import random
from colorsys import hls_to_rgb
from PyQt5.QtWidgets import QFileDialog, QApplication
import pickle

# Global states
TRACE_ENABLED = False
RECORD_ENABLED = False
DATA_POINTS_ENABLED = False
PLOTTING_ENABLED = True
LAST_DATA = None
CURRENT_COLORS = []
DATA_TO_REDO = []
ALL_PLOTS = []
SHAPE_INFLUENCE = None
AXIS_INFLUENCE = "spiral"
LAST_POSITION = None
DARK_MODE = False

def get_complementary_colors():
    h = random.random()
    colors = []
    for i in range(3):
        l = random.uniform(0.5, 0.75)
        s = 0.95
        rgb = hls_to_rgb((h + i / 2.5) % 1, l, s)
        colors.append(rgb)
    return colors

def get_axis_multiplier(theta):
    if AXIS_INFLUENCE == "spiral":
        return theta
    elif AXIS_INFLUENCE == "random":
        return np.sin(random.randint(1, 100) * theta)
    return theta

def plot_spiral(ax, continue_from=None):
    global LAST_DATA, CURRENT_COLORS, DATA_TO_REDO, ALL_PLOTS, SHAPE_INFLUENCE, AXIS_INFLUENCE, LAST_POSITION

    if not RECORD_ENABLED:
        ax.clear()
        ALL_PLOTS = []

    random_multiplier = random.randint(1, 100)
    theta = np.linspace(0 if not continue_from else continue_from, 8 * np.pi, 20000)
    axis_multiplier = get_axis_multiplier(theta)

    if SHAPE_INFLUENCE == 'circle':
        r = np.sin(random_multiplier * axis_multiplier)
    elif SHAPE_INFLUENCE == 'square':
        r = np.sign(np.sin(random_multiplier * axis_multiplier))
    elif SHAPE_INFLUENCE == 'triangle':
        r = np.abs(np.sin(random_multiplier * axis_multiplier))
    else:
        r = np.sin(random_multiplier * axis_multiplier) * np.exp(-theta / 10)

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.linspace(0, 10, len(theta))

    colors = CURRENT_COLORS if CURRENT_COLORS else get_complementary_colors()
    CURRENT_COLORS = colors
    DATA_TO_REDO = []

    segments = len(x) // 100
    for i in range(0 if not LAST_POSITION else LAST_POSITION, len(x), segments):
        if not PLOTTING_ENABLED:
            LAST_POSITION = i
            break
        segment_end = i + segments if i + segments < len(x) else len(x)
        if DATA_POINTS_ENABLED:
            line, = ax.plot(x[i:segment_end], y[i:segment_end], z[i:segment_end], 'o', color=colors[int(3 * i/len(x))], markersize=1)
        else:
            line, = ax.plot(x[i:segment_end], y[i:segment_end], z[i:segment_end], color=colors[int(3 * i/len(x))])
        ALL_PLOTS.append(line)
        DATA_TO_REDO.append(line)
        plt.pause(0.02)

    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))
    ax.axis('off')

    LAST_DATA = (x, y, z)
    plt.draw()

def update_color_button(event):
    global CURRENT_COLORS
    CURRENT_COLORS = get_complementary_colors()
    for i, rect in enumerate(color_button_ax.patches):
        rect.set_facecolor(CURRENT_COLORS[i])
    fig.canvas.draw()

def next_pattern(event):
    global PLOTTING_ENABLED, DATA_TO_REDO, LAST_POSITION
    DATA_TO_REDO = []
    PLOTTING_ENABLED = True
    LAST_POSITION = None
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

def toggle_data_points(event):
    global DATA_POINTS_ENABLED
    DATA_POINTS_ENABLED = not DATA_POINTS_ENABLED
    if DATA_POINTS_ENABLED:
        data_points_button.label.set_text('Line\nTrail')
    else:
        data_points_button.label.set_text('Dot\nTrail')
    fig.canvas.draw()

def stop_plotting(event):
    global PLOTTING_ENABLED, LAST_POSITION
    PLOTTING_ENABLED = not PLOTTING_ENABLED
    if PLOTTING_ENABLED:
        stop_button.label.set_text('STOP')
        plot_spiral(ax, continue_from=LAST_POSITION)
    else:
        stop_button.label.set_text('RESUME')
    fig.canvas.draw()

def undo(event):
    if DATA_TO_REDO:
        removed = DATA_TO_REDO.pop()
        removed.remove()
        plt.draw()

def reset(event):
    global TRACE_ENABLED, RECORD_ENABLED, DATA_POINTS_ENABLED, PLOTTING_ENABLED, LAST_DATA, CURRENT_COLORS, ALL_PLOTS, LAST_POSITION
    TRACE_ENABLED = False
    RECORD_ENABLED = False
    DATA_POINTS_ENABLED = False
    PLOTTING_ENABLED = True
    LAST_DATA = None
    CURRENT_COLORS = []
    for plot in ALL_PLOTS:
        plot.remove()
    ALL_PLOTS = []
    LAST_POSITION = None
    ax.clear()
    ax.axis('off')
    plt.draw()

def print_plot(event):
    app = QApplication([])
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(None, "Save Plot", "", "PDF Files (*.pdf);;All Files (*)", options=options)
    if filename:
        plt.savefig(filename)
    app.quit()

def save_data(event):
    app = QApplication([])
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(None, "Save Plot Data", "", "Pickle Files (*.pkl);;All Files (*)", options=options)
    if filename:
        with open(filename, 'wb') as f:
            pickle.dump({
                'plots': ALL_PLOTS,
                'last_data': LAST_DATA,
                'colors': CURRENT_COLORS
            }, f)
    app.quit()

def load_data(event):
    app = QApplication([])
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(None, "Load Plot Data", "", "Pickle Files (*.pkl);;All Files (*)", options=options)
    if filename:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            global LAST_DATA, CURRENT_COLORS, ALL_PLOTS
            for plot in ALL_PLOTS:
                plot.remove()
            ALL_PLOTS = data['plots']
            LAST_DATA = data['last_data']
            CURRENT_COLORS = data['colors']
            plot_spiral(ax)
    app.quit()

def on_slider_val_change(val):
    factor = 1 / slider.val
    ax.set_xlim(min(LAST_DATA[0]) * factor, max(LAST_DATA[0]) * factor)
    ax.set_ylim(min(LAST_DATA[1]) * factor, max(LAST_DATA[1]) * factor)
    ax.set_zlim(min(LAST_DATA[2]) * factor, max(LAST_DATA[2]) * factor)
    plt.draw()

def shape_influence(label):
    global SHAPE_INFLUENCE
    SHAPE_INFLUENCE = label if SHAPE_INFLUENCE != label else None
    if SHAPE_INFLUENCE is None:
        shape_buttons.set_active(-1)
    plot_spiral(ax)

def toggle_dark_mode(label):
    global DARK_MODE
    DARK_MODE = not DARK_MODE
    fig.set_facecolor('black' if DARK_MODE else 'white')
    ax.set_facecolor('black' if DARK_MODE else 'white')
    fig.canvas.draw()

def toggle_axis_influence(label):
    global AXIS_INFLUENCE
    AXIS_INFLUENCE = label if AXIS_INFLUENCE != label else "spiral"
    if AXIS_INFLUENCE == "spiral":
        axis_buttons.set_active(0)
    else:
        axis_buttons.set_active(1)
    plot_spiral(ax)

number_of_buttons = 11
button_width = 0.07
button_spacing = (0.9 - number_of_buttons * button_width) / (number_of_buttons + 1)
button_positions = [button_spacing + i * (button_width + button_spacing) for i in range(number_of_buttons)]

# Create figure and axes
gs = GridSpec(4, 1, height_ratios=[1, 0.1, 0.1, 0.1])
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(gs[0], projection='3d')
ax.axis('off')
fig.set_facecolor('white')

pattern_button_ax = plt.axes([button_positions[0], 0.25, button_width, 0.075])
pattern_button = Button(pattern_button_ax, 'NEXT\nPATTERN')
pattern_button.on_clicked(next_pattern)

record_button_ax = plt.axes([button_positions[1], 0.25, button_width, 0.075])
record_button = Button(record_button_ax, 'LOCK\nPATTERN')
record_button.on_clicked(record)

trace_button_ax = plt.axes([button_positions[2], 0.25, button_width, 0.075])
trace_button = Button(trace_button_ax, 'TRACE')
trace_button.on_clicked(trace)

data_points_button_ax = plt.axes([button_positions[3], 0.25, button_width, 0.075])
data_points_button = Button(data_points_button_ax, 'Dot\nTrail')
data_points_button.on_clicked(toggle_data_points)

stop_button_ax = plt.axes([button_positions[4], 0.25, button_width, 0.075])
stop_button = Button(stop_button_ax, 'STOP')
stop_button.on_clicked(stop_plotting)

undo_button_ax = plt.axes([button_positions[5], 0.25, button_width, 0.075])
undo_button = Button(undo_button_ax, 'UNDO')
undo_button.on_clicked(undo)

color_button_ax = plt.axes([button_positions[6], 0.25, button_width, 0.075])
color_button = Button(color_button_ax, '')
color_button.on_clicked(update_color_button)

reset_button_ax = plt.axes([button_positions[7], 0.25, button_width, 0.075])
reset_button = Button(reset_button_ax, 'RESET')
reset_button.on_clicked(reset)

save_button_ax = plt.axes([button_positions[8], 0.25, button_width, 0.075])
save_button = Button(save_button_ax, 'SAVE')
save_button.on_clicked(save_data)

load_button_ax = plt.axes([button_positions[9], 0.25, button_width, 0.075])
load_button = Button(load_button_ax, 'LOAD')
load_button.on_clicked(load_data)

print_button_ax = plt.axes([button_positions[10], 0.25, button_width, 0.075])
print_button = Button(print_button_ax, 'PDF')
print_button.on_clicked(print_plot)

slider_ax = plt.axes([0.91, 0.2, 0.015, 0.7])
slider = Slider(slider_ax, 'Zoom', 0.1, 2.0, valinit=1.0, orientation='vertical')
slider.on_changed(on_slider_val_change)

CURRENT_COLORS = get_complementary_colors()
for i in range(3):
    rect = plt.Rectangle((0, i/3), 1, 1/3, facecolor=CURRENT_COLORS[i], transform=color_button_ax.transAxes)
    color_button_ax.add_patch(rect)

shape_button_ax = plt.axes([0.01, 0.35, 0.2, 0.15])
shape_buttons = RadioButtons(shape_button_ax, ('square', 'circle', 'triangle'), activecolor='blue', active=-1)
shape_buttons.on_clicked(shape_influence)

axis_button_ax = plt.axes([0.01, 0.53, 0.2, 0.1])
axis_buttons = RadioButtons(axis_button_ax, ('spiral', 'random'), activecolor='green')
axis_buttons.on_clicked(toggle_axis_influence)

dark_mode_check = CheckButtons(plt.axes([0.01, 0.95, 0.15, 0.08]), ['Dark Mode'], [False])
dark_mode_check.labels[0].set_size(10)
dark_mode_check.on_clicked(toggle_dark_mode)

plot_spiral(ax)
plt.show()
