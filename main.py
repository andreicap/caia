from voice_parser import Listener
import pandas as pd
from fuzzywuzzy import fuzz
import speech_recognition as sr
from speaker import Speaker
from num2words import num2words
import json
import stockquotes


speaker_obj = Speaker()
listener = Listener()

topics = json.load(open("caia_logic.json"))['topics']
sentences = json.load(open("caia_logic.json"))['sentences']

client_data = pd.DataFrame()
client_data.loc[0, 'name'] = "Andrei Cap"
client_data['liquidity'] = 999999.0
client_data['investments'] = 186.6
client_data['currency'] = 'CHF'


def say_what_again():
    text = "Say 'what' again. Say 'what' again, I dare you, I double dare you motherfucker, say what one more Goddamn time!"
    speaker_obj.speak_text(text)


def get_text_topic(speech_text):
    ratio = fuzz.partial_ratio(speech_text, "assets")
    if ratio > 90:
        return "assets"

def extract_text_loop():
    speech_text = listener.extract_text()
    if speech_text.lower() == "what":
        say_what_again()

    topic = get_text_topic(speech_text)
    analyze_text_loop(topic)

def analyze_text_loop(topic):
    if topic == "assets":
        total_assets = int((client_data['investments'] + client_data['liquidity']).iloc[0])
        total_assets_str = num2words(total_assets)
        assets_text = f"Your total assets are {total_assets_str} swiss francs"
        speaker_obj.speak_text(assets_text)

    speaker_obj.speak_text("Next question, please")
    extract_text_loop()


def get_stock_price(stock_ticker):
    # e.g. print(get_stock_price('%5ESSMI'))
    stock = stockquotes.Stock(stock_ticker)
    return stock.current_price


def get_stock_percent(stock_ticker):
    # print(get_stock_percent('%5ESSMI'))
    stock = stockquotes.Stock(stock_ticker)
    return stock.increase_percent


if __name__ == "__main__":
    intro_string = "Hi, I am Ka-ya, and I will be you client advisor today! How can I help you?"
    speaker_obj.speak_text(intro_string)
    extract_text_loop()
