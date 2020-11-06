from voice_parser import Listener
import pandas as pd
from fuzzywuzzy import fuzz, process
import speech_recognition as sr
from speaker import Speaker
from num2words import num2words
import json
import stockquotes
import random


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
    max_score = 20
    selected_topic = "no_topic"
    for topic, tokens in topics.items():
        token_score = process.extractOne(speech_text, tokens, scorer=fuzz.partial_ratio)
        if token_score[1] > max_score:
            max_score = token_score[1]
            selected_topic = topic
    if selected_topic == "no_topic":
        error_statement()
    return selected_topic


def extract_text_loop():
    speech_text = listener.extract_text()
    if speech_text.lower() == "what":
        say_what_again()

    topic = get_text_topic(speech_text)
    analyze_text_loop(topic)

def analyze_text_loop(topic):
    potential_sentences = sentences[topic]
    text_output = random.choice(sequence)
    
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
