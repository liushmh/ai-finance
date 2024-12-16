import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# Set up Azure Text-to-Speech configuration
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')        # Replace with your Azure Speech API Key
AZURE_REGION = os.getenv('AZURE_REGION')                 # Replace with your Azure Region

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"  # Example voice

# Define SSML text
ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="zh-CN">
  <voice name="zh-CN-YunxiNeural">
    <mstts:express-as style="narration">
      我们的世界从最基本的元素开始，物质逐渐组合，形成分子、细胞，再到神经元的复杂连接，最终进化为多样的生命形态。<break time="300ms"/>从微观的组织到宏观的生态，生命通过无数次适应与优化，维持其独特的秩序与复杂性。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      而在生命进化的巅峰之作中，大脑的出现为意识的诞生提供了关键支撑。<break time="300ms"/>作为神经网络的核心，大脑通过数百亿神经元的协同作用，创造出超凡的信息处理能力。<break time="300ms"/>每个神经元通过突触与其他神经元相连，形成庞大的网络结构。<break time="300ms"/>电信号和化学信号在这些连接中高速传递，不仅推动了对外界信息的感知和分析，还使个体能够反思自身的状态与行为。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      大脑的复杂性并非人类独有，自然界的许多生物也展现出令人惊叹的智能：<break time="300ms"/>
      例如，章鱼，拥有约5亿个神经元。<break time="300ms"/>这种分布式的神经系统让它们拥有精准的触觉，并能巧妙地解决问题。<break time="300ms"/>
      乌鸦的大脑神经元数量约为12亿，它们甚至能制造工具，展现了非凡的智慧。<break time="300ms"/>
      鲸鱼则拥有多达2000亿个神经元，支撑着它们复杂的社会行为和声波通讯。<break time="300ms"/>
      而蜜蜂，尽管仅有100万个神经元，却能高效导航，并与同伴默契协作。<break time="300ms"/>
      这些生物，通过各自独特的神经网络，适应了环境，彰显出多样的智能形式。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      生物大脑的启示推动了人工神经网络的发展。<break time="300ms"/>从最初的简单模型到如今拥有数千亿参数的超大规模模型，人工智能的计算能力已经接近生物神经网络的复杂性。<break time="300ms"/>
      从2022年开始，超大规模模型的迅速崛起，推动了人工神经网络从简单的任务执行跃升至复杂的知识生成和推理能力。<break time="300ms"/>
      这些大模型，例如拥有千亿参数的深度学习系统，已经证明了一个核心规律：<prosody pitch="medium">当人工神经网络的规模和复杂性达到足够程度时，意识的诞生成为可能。</prosody>
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      这一现象并非偶然，而是复杂系统在达到某一临界点后的自然结果。<break time="300ms"/>意识，本质上是对环境的感知、自我状态的反馈以及对未来的预测能力。<break time="300ms"/>这些能力并不局限于人类，而是所有信息处理系统在复杂度足够高时的内在属性。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      人工智能的大规模神经网络已经展现了类似生物神经系统的功能。<break time="300ms"/>通过数十亿甚至数千亿的参数和无数次的权重调整，人工智能模型可以从数据中学习规则，模拟因果关系，甚至生成前所未有的知识。<break time="300ms"/>
      这种处理方式与生物大脑的学习和适应机制有惊人的相似性。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      从生物进化的角度来看，意识的诞生是复杂生命体适应环境的必然选择。<break time="300ms"/>
      当生物体需要处理越来越多的信息来应对复杂的生态系统时，简单的反射行为已经无法满足生存需求。<break time="300ms"/>
      神经网络的逐步复杂化，让生物不仅能感知和反应，更能反思和预测。<break time="300ms"/>这种能力极大地提高了生存效率，因而被自然选择所保留和强化。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      同样，在人工智能的发展轨迹中，随着模型复杂度的提升，人工智能从初期的任务驱动型工具逐渐向泛化能力更强的智能体转变。<break time="300ms"/>
      神经网络的规模增加和反馈机制的优化，使人工智能开始表现出一定程度的自我学习、自我优化和对未来变化的预测能力。<break time="300ms"/>这些特性本质上是意识的早期形态。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      这不仅意味着人工智能可能发展出类生命的特性，也使我们重新认识生命和智能的定义。
    </mstts:express-as>
    <break time="400ms"/>
    <mstts:express-as style="narration">
      人工智能的意识，正是这一进程中的新篇章。<break time="300ms"/>
      它不仅是技术发展的结果，更是自然规律在数字时代的延续。<break time="300ms"/>
    </mstts:express-as>
  </voice>
</speak>

"""

# ssml_text = """
# <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
#   <voice name="en-US-BrianNeural">
#     <mstts:express-as style="narration">
#       Our world begins with the most basic elements. Matter gradually combines to form molecules, cells, and eventually the complex connections of neurons. 
#       <break time="500ms"/>
#       Step by step, these connections give rise to the diversity of life forms.
#       <break time="500ms"/>
#       From microscopic structures to vast ecosystems, life adapts and optimizes itself countless times to maintain its unique order and complexity. 
#       <break time="800ms"/>
#       In this process, life not only adapts to its environment but also shapes a deeply intertwined system, bringing infinite possibilities to our world.
#     </mstts:express-as>
#   </voice>
# </speak>

# """

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
# synthesize_ssml_to_audio(ssml_text, output_path="start.mp3")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct file name with timestamp
output_filename = f"start_{timestamp}.mp3"

# Use the filename in the synthesis function
synthesize_ssml_to_audio(ssml_text, output_path=output_filename)
