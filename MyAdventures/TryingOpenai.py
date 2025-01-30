from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found.")

client = OpenAI(api_key=api_key)

prompt = "How can I learn to code?"

chat_completion = client.chat.completions.create(
    messages = [
        {

        "role": "user",
        "content": prompt

        }
    ],
    model="gpt-3.5-turbo"

)
print(chat_completion.choices[0].message.content)