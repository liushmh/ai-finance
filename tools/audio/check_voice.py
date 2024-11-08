from google.cloud import texttospeech
import os

# Set up your credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

# Initialize the client
client = texttospeech.TextToSpeechClient()

# Request a list of available voices
response = client.list_voices()

# Filter for Mandarin (zh-CN) and Cantonese (yue-HK) voices
for voice in response.voices:
    if 'm' in voice.language_codes or 'yue-HK' in voice.language_codes:
        print(f"Name: {voice.name}")
        print(f"Language Codes: {voice.language_codes}")
        print(f"SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}")
        print(f"Voice Type: {'Studio' if 'Studio' in voice.name else 'Standard/WaveNet'}\n")
