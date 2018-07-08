import telebot
import requests
import json
from pydub import AudioSegment
import os
import messages

import config

API_ENDPOINT = 'https://api.wit.ai/speech'

wit_access_token = config.wit_token

bot = telebot.TeleBot(config.token)

def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

def RecognizeSpeech(AUDIO_FILENAME):
    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + wit_access_token, 'Content-Type': 'audio/wav'}
    # making an HTTP post request
    audio = read_audio(AUDIO_FILENAME)
    resp = requests.post(API_ENDPOINT, headers=headers, data=audio)
    # converting response content to JSON format
    data = json.loads(resp.content)
    # get text from data
    try:
        user_text = data['_text']
        return user_text
    except:
        return messages.VOICEERROR

def voice_to_text(message):
    # writing file
    file_ogg = 'voices/' + str(message.chat.id) + '.ogg'
    file_wav = 'voices/' + str(message.chat.id) + '.wav'
    # download file
    raw = message.voice.file_id
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_ogg, 'wb') as new_file:
        new_file.write(downloaded_file)
    sound = AudioSegment.from_ogg(file_ogg)
    sound.export(file_wav, format='wav')
    text = RecognizeSpeech(file_wav)
    os.remove(file_ogg)
    os.remove(file_wav)
    return format(text)

