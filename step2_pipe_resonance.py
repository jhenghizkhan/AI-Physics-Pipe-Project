import numpy as np
import matplotlib.pyplot as plt

def pipe_resonance(pipe_type='open', length=1.0, harmonic=1, v=343):
    x = np.linspace(0, length, 1000)
    if pipe_type == 'open':
        wavelength = 2 * length / harmonic
    elif pipe_type == 'closed':
        wavelength = 4 * length / harmonic
    else:
        raise ValueError("pipe_type must be 'open' or 'closed'")
    frequency = v / wavelength
    k = 2 * np.pi / wavelength
    y = np.sin(k * x)
    return x, y, frequency

# Open pipe, 2nd harmonic
x1, y1, f1 = pipe_resonance('open', 1.0, 2)
# Closed pipe, 1st harmonic
x2, y2, f2 = pipe_resonance('closed', 1.0, 1)

# Plot both waves together
plt.figure(figsize=(10,4))
plt.plot(x1, y1, 'b-', label=f'Open Pipe, 2nd Harmonic, f={f1:.2f}Hz')
plt.plot(x2, y2, 'r--', label=f'Closed Pipe, 1st Harmonic, f={f2:.2f}Hz')
plt.axhline(0, color='black', linewidth=0.8)
plt.title("Open vs Closed Pipe Standing Waves")
plt.xlabel("Position along pipe (m)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()
