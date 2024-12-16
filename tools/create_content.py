import os
import requests
from bs4 import BeautifulSoup
import time
import json


# Load environment variables
OPENAI_API_KEY = os.getenv("CHAT_GPT_KEY")
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"


# Helper: Delay function
def delay(seconds):
    time.sleep(seconds)

# Helper: Call OpenAI API
def call_openai(api_url, data):
    retry_count = 0
    max_retries = 5

    while retry_count < max_retries:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            }
            response = requests.post(api_url, json=data, headers=headers)

            # Check rate limit headers for debugging
            remaining = response.headers.get("x-ratelimit-remaining-requests")
            reset_time = response.headers.get("x-ratelimit-reset-requests")
            print(f"Remaining Requests: {remaining}")
            print(f"Reset Time: {reset_time if reset_time else 'N/A'}")

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:  # Rate limit hit
                reset_time = response.headers.get("x-ratelimit-reset-requests")
                if reset_time and reset_time.isdigit():
                    wait_time = max(int(reset_time) - int(time.time()), 1)
                else:
                    print("Missing or invalid resetTime. Defaulting to 10 seconds.")
                    wait_time = 10
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                delay(wait_time)
                retry_count += 1
            else:
                print(f"API Error: {response.json() if response.content else str(err)}")
                raise err

    raise Exception("Max retries reached for OpenAI API")

 # model = "ft:gpt-4o-mini-2024-07-18:personal:aiyun:AUzqkJz2"
model = "gpt-4o-mini"
    
def generate_ssml_with_dynamic_style(content, title):
    """
    Use a single prompt to analyze content, determine the tone, and generate SSML with the appropriate style.
    """
    
    ssml_result = call_openai(
        CHATGPT_API_URL,
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional news analyst and tone analyzer. Your job is to analyze the content tone and generate a "
                        "Mandarin narration in Microsoft SSML MSTTS format. The narration should strictly adhere to the following rules:\n\n"
                        "1. **English Handling**:\n"
                        "   - All English words or phrases must be enclosed in `<lang xml:lang=\"en-US\">[English]</lang>` tags for proper pronunciation.\n"
                        "   - Example: `<lang xml:lang=\"en-US\">Nvidia</lang>`.\n\n"
                        "2. **Sentence Breaks**:\n"
                        "   - Insert `<break time=\"300ms\"/>` between sentences or ideas to create natural pauses.\n\n"
                        "3. **Tone Selection**:\n"
                        "   - Choose the tone that matches the content ('neutral', 'cheerful', 'serious', or 'sad').\n"
                        "   - Use `<mstts:express-as style=\"[tone]\">` to wrap the content.\n\n"
                        "4. **Content Structure**:\n"
                        "   - Generate a clear, logical Mandarin narration.\n"
                        "   - Ensure all sentences are formatted properly and no English words are left unformatted.\n\n"
                        "5. **Example Output Format**:\n"
                        "   <mstts:express-as style=\"serious\">\n"
                        "   这是一个示例内容。<break time=\"300ms\"/>\n"
                        "   <lang xml:lang=\"en-US\">Nvidia</lang> 是一家领先的科技公司。\n"
                        "   </mstts:express-as>\n\n"
                        "If any English words or phrases are detected in the content, ensure they are processed correctly with `<lang xml:lang=\"en-US\">` tags."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"请根据以下内容生成符合 Microsoft SSML MSTTS 格式只和标题'{title}'相关的中文段落,注意去掉报告来源\n\n"
                        f"内容: {content}"
                    ),
                },
            ],
            "max_tokens": 700,
            "temperature": 0.5,  # Lower temperature for consistency
        },
    )


    return ssml_result

# Main Function to Fetch and Process URL
def process_url(url):
    try:
        # Fetch and parse webpage content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.string if soup.title else "No Title"  # Extract page title
        content = "\n".join([p.get_text() for p in soup.find_all("p")])  # Combine all paragraphs

        print("\n=== Extracted Data ===")
        print(f"Title: {title}")
        print(f"Content: {content}")

        
        # Generate SSML Conclusion
        ssml_conclusion = generate_ssml_with_dynamic_style(content, title)

        # Generate Simple Sentence
        simple_sentence = call_openai(
            CHATGPT_API_URL,
            {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional financial analyst who creates concise summaries in Chinese for images.",
                    },
                    {"role": "user", "content": f"你是一位财经专业人士，请用25到50个汉字概括以下内容：{content}"},
                ],
                "max_tokens": 200,
                "temperature": 0.7,
            },
        )

        # Save the results to a file
        result = {
            "title": title,
            "ssmlConclusion": ssml_conclusion,
            "simpleSentence": simple_sentence,
        }

        output_file = "output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print(f"\nResults saved to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing the URL: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Entry Point for the Script
if __name__ == "__main__":
    url = input("Enter the URL to process: ").strip()
    if not url:
        print("URL is required. Exiting.")
    else:
        process_url(url)
