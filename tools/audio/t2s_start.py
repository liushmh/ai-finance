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
        欢迎来到中速财经，<break time="300ms"/>我们不仅致力于提供市场龙头的专业分析，<break time="300ms"/>更希望与您一起把握趋势，共同迈向财富增值的未来。<break time="500ms"/>
        在这里，<break time="300ms"/>您将获得关于美股和加密货币市场的最新动态和深度见解，<break time="300ms"/>助您在每一次投资决策中更加自信和从容。<break time="500ms"/>

        美股方面，<break time="300ms"/>我们紧跟市场领军企业的最新发展，<break time="300ms"/>为您剖析公司动向和行业趋势，<break time="300ms"/>帮助您识别价值所在。<break time="500ms"/>
        
        在迅速发展的加密货币领域，<break time="300ms"/>我们关注主要数字资产的价格走势和市场情绪变化，<break time="300ms"/>陪伴您在每次波动中找到投资良机。<break time="500ms"/>

        此外，中速财经还定期带来热点话题的深度解析，<break time="300ms"/>涵盖宏观经济、行业政策及未来科技的最新动态，<break time="300ms"/>为您提供更加全面的投资视角。<break time="500ms"/>

        我们相信，智慧与洞见可以成就财富增长。<break time="300ms"/>中速财经希望成为您可靠的伙伴，<break time="300ms"/>与您携手迈向机遇的未来。<break time="500ms"/>
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
