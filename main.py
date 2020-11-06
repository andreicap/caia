from voice_parser import extract_text
import pandas as pd
from fuzzywuzzy import fuzz
import speech_recognition as sr


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
        assets_text = f"Your total assets are {total_assets}"
        #speak_text()
        print(assets_text)
        extract_text_loop()

if __name__ == "__main__":
    extract_text_loop()
