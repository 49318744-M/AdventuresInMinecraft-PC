import asyncio
import string
from MinecraftAgent import MinecraftAgent

class OracleBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OracleBot", mc)
        self.mc = mc
        self.responses = {
            "how do i move in minecraft": "Use the W, A, S, and D keys to move, and the spacebar to jump.",
            "how do i open my inventory": "Press the E key to open your inventory.",
            "how do i break blocks": "Left-click and hold on a block to break it.",
            "how do i place blocks": "Right-click on a surface to place the block you're holding.",
        }
        self.agents = ["insult", "anotherbotname"]  
    def get_response(self, question):
        question_lower = question.lower().rstrip('?')
        question_clean = question_lower.translate(str.maketrans('', '', string.punctuation))
        question_clean = ' '.join(question_clean.split())
        return self.responses.get(question_clean, "Sorry, I don't know the answer to that question.")

    async def respond_to_chat(self, stop_event, bot_manager):
        while not stop_event.is_set():
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                if stop_event.is_set():
                    return
                message = event.message.strip().lower()

                if message.endswith("?"):
                    answer = self.get_response(message)
                    self.mc.postToChat(f"{self.name}: {answer}")

                if message in self.agents:
                    stop_event.set()
                    self.send_message(f"Stopping OracleBot and switching to {message}.")
                    await bot_manager.handle_command(message)  # Switch to the new bot
                    return
            await asyncio.sleep(0.1)

    def show_available_questions(self):
        questions = [f"- {question}" for question in self.responses.keys()]
        self.mc.postToChat(f"{self.name}: You can ask the following questions:")
        for question in questions:
            self.mc.postToChat(question)
    async def perform_task(self, stop_event):
        self.show_available_questions()
        while not stop_event.is_set():
            try:
                await asyncio.wait_for(self.respond_to_chat(stop_event), timeout=0.1)
            except asyncio.TimeoutError:
                pass
        self.send_message("OracleBot task interrupted.")
