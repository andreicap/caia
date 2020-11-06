"""
Speaker function --> speaks out a string
Dependencies:
    - pyttsx3 // pip install pyttsx3
"""
import pyttsx3

class Speaker():
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()