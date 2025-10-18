import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

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

# Parameters
pipe1 = ('open', 1.0, 2)    # Open pipe, 2nd harmonic
pipe2 = ('closed', 1.0, 1)  # Closed pipe, 1st harmonic

x1, k1, f1 = standing_wave(*pipe1)
x2, k2, f2 = standing_wave(*pipe2)

# Figure
fig, ax = plt.subplots(figsize=(12,5))
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel("Position along pipe (m)")
ax.set_ylabel("Amplitude")
ax.set_title("Open and Closed Pipe Standing Waves with Pipe Drawing")
ax.axhline(0, color='black', linewidth=0.8)
ax.grid(True)

# Draw pipes
ax.add_patch(Rectangle((0, -0.1), pipe1[1], 0.2, fill=False, edgecolor='blue', linewidth=2, label='Open Pipe'))
ax.add_patch(Rectangle((0, -1.3), pipe2[1], 0.2, fill=False, edgecolor='red', linewidth=2, label='Closed Pipe'))

# Lines for waves
line1, = ax.plot([], [], 'b-', linewidth=2)
line2, = ax.plot([], [], 'r--', linewidth=2)

ax.legend()

# Animation
def animate(t):
    line1.set_data(x1, np.sin(k1*x1) * np.cos(2*np.pi*f1*t) + 0.0)   # open pipe wave at y=0
    line2.set_data(x2, np.sin(k2*x2) * np.cos(2*np.pi*f2*t) - 1.2)   # closed pipe wave shifted down
    return line1, line2

anim = FuncAnimation(fig, animate, frames=np.linspace(0,0.02,200), interval=50, blit=True)
plt.show()
