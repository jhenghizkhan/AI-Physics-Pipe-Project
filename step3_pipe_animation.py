import numpy as np
import matplotlib.pyplot as plt
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

# ---------- PARAMETERS ----------
pipe1 = ('open', 1.0, 2)    # open pipe, 2nd harmonic
pipe2 = ('closed', 1.0, 1)  # closed pipe, 1st harmonic

x1, k1, f1 = standing_wave(*pipe1)
x2, k2, f2 = standing_wave(*pipe2)

# ---------- SETUP FIGURE ----------
fig, ax = plt.subplots(figsize=(10,4))
line1, = ax.plot([], [], 'b-', label=f'Open Pipe, 2nd Harmonic, f={f1:.2f}Hz')
line2, = ax.plot([], [], 'r--', label=f'Closed Pipe, 1st Harmonic, f={f2:.2f}Hz')
ax.set_xlim(0, max(pipe1[1], pipe2[1]))
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel("Position along pipe (m)")
ax.set_ylabel("Amplitude")
ax.set_title("Animated Standing Waves")
ax.axhline(0, color='black', linewidth=0.8)
ax.legend()
ax.grid(True)

# ---------- ANIMATION FUNCTION ----------
def animate(t):
    line1.set_data(x1, np.sin(k1*x1) * np.cos(2 * np.pi * f1 * t))
    line2.set_data(x2, np.sin(k2*x2) * np.cos(2 * np.pi * f2 * t))
    return line1, line2

# ---------- CREATE ANIMATION ----------
anim = FuncAnimation(fig, animate, frames=np.linspace(0, 0.02, 200), interval=50, blit=True)
plt.show()
