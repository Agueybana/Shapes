# 🎨 Shapes - Interactive Spiral Pattern Generator

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-v3.0+-orange.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Overview

**Shapes** is a collection of interactive Python scripts that generate beautiful, customizable spiral patterns in both 2D and 3D. These scripts utilize mathematical formulas to create mesmerizing visualizations with real-time controls for pattern manipulation, color schemes, and export capabilities.

## 📋 Table of Contents
- [Features](#-features)
- [Scripts Overview](#-scripts-overview)
- [Installation](#-installation)
- [Usage](#-usage)
- [Script Details](#-script-details)
- [Controls Guide](#-controls-guide)
- [Examples](#-examples)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

### 🎯 Core Features
- **Real-time Pattern Generation** - Watch patterns form dynamically
- **Interactive Controls** - Manipulate patterns on-the-fly
- **2D/3D Visualization** - Switch between dimensions seamlessly
- **Custom Color Schemes** - Generate complementary color palettes
- **Export Capabilities** - Save as PDF or pickle data files
- **Dark Mode Support** - Easy on the eyes
- **Shape Influences** - Apply geometric transformations

### 🎮 Control Features
- Pattern randomization
- Animation pause/resume
- Zoom controls
- Trail options (dots/lines)
- Pattern locking
- Undo functionality

## 📚 Scripts Overview

| Script | Dimension | Features | Complexity |
|--------|-----------|----------|------------|
| `Shapes.py` | 2D | Basic spiral with replay | ⭐ |
| `Shapes_v2.py` | 2D | Enhanced controls, traces | ⭐⭐ |
| `Shapes_v4_3D.py` | 3D | Basic 3D with file dialog | ⭐⭐ |
| `Shapes_v5_3D.py` | 3D | Save/load, zoom slider | ⭐⭐⭐ |
| `Shapes_v6_3D.py` | 3D | Shape influences, dark mode | ⭐⭐⭐⭐ |
| `Shapes_v7_3D.py` | 3D | Improved pause/resume | ⭐⭐⭐⭐ |
| `Shapes_3D2D_merge_v1.py` | 2D/3D | Dimension switching | ⭐⭐⭐⭐ |
| `Shapes_3D2D_merge_v5.py` | 2D/3D | All features combined | ⭐⭐⭐⭐⭐ |

## 🚀 Installation

### Prerequisites
```bash
# Ensure Python 3.7+ is installed
python --version

# Install required packages
pip install numpy matplotlib PyQt5
```

### Clone Repository
```bash
git clone https://github.com/Agueybana/Shapes.git
cd Shapes
```

## 💻 Usage

### Basic Usage
Run any script directly:
```bash
python Shapes.py
```

### Examples for Each Script

#### 1️⃣ **Shapes.py** - Basic Spiral Generator
```bash
python Shapes.py
```
- **Default Settings**: Random spiral pattern, full-screen mode
- **Controls**: REPLAY button only
- **Key Features**: Simple, clean interface for quick pattern generation

#### 2️⃣ **Shapes_v2.py** - Enhanced 2D Generator
```bash
python Shapes_v2.py
```
- **Default Settings**: Random pattern, complementary colors, animation enabled
- **Controls**: 9 interactive buttons
- **Key Features**: Trace mode, pattern locking, color customization

#### 3️⃣ **Shapes_v4_3D.py** - Basic 3D Visualizer
```bash
python Shapes_v4_3D.py
```
- **Default Settings**: 3D spiral with z-axis progression
- **Controls**: Standard control panel with PDF export
- **Key Features**: PyQt5 file dialog for saving

#### 4️⃣ **Shapes_v5_3D.py** - Advanced 3D with Save/Load
```bash
python Shapes_v5_3D.py
```
- **Default Settings**: 3D spiral with persistence options
- **Controls**: 11 buttons including save/load
- **Key Features**: Zoom slider, pickle file support

#### 5️⃣ **Shapes_v6_3D.py** - Shape-Influenced 3D
```bash
python Shapes_v6_3D.py
```
- **Default Settings**: Standard spiral, shape influences available
- **Controls**: Shape selectors (square/circle/triangle)
- **Key Features**: Axis influence options, dark mode checkbox

#### 6️⃣ **Shapes_v7_3D.py** - Refined 3D Generator
```bash
python Shapes_v7_3D.py
```
- **Default Settings**: Improved animation handling
- **Controls**: Streamlined button layout
- **Key Features**: Better pause/resume logic

#### 7️⃣ **Shapes_3D2D_merge_v1.py** - Dimension Switcher
```bash
python Shapes_3D2D_merge_v1.py
```
- **Default Settings**: Starts in 3D mode
- **Controls**: "Switch to 2D/3D" toggle button
- **Key Features**: Seamless dimension switching

#### 8️⃣ **Shapes_3D2D_merge_v5.py** - Ultimate Generator
```bash
python Shapes_3D2D_merge_v5.py
```
- **Default Settings**: Full feature set enabled
- **Controls**: Complete control panel
- **Key Features**: All features from previous versions combined

## 🎛️ Controls Guide

### 🔘 Button Controls

| Button | Function | Description |
|--------|----------|-------------|
| **NEXT PATTERN** | Generate new pattern | Creates a random spiral with new parameters |
| **LOCK PATTERN** | Toggle pattern lock | Prevents clearing when generating new patterns |
| **TRACE** | Toggle trace mode | Shows pattern formation path |
| **Dot Trail** | Toggle trail style | Switches between dots and continuous lines |
| **STOP/RESUME** | Pause animation | Halts/continues pattern generation |
| **UNDO** | Remove last segment | Removes the most recent pattern segment |
| **Color Block** | New color scheme | Generates complementary colors |
| **RESET** | Clear canvas | Removes all patterns and resets state |
| **SAVE** | Save pattern data | Exports to .pkl file |
| **LOAD** | Load pattern data | Imports from .pkl file |
| **PDF** | Export to PDF | Saves current view as PDF |

### 🎚️ Additional Controls

- **Zoom Slider**: Adjust view scale (0.1x to 2.0x)
- **Shape Influence**: Apply geometric transformations
  - Square: Angular transformation
  - Circle: Circular transformation
  - Triangle: Triangular transformation
- **Dark Mode**: Toggle dark background
- **Switch to 2D/3D**: Change visualization dimension

## 📊 Script Details

### Core Functions

#### `get_complementary_colors()`
Generates a harmonious color palette using HLS color space:
```python
- Base hue: Random (0-1)
- Lightness: 0.5-0.75
- Saturation: 0.95
- Returns: List of 3 RGB color tuples
```

#### `plot_spiral(ax, continue_from=None)`
Main pattern generation function:
```python
- Parameters:
  - ax: Matplotlib axes object
  - continue_from: Resume point for paused animations
- Algorithm: r = sin(multiplier * θ) * e^(-θ/10)
- Segments: 100 animation steps
```

### Mathematical Formulas

**Basic Spiral**:
```
x = r * cos(θ)
y = r * sin(θ)
z = linear_space(0, 10, len(θ))  # For 3D
```

**Shape Influences**:
- Circle: `r = sin(multiplier * θ)`
- Square: `r = sign(sin(multiplier * θ))`
- Triangle: `r = |sin(multiplier * θ)|`
- Default: `r = sin(multiplier * θ) * e^(-θ/10)`

## 🖼️ Examples

### Command Examples

**Generate a simple 2D spiral:**
```bash
python Shapes.py
```

**Create a 3D spiral with save capability:**
```bash
python Shapes_v5_3D.py
# Click 'NEXT PATTERN' to generate
# Click 'SAVE' to export pattern data
# Click 'PDF' to export visual
```

**Work with shape influences:**
```bash
python Shapes_v6_3D.py
# Select 'circle' for smooth curves
# Select 'square' for angular patterns
# Select 'triangle' for pointed shapes
```

**Switch between 2D and 3D:**
```bash
python Shapes_3D2D_merge_v5.py
# Click 'Switch to 2D' for flat view
# Click 'Switch to 3D' for depth view
```

## 📦 Requirements

### Python Dependencies
```
numpy>=1.19.0
matplotlib>=3.3.0
PyQt5>=5.15.0
```

### System Requirements
- Python 3.7 or higher
- GUI environment (not suitable for headless systems)
- Minimum 4GB RAM recommended
- OpenGL support for 3D rendering

## 🔧 Troubleshooting

### Common Issues

**1. Import Error for PyQt5**
```bash
# Solution:
pip install --upgrade PyQt5
```

**2. Matplotlib Backend Issues**
```bash
# Set backend explicitly:
export MPLBACKEND=Qt5Agg
```

**3. Slow Performance**
- Reduce pattern complexity
- Close other applications
- Use 2D mode for better performance

**4. File Dialog Not Opening**
- Ensure PyQt5 is properly installed
- Check file system permissions
- Try running with administrator privileges

### Performance Tips
- Use 'STOP' to pause complex patterns
- Clear patterns with 'RESET' before generating new ones
- Disable 'Dot Trail' for smoother animation
- Use lower zoom values for better performance

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for:
- New shape algorithms
- Additional color schemes
- Performance improvements
- UI enhancements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Created with ❤️ using:
- **NumPy** for mathematical computations
- **Matplotlib** for visualization
- **PyQt5** for file dialogs
- Mathematical inspiration from spiral geometry

---

**Happy Pattern Making! 🌀**
