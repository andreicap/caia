import speech_recognition as sr
"""
	Dependencies:
		- pyaudio
		- speech_recognition
"""
class Listener():
	def __init__(self):
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
		with self.microphone as source:
			self.recognizer.adjust_for_ambient_noise(source)
		

	def extract_text(self):
		text = ""
		with self.microphone as source:
			try:
				print("Please speak")
				audio = self.recognizer.listen(source)
				text = self.recognizer.recognize_google(audio)
				print("Text recognized: \n" + text)
			except Exception as e:
				print("Error " + str(e))
		return text