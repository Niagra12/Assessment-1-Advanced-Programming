
"""THE CODE IS LESS THAN 100 LINES IF THE COMMENTS ARE REMOVED"""
# This program tells random jokes using Tkinter GUI and text-to-speech.

import tkinter as tk                # GUI toolkit
from tkinter import messagebox       # For showing popup messages
from PIL import Image, ImageTk       # For loading and resizing images
import pyttsx3                       # For text-to-speech
import random                        # To pick random jokes
import threading                     # To run speech without freezing GUI

# ------------------ WINDOW SETUP ------------------
root = tk.Tk()                       # Create main window
root.title("CORNY AHH JOKES")        # Set window title
root.geometry("500x300")             # Define window size

# Try to load background image
try:
    bg = Image.open("exercise 2 speedimage.jpg")  # Load image
    bg = bg.resize((500, 300))                    # Resize to fit window
    bg_photo = ImageTk.PhotoImage(bg)             # Convert to Tkinter image
    tk.Label(root, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="white")                    # Fallback background color

# ------------------ TEXT-TO-SPEECH SETUP ------------------
engine = pyttsx3.init()              # Initialize TTS engine
#select a female voice if available
for voice in engine.getProperty("voices"):
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

# Function to speak text using threading so GUI doesn't freeze
def speak(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()

# ------------------ LOAD JOKES FUNCTION ------------------
def load_jokes(file_name):
    """
    Reads jokes from a text file.
    Each line should contain a setup and punchline separated by '?'.
    Returns a list of (setup, punchline) tuples.
    """
    jokes = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup.strip(), punchline.strip()))
    return jokes

# ------------------ JOKE FUNCTIONS ------------------
def tell_joke():
    """Picks and displays a random joke setup."""
    global current_joke, current_punchline, first_joke
    current_joke, current_punchline = random.choice(jokes)
    output_label.config(text=current_joke + "?")
    speak(current_joke + "?")
    submit_btn.config(command=show_punchline)     # Change button to show punchline

def show_punchline():
    """Displays punchline and speaks the full joke."""
    output_label.config(text=f"{current_joke}?\n\n{current_punchline}")
    speak(current_joke + "? " + current_punchline)
    entry.delete(0, tk.END)                       # Clear input box
    submit_btn.config(command=check_input)        # Reset button command
    instruction_label.config(text="Type 'Alexa tell me another joke' or 'quit'")
    speak("Type Alexa tell me another joke or quit.")

# ------------------ COMMAND CHECKING FUNCTION ------------------
def check_input():
    """Reads user input and performs actions based on the command."""
    cmd = entry.get().lower().strip()
    funny_replies = [
        "Oops! That didn't work.",
        "Try saying the magic words!",
        "Hmm, I didn't get that.",
        "Alexa is confused! Try again."
    ]

    # Respond according to command
    if first_joke and cmd == "alexa tell me a joke":
        tell_joke()
        set_first(False)
    elif not first_joke and cmd == "alexa tell me another joke":
        tell_joke()
    elif cmd == "quit":
        speak("Goodbye! Hope you laughed!")
        root.quit()
    else:
        msg = random.choice(funny_replies)
        messagebox.showinfo("Try Again", msg)
        speak(msg)
        entry.delete(0, tk.END)

# ------------------ HELPER FUNCTION ------------------
def set_first(value):
    """Sets the 'first_joke' flag."""
    global first_joke
    first_joke = value

# ------------------ VARIABLES ------------------
jokes = load_jokes("randomJokes.txt")   # List of jokes loaded from file
current_joke = ""                       # Current joke setup
current_punchline = ""                  # Current joke punchline
first_joke = True                       # Tracks if it's the first joke

# ------------------ WIDGETS ------------------
instruction_label = tk.Label(
    root,
    text="Type 'Alexa tell me a joke' or 'quit'",
    font=("Arial", 14),
    bg="white"
)
instruction_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=40)  # User input box
entry.pack(pady=10)
entry.focus()                                         # Cursor focus

submit_btn = tk.Button(
    root,
    text="Submit",
    width=20,
    bg="#007ACC",
    fg="white",
    command=check_input
)
submit_btn.pack(pady=5)

output_label = tk.Label(
    root,
    text="",
    font=("Arial", 16),
    wraplength=450,
    justify="center",
    bg="white"
)
output_label.pack(pady=20)

# Welcome message spoken after window appears
root.after(500, lambda: speak("Welcome! Type Alexa tell me a joke to start or quit to exit."))

# ------------------ RUN THE APPLICATION ------------------
root.mainloop()
