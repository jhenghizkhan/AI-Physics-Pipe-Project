import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

# ---------- FUNCTION TO GENERATE STANDING WAVE ----------
def standing_wave(pipe_type='open', length=1.0, harmonic=1, v=343):
    x = np.linspace(0, length, 1000)
    if pipe_type == 'open':
        wavelength = 2 * length / harmonic
    elif pipe_type == 'closed':
        wavelength = 4 * length / harmonic
    else:
        raise ValueError("pipe_type must be 'open' or 'closed'")
    frequency = v / wavelength
    k = 2 * np.pi / wavelength
    return x, k, frequency

# ---------- PIPE PARAMETERS ----------
pipe_open = ('open', 1.0, 2)     # Open pipe, 2nd harmonic
pipe_closed = ('closed', 1.0, 1) # Closed pipe, 1st harmonic

x_open, k_open, f_open = standing_wave(*pipe_open)
x_closed, k_closed, f_closed = standing_wave(*pipe_closed)

# ---------- FIGURE SETUP ----------
fig, ax = plt.subplots(figsize=(12,5))
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-2, 2)
ax.set_xlabel("Position along pipe (m)")
ax.set_ylabel("Amplitude")
ax.set_title("Standing Waves Inside Open and Closed Pipes")
ax.axhline(0, color='black', linewidth=0.8)
ax.grid(True)

# ---------- DRAW PIPE RECTANGLES ----------
# Open pipe rectangle at y=0
rect_open = Rectangle((0, -0.2), pipe_open[1], 0.4, fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(rect_open)
# Closed pipe rectangle at y=-1.5
rect_closed = Rectangle((0, -1.7), pipe_closed[1], 0.4, fill=False, edgecolor='red', linewidth=2)
ax.add_patch(rect_closed)

# ---------- INIT LINES ----------
line_open, = ax.plot([], [], 'b-', linewidth=2, label='Open Pipe Wave')
line_closed, = ax.plot([], [], 'r-', linewidth=2, label='Closed Pipe Wave')
ax.legend()

# ---------- ANIMATION FUNCTION ----------
def animate(t):
    # Normalize wave amplitude to fit inside rectangle height
    amplitude_open = 0.2  # rectangle half-height
    amplitude_closed = 0.2
    
    y_open = amplitude_open * np.sin(k_open * x_open) * np.cos(2*np.pi*f_open*t)
    line_open.set_data(x_open, y_open)
    
    y_closed = amplitude_closed * np.sin(k_closed * x_closed) * np.cos(2*np.pi*f_closed*t) - 1.5
    line_closed.set_data(x_closed, y_closed)
    
    return line_open, line_closed

# ---------- CREATE ANIMATION ----------
anim = FuncAnimation(fig, animate, frames=np.linspace(0,0.02,200), interval=50, blit=True)
plt.show()
