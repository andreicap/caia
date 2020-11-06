"""
Speaker function --> speaks out a string
Dependencies:
    - pyttsx3 // pip install pyttsx3
"""
import pyttsx3

class Speaker():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.change_voice(0)
        self.change_voice_speed(230)

    def speak_text(self, text):
        print(f"CAIA >> {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def change_voice(self, voice_number):
        """
        Normal man voice = 0
        Female voice = 41
        """
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_number].id)

    def change_voice_speed(self, new_voice_rate):
        """
        Default voice rate: 250
        """
        self.engine.setProperty('rate', new_voice_rate)