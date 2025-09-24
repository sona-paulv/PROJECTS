# ------------------- FFmpeg Setup -------------------
from pydub import AudioSegment
from pydub.utils import which

# Manually specify the ffmpeg and ffprobe paths
AudioSegment.converter = r"C:\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg-8.0-essentials_build\bin\ffprobe.exe"

# ------------------- Imports -------------------
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tkinter as tk
from textblob import TextBlob
from tkinter import filedialog, messagebox

# ------------------- Helper Functions -------------------
def clear_screen():
    """Clears all widgets from previous screens."""
    label.config(text="")
    label1.config(text="")
    label2.config(text="")
    content.grid_forget()
    btn_text_to_voice.grid_forget()
    btn_upload_voice.grid_forget()

# ------------------- Instructions Page -------------------
def instructions():
    clear_screen()
    info = """
    This converter provides two options:
    
    1. Text to Voice:
       - Convert entered text to voice.
       - Enter text and click "Convert".
    
    2. Voice to Text:
       - Convert an uploaded voice file (MP3/WAV) to text.
       - Select a file and click "Convert".
    """
    label.config(text=info)

# ------------------- Text to Voice -------------------
def text_converter():
    clear_screen()
    label.config(text="Enter text to convert into speech:")
    content.grid(column=0, row=1, padx=10, pady=5)
    btn_text_to_voice.grid(column=0, row=2, padx=10, pady=5)

def texttovoice():
    text = content.get()
    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    # Sentiment Analysis
    tv = TextBlob(text).sentiment
    label1.config(text=f"Polarity: {tv.polarity:.2f}, Subjectivity: {tv.subjectivity:.2f}")
    label1.grid(column=0, row=4, padx=10, pady=10)

    # Generate and Play Speech
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("output.mp3")
    playsound("output.mp3")
    messagebox.showinfo("Success", "Audio generated and played successfully!")

# ------------------- Voice to Text -------------------
def voice_converter():
    clear_screen()
    label.config(text="Select an MP3 or WAV file to convert into text:")
    btn_upload_voice.grid(column=0, row=1, padx=10, pady=5)

def upload_and_convert():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if not file_path:
        return

    # If MP3, convert to WAV using Pydub
    if file_path.endswith(".mp3"):
        sound = AudioSegment.from_mp3(file_path)
        file_path = "converted.wav"
        sound.export(file_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        messagebox.showinfo("Recognized Text", text)

        # Sentiment Analysis
        vt = TextBlob(text).sentiment
        label2.config(text=f"Polarity: {vt.polarity:.2f}, Subjectivity: {vt.subjectivity:.2f}")
        label2.grid(column=0, row=4, padx=10, pady=10)

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, could not understand the audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "API service unavailable.")

# ------------------- Main GUI -------------------
root = tk.Tk()
root.geometry('500x400')
root.title("Text ↔ Voice Converter")

# Set window icon
try:
    img = tk.PhotoImage(file='./text-to-speech.png')
    root.iconphoto(False, img)
except:
    pass  # If icon not found, skip

# Menu bar
menubar = tk.Menu(root)
menubar.add_cascade(label="Home", command=instructions)
menubar.add_cascade(label="Text To Voice", command=text_converter)
menubar.add_cascade(label="Voice To Text", command=voice_converter)
root.config(menu=menubar)

# Home label
label = tk.Label(root, text="", wraplength=450, justify="left")
label.grid(column=0, row=0, padx=10, pady=10)

# Text input for text-to-speech
content = tk.Entry(root, width=40)

# Labels to show polarity and subjectivity
label1 = tk.Label(root, text="", wraplength=450, justify="left")
label2 = tk.Label(root, text="", wraplength=450, justify="left")

# Buttons
btn_text_to_voice = tk.Button(root, text="Convert to Voice", command=texttovoice)
btn_upload_voice = tk.Button(root, text="Upload and Convert", command=upload_and_convert)

instructions()  # Show instructions at startup
root.mainloop()
