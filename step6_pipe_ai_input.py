import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import speech_recognition as sr

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

# ---------- FUNCTION TO PARSE INPUT ----------
def parse_input(text):
    text = text.lower()
    pipe_type = 'open' if 'open' in text else 'closed'
    
    import re

    # Find harmonic number (look for 1st, 2nd, 3rd, or just a number before 'harmonic')
    harmonic_match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*harmonic', text)
    harmonic = int(harmonic_match.group(1)) if harmonic_match else 1

    # Find length (number before 'meter' or 'm')
    length_match = re.search(r'(\d+(\.\d+)?)\s*(m|meter)', text)
    length = float(length_match.group(1)) if length_match else 1.0

    return pipe_type, length, harmonic


# ---------- FUNCTION TO GET SPEECH INPUT ----------
def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your command (e.g., '3rd harmonic, closed pipe, 0.5 meters'):")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio, please try again.")
            return ""
        except sr.RequestError:
            print("Speech recognition service failed.")
            return ""

# ---------- ASK USER FOR INPUT TYPE ----------
mode = input("Type 's' for typing or 'v' for voice input: ").lower()
if mode == 'v':
    user_input = get_speech_input()
else:
    user_input = input("Type your command (e.g., '2nd harmonic, open pipe, 1 meter'): ")

pipe_type, length, harmonic = parse_input(user_input)

# ---------- GENERATE WAVE DATA ----------
x, k, f = standing_wave(pipe_type, length, harmonic)
amplitude = 0.2

# ---------- FIGURE SETUP ----------
fig, ax = plt.subplots(figsize=(10,4))
ax.set_xlim(-0.1, length + 0.1)
ax.set_ylim(-0.5, 0.5)
ax.set_xlabel("Position along pipe (m)")
ax.set_ylabel("Amplitude")
ax.set_title(f"{pipe_type.capitalize()} Pipe - Harmonic {harmonic} - {length} m - f={f:.2f}Hz")
ax.grid(True)

# Draw pipe rectangle
rect = Rectangle((0, -amplitude), length, 2*amplitude, fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(rect)

# Line for wave
line, = ax.plot([], [], 'b-', linewidth=2)

# ---------- ANIMATION FUNCTION ----------
def animate(t):
    y = amplitude * np.sin(k*x) * np.cos(2*np.pi*f*t)
    line.set_data(x, y)
    return line,

# ---------- CREATE ANIMATION ----------
anim = FuncAnimation(fig, animate, frames=np.linspace(0,0.02,200), interval=50, blit=True)
plt.show()
