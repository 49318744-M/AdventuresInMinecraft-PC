
import os
from MinecraftAgent import MinecraftAgent
import asyncio
from openai import OpenAI
from config import API_KEY


class OpenAIBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OpenAIBot", mc)

       # Obtén y verifica la API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.strip() == "":
            raise ValueError("API Key no encontrada en las variables de entorno.")
        
        # Depuración: Imprime la clave cargada
        print(f"API Key utilizada en OpenAIBot: {api_key}")

        # Inicializa el cliente OpenAI
        self.client = OpenAI(api_key=api_key)

    async def get_response(self, prompt):
        try:
            print(f"Enviando solicitud a OpenAI con la clave: {self.client.api_key[:5]}...")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Friendly bot that answers questions."},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-3.5-turbo"
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error detallado: {e}")
            return f"Error generando respuesta: {e}"
    
    async def perform_task(self, stop_event):
        self.send_message("Ready to respond questions.")
        while not stop_event.is_set():
            await asyncio.sleep(1)
        self.send_message("OpenAIBot desactivated.")