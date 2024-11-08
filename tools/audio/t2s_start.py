from google.cloud import texttospeech
import os

# Set up your Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# 使用 SSML 控制发音
ssml_text = """
<speak>
    欢迎来到玄策财经，<break time="300ms"/>在这里，我们洞悉市场的深层逻辑，<break time="300ms"/>为您带来独到的智慧解读。
</speak>
"""




synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

# Set the Studio voice parameters
voice = texttospeech.VoiceSelectionParams(
    language_code='cmn-CN',  # Mandarin Chinese
    name='cmn-CN-Wavenet-C',  # Example Studio voice for Mandarin Chinese
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Configure audio output
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Synthesize speech
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save the generated audio to a file
with open("start.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content has been saved as 'start.mp3'")
