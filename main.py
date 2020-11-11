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

client_data = pd.read_csv('caia_sample_dataset.csv')
for col in client_data.columns:
    try:
        client_data[col] = client_data[col].map(num2words)
    except:
        pass

def error_statement():
    texts =["I didn't get this, but my developers will teach me later. Can you repeat please?",
    "I didnt quite get that. Again?"]
    speaker_obj.speak_text(random.choice(texts))
    extract_text_loop()


def say_what_again():
    text = "Say 'what' again. Say 'what' again, I dare you, I double dare you motherfucker, say what one more Goddamn time!"
    speaker_obj.speak_text(text)
    extract_text_loop()


def get_text_topic(speech_text):
    max_score = 70
    selected_topic = "no_topic"
    for topic, tokens in topics.items():
        token_score = process.extractOne(speech_text, tokens, scorer=fuzz.token_set_ratio)
        if token_score[1] > max_score:
            max_score = token_score[1]
            selected_topic = topic
    # special case, swiss market index
    token_score = process.extractOne(speech_text, ["swiss","market","index"], scorer=fuzz.partial_ratio)
    if token_score[1] > max_score:
        max_score = token_score[1]
        selected_topic = "smi"
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
    text_output = ""
    if topic == "smi":
        price, perc = get_stock_price_percent(r'%5ESSMI')
        text_output = f"The SMI index is at {price} today with {str('an increase' if perc > 0 else 'a decrease')} of {abs(perc)} percentage"
    else:
        potential_sentences = sentences[topic]
        text_output = random.choice(potential_sentences)
        text_output = text_output.format(**client_data.iloc[0].to_dict())
        
    speaker_obj.speak_text(text_output)
    if topic == 'topic_end':
        exit()

    next_questions = ["Do you have any other question?", "Can I help you with something else?", "Do you have other questions?"]
    speaker_obj.speak_text(random.choice(next_questions))
    print('next question')
    extract_text_loop()


def get_stock_price_percent(stock_ticker):
    # print(get_stock_percent('%5ESSMI'))
    stock = stockquotes.Stock(stock_ticker)
    return (stock.current_price, stock.increase_percent)


if __name__ == "__main__":
    # intro_string = "Hi, I am Ka-ya, and I will be you client advisor today! How can I help you?"
    intro_string = f"Hi {client_data['data_name'].iloc[0]}, I am Kah-yah! How can I help you?"
    speaker_obj.speak_text(intro_string)
    extract_text_loop()
