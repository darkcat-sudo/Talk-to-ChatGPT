import tkinter as tk
import speech_recognition as sr
import pyautogui
import time
import keyboard
import threading
import clipboard
import pyttsx3
import wave
import pyaudio

voicee= "David"
defaulttext ="Tab Ctrl+Space to listen.. Shift to repeat QN"

# Define a function to trigger the code when Alt is pressed
def trigger_alt_key(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'shift':
        #filter the para
        with open('tempo.txt', 'r') as file:
            lines = file.readlines()

        paragraphs = []

        current_paragraph = []
        for line in lines:
            if line.strip() == "":
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                current_paragraph = []
            else:
                current_paragraph.append(line)

        if current_paragraph:
            paragraphs.append(current_paragraph)

        if paragraphs:
            last_paragraph = paragraphs[-1]
            txttext="".join(last_paragraph)

        # Execute the code you provided
        result_label.config(text="Repeating previous question..")    
        engine = pyttsx3.init()
        desired_voice = voicee
        for voice in engine.getProperty('voices'):
            if desired_voice in voice.name:
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)
        engine.say(txttext)
        engine.runAndWait()
        result_label.config(text=defaulttext)
        
# Listen for the Alt key press event system-wide
keyboard.hook(trigger_alt_key)


def delete_last_line(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    if lines:
        lines.pop()  # Remove the last line

    with open(filename, "w") as file:
        file.writelines(lines)

#soundtrack function
def play_audio_file(file_path):
    CHUNK = 1024

    wf = wave.open(file_path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()




def recognize_speech():
    recognizer = sr.Recognizer()
    
    # Display "Listening now..." message
    result_label.config(text="Listening now...")
    root.update()
    wav_file_path = "assets/microphone-start-track.wav"  # Replace with the actual file path
    play_audio_file(wav_file_path)
    
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        result_label.config(text="Transcribing...")

    try:
        text = recognizer.recognize_google(audio)
        wav_file_path = "assets/microphone-mid-track.wav"  # Replace with the actual file path
        play_audio_file(wav_file_path)
        pyautogui.click(1333,611)
        pyautogui.click(497, 653)
        result_label.config(text=f"You: {text}")
        text_to_append = "You: " + text + "\n"
        file_path = "report.txt"
        with open(file_path, "a") as file:
            file.write(text_to_append)
        # Add a blank line
        with open(file_path, "a") as file:
            file.write("\n")

        # Adjust the window height based on text length
        root.update_idletasks()  # Update idle tasks to get accurate label height
        label_height = result_label.winfo_reqheight()
        window_height = 80 + label_height
        root.geometry(f"250x{window_height}")

        # Type the recognized text using pyautogui
        pyautogui.typewrite(text)
        pyautogui.press('enter')
        time.sleep(5) #adjust waiting time to copy the text
        pyautogui.click(1333,611)
        pyautogui.click(497, 653)

        #copying the text
        pyautogui.moveTo(499, 247)
        pyautogui.click()
        pyautogui.mouseDown()
        pyautogui.moveTo(1084, 548)
        pyautogui.mouseUp()
        pyautogui.hotkey('ctrl', 'c')
        clipboard_text = clipboard.paste()
        with open('tempo.txt', 'w', encoding="utf-8") as file:
             file.write(clipboard_text)
        pyautogui.moveTo(484, 659)
        pyautogui.click()

        #filter the last para
        with open('tempo.txt', 'r') as file:
            lines = file.readlines()
        paragraphs = []
        current_paragraph = []
        for line in lines:
            if line.strip() == "":
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                current_paragraph = []
            else:
                current_paragraph.append(line)

        if current_paragraph:
            paragraphs.append(current_paragraph)

        if paragraphs:
            last_paragraph = paragraphs[-1]
            txttext = "".join(last_paragraph)
            text_to_append = "GPT: " + "".join(last_paragraph) + "\n"
            file_path = "report.txt"
            with open(file_path, "a") as file:
                file.write(text_to_append)

        #text to speech
        result_label.config(text="GPT is Taking...")
        engine = pyttsx3.init()
        desired_voice = voicee

        for voice in engine.getProperty('voices'):
            if desired_voice in voice.name:
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 160)
        engine.say(txttext)
        engine.runAndWait()
        delete_last_line("report.txt")

    except sr.UnknownValueError:
        wav_file_path = "assets/microphone-out-track.wav"  # Replace with the actual file path
        play_audio_file(wav_file_path)
        time.sleep(1)
        result_label.config(text="Could not understand audio")
        engine = pyttsx3.init()
        desired_voice = 'Zira'
        for voice in engine.getProperty('voices'):
            if desired_voice in voice.name:
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 150)
        engine.say("No speech detected. Please try again.")
        engine.runAndWait()

                   
    except sr.RequestError as e:
        result_label.config(text=f"Error: {str(e)}")

    # Reset the label text after processing
    result_label.after(3000, lambda: result_label.config(text=defaulttext))

def start_listening():
    # Start the speech recognition process in a separate thread
    threading.Thread(target=recognize_speech).start()

# Create the main window
root = tk.Tk()
root.title("Talk to GPT")

# Set the window size (250x80 pixels)
root.geometry("250x80")

# Remove minimize and maximize buttons
root.resizable(False, False)

# Set the window to be always on top
root.attributes('-topmost', True)

# Set the background color and title color for dark mode
root.configure(bg="#333333")
root.title("Talk to GPT")
root.option_add("*TButton*highlightThickness", 0)  # Remove button border

# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the initial window position with gaps from the top and right
initial_x = screen_width - 250 - 10  # 10 pixels from the right
initial_y = 100  # 100 pixels from the top
root.geometry(f"250x80+{initial_x}+{initial_y}")

# Create a frame to contain the button and label
frame = tk.Frame(root, bg="#333333")  # Set the frame background color
frame.pack(fill="both", expand=True)

# Create a slightly smaller button to start voice recognition
recognize_button = tk.Button(frame, text="Start", command=start_listening, height=1, width=8)
recognize_button.pack(pady=10)

# Create a label to display the recognized text with a darker color
result_label = tk.Label(frame, text=defaulttext, wraplength=240, bg="#333333", fg="#999999")
result_label.pack(pady=5)

# Center the frame in the window
frame.place(relx=0.5, rely=0.5, anchor="center")

# Define a function to trigger the "Start" button
def trigger_start_button(e=None):  # Accept an optional argument
    start_listening()

# Listen for the Ctrl+Space key combination system-wide
keyboard.add_hotkey('ctrl+space', trigger_start_button)


root.mainloop()
