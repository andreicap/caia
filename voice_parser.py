import speech_recognition as sr
"""
	Dependencies:
		- pyaudio
		- speech_recognition
"""

def listen_command():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Please speak")
		audio = r.listen(source)
		print("Recognizing")
		try:
			print("You said \n" + r.recognize_google(audio))
			print("Audio recorded succesfully")

		except Exception as e:
			print("Error " + str(e))

		with open("recorded.wav", "wb") as f:
			f.write(audio.get_wav_data())


if __name__ == "__main__":
    listen_command()