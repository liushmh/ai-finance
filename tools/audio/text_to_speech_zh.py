from google.cloud import texttospeech
import os

# Set up your Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service_account.json'

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# 使用 SSML 控制发音
ssml_text = """
<speak>
    在特朗普当选美国总统后，<break time="300ms"/>比特币价格创下新高，<break time="300ms"/>币圈市场随之迎来一波上涨。<break time="500ms"/>
    比特币上涨了 8%，<break time="300ms"/>突破 75,000 美元，打破了此前三月份的纪录。<break time="500ms"/>
    以太币也上涨了 10%，<break time="300ms"/>狗狗币则涨 15%。<break time="300ms"/>而去中心化交易所 Uniswap 则暴涨 28%。<break time="500ms"/>
    特朗普曾是加密货币的怀疑论者，<break time="300ms"/>但在选举前转变立场，<break time="300ms"/>承诺将美国打造成“全球加密货币之都”。<break time="500ms"/>
    他的竞选活动接受加密货币捐赠，<break time="300ms"/>并且成立了“世界自由金融”公司，<break time="300ms"/>计划与家人共同进军加密货币交易领域。<break time="500ms"/>

    特斯拉的股价在特朗普当选后也大涨近 15%，<break time="300ms"/>创下年内新高，使埃隆·马斯克的财富增加了 170 亿美元。<break time="500ms"/>
    特朗普在胜选演讲中称赞马斯克为“超级天才”和“新星”。<break time="500ms"/>
    马斯克为特朗普的竞选活动捐赠了至少 1.18 亿美元，<break time="300ms"/>成为其主要支持者之一。<break time="500ms"/>

    分析人士指出，特朗普的政策将为特斯拉在自动驾驶技术和机器人方面的积极发展提供有力支持。<break time="300ms"/>特斯拉正在推出高度智能化的家庭机器人，<break time="500ms"/>
    此项创新不仅有望进一步巩固特斯拉的市场地位，<break time="300ms"/>也为智能化生活方式的普及带来了无限可能。
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
with open("content_focus.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content has been saved as 'content_focus.mp3'")
