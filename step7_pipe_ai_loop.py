import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import speech_recognition as sr
import re

# ---------- STANDING WAVE FUNCTION ----------
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

# ---------- PARSE INPUT FUNCTION ----------
def parse_input(text):
    """
    Parses a command like:
    'second harmonic, closed pipe, 0.5 meters'
    '3rd harmonic open pipe 1 meter'
    Returns: pipe_type (str), length (float), harmonic (int)
    """
    text = text.lower()
    
    # Detect pipe type
    pipe_type = 'open' if 'open' in text else 'closed'

    # Convert word numbers to digits
    word_to_num = {
        'first': 1, '1st': 1,
        'second': 2, '2nd': 2,
        'third': 3, '3rd': 3,
        'fourth': 4, '4th': 4,
        'fifth': 5, '5th': 5,
        'sixth': 6, '6th': 6,
        'seventh': 7, '7th': 7,
        'eighth': 8, '8th': 8,
        'ninth': 9, '9th': 9,
        'tenth': 10, '10th': 10
    }
    for word, num in word_to_num.items():
        text = text.replace(word, str(num))

    # Extract harmonic
    harmonic_match = re.search(r'(\d+)\s*harmonic', text)
    harmonic = int(harmonic_match.group(1)) if harmonic_match else 1

    # Extract length in meters
    length_match = re.search(r'(\d+(\.\d+)?)\s*(m|meter)', text)
    length = float(length_match.group(1)) if length_match else 1.0

    return pipe_type, length, harmonic

# ---------- SPEECH INPUT FUNCTION ----------
def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your command (e.g., 'second harmonic, closed pipe, 0.5 meters'):")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=10)  # listen up to 10 seconds
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

# ---------- MAIN LOOP ----------
while True:
    mode = input("\nType 's' for typing, 'v' for voice input, or 'q' to quit: ").lower()
    if mode == 'q':
        print("Exiting program.")
        break
    elif mode == 'v':
        user_input = get_speech_input()
        if not user_input:
            continue
    else:
        user_input = input("Type your command (e.g., '2nd harmonic, open pipe, 1 meter'): ")
    
    pipe_type, length, harmonic = parse_input(user_input)

    # Generate wave data
    x, k, f = standing_wave(pipe_type, length, harmonic)
    amplitude = 0.2

    # Figure setup
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

    # Animation function
    def animate(t):
        y = amplitude * np.sin(k*x) * np.cos(2*np.pi*f*t)
        line.set_data(x, y)
        return line,

    anim = FuncAnimation(fig, animate, frames=np.linspace(0,0.02,200), interval=50, blit=True)
    plt.show()
