"""
Project: AI-Powered Physics Pipe Simulation
Step 1: Plot a simple sine wave to test setup.

Author: [Your Name]
Date: [Today's Date]
"""

# ---------- IMPORT LIBRARIES ----------
import numpy as np
import matplotlib.pyplot as plt

# ---------- GENERATE DATA ----------
# Create x values (position or angle)
x = np.linspace(0, 2 * np.pi, 1000)

# Create a simple sine wave
y = np.sin(x)

# ---------- PLOT ----------
plt.figure(figsize=(8, 3))
plt.plot(x, y, 'b-', label='Sine Wave')
plt.axhline(0, color='black', linewidth=0.8)
plt.title("Step 1: Test Sine Wave")
plt.xlabel("x (position)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()
