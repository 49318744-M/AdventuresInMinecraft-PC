from MinecraftAgent import MinecraftAgent
import asyncio
from openai import OpenAI
import os
from dotenv import load_dotenv

class OpenAIBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OpenAIBot", mc)
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API Key not found")
    
        self.client = OpenAI(api_key=api_key)
        

    async def get_response(self, prompt):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Bot that responds questions"},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-3.5-turbo"
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"

    async def perform_task(self, stop_event):
        self.send_message("Ready to respond questions.")
        while not stop_event.is_set():
            await asyncio.sleep(1)
        self.send_message("OpenAIBot desactivated.")