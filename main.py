from voice_parser import extract_text
import pandas as pd
from fuzzywuzzy import fuzz
import speech_recognition as sr
from speaker import Speaker
from num2words import num2words 

speaker_obj = Speaker()

client_data = pd.DataFrame()
client_data.loc[0, 'name'] = "Andrei Cap"
client_data['liquidity'] = 999999.0
client_data['investments'] = 186.6
client_data['currency'] = 'CHF'

def get_text_topic(speech_text):
    ratio = fuzz.partial_ratio(speech_text, "assets")
    if ratio > 90:
        return "assets"

def extract_text_loop():
    speech_text = extract_text()
    topic = get_text_topic(speech_text)
    analyze_text_loop(topic)

def analyze_text_loop(topic):
    if topic == "assets":
        total_assets = int((client_data['investments']+client_data['liquidity']).iloc[0])
        total_assets_str = num2words(total_assets)
        print(total_assets_str)
        assets_text = f"Your total assets are {total_assets_str} swiss francs"
        speaker_obj.speak_text(assets_text)
    extract_text_loop()

if __name__ == "__main__":
    intro_string = "Hi, I am Ka-ya, and I will be you client advisor today! How can I help you?"
    speaker_obj.speak_text(intro_string)
    extract_text_loop()
