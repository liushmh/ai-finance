import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Azure Text-to-Speech configuration
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')        # Replace with your Azure Speech API Key
AZURE_REGION = os.getenv('AZURE_REGION')                 # Replace with your Azure Region

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"  # Example voice

# Define SSML text
ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
    <voice name="zh-CN-YunxiNeural">
        
        <mstts:express-as style="cheerful">
            标普500指数和纳斯达克综合指数在周四上涨，延续了特朗普当选后的华尔街反弹，两大指数均创下历史新高！
        </mstts:express-as>
        <break time="200ms"/>
        标普500指数上涨<prosody pitch="+1st">0.74%</prosody>，收于5,973.09点。
        <break time="200ms"/>

        <mstts:express-as style="cheerful">
            纳斯达克指数上涨1.54%，达到21,101.57点，这是该指数首次收于21,000点以上！投资者对这一成就感到非常乐观。
        </mstts:express-as>
        <break time="300ms"/>

        投资者对特朗普第二任期的政策反应积极，预计将有利于股票等风险资产，部分原因是他提出的<emphasis level="strong">减税计划</emphasis>。
        <break time="200ms"/>
        
        <mstts:express-as style="sad">
            然而，持续的政府赤字和更高的关税可能引发对通胀反弹的担忧，导致市场波动性增加。
        </mstts:express-as>
        <break time="300ms"/>

        美联储宣布降息<prosody rate="fast" pitch="-1st">25个基点</prosody>，这是市场普遍预期的，但降幅小于9月份的50个基点。
        <break time="200ms"/>
        
        <mstts:express-as style="cheerful">
            美联储主席鲍威尔表示对经济状况感到“良好”，央行似乎将继续坚持小幅度的调整策略。
        </mstts:express-as>
        <break time="300ms"/>

        <mstts:express-as style="empathetic">
            在美联储自特朗普当选以来首次降息后，加密货币价格与会议前基本持平。社交媒体评论者认为，联邦公开市场委员会的决策对数字资产价格的影响可能会越来越小。
        </mstts:express-as>
        <break time="200ms"/>

        美联储主席杰罗姆·鲍威尔表示，央行不会因短期通胀数据或选举结果而改变策略。
        <break time="300ms"/>
        
        他强调，删除关于“对通胀更有信心”的措辞只是<emphasis level="moderate">说法上的调整</emphasis>，并非政策方向的改变。
        <break time="200ms"/>

        <mstts:express-as style="sad">
            特朗普和鲍威尔在利率政策上一直存在分歧。尽管特朗普在2017年任命了鲍威尔，但他曾批评鲍威尔采取保守的利率政策，声称这减缓了美国的经济增长。
        </mstts:express-as>
        <break time="200ms"/>

        <mstts:express-as style="empathetic">
            有传言称，一旦特朗普在一月份就任，鲍威尔可能会辞职。但鲍威尔在新闻发布会上表示，即使被特朗普要求辞职，他也不会下台。
        </mstts:express-as>
        <break time="200ms"/>
    </voice>
</speak>
"""

# Function to convert SSML to speech and save as audio file
def synthesize_ssml_to_audio(ssml_text, output_path="output_audio.mp3"):
    # Set up the audio output format and config
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    # Perform synthesis with SSML input
    result = synthesizer.speak_ssml_async(ssml_text).get()

    # Check result for success or error
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio content saved to '{output_path}'")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")

# Call the function with SSML text
synthesize_ssml_to_audio(ssml_text, output_path="start.mp3")
