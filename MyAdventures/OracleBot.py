import asyncio
import string
from MinecraftAgent import MinecraftAgent

class OracleBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OracleBot", mc)
        self.responses = {
            "how do i move in minecraft": "Use the W, A, S, and D keys to move, and the spacebar to jump.",
            "how do i open my inventory": "Press the E key to open your inventory.",
            "how do i break blocks": "Left-click and hold on a block to break it.",
            "how do i place blocks": "Right-click on a surface to place the block you're holding.",
        }

    def get_response(self, question):
        question_lower = question.lower().rstrip('?')
        question_clean = question_lower.translate(str.maketrans('', '', string.punctuation))
        question_clean = ' '.join(question_clean.split())
        return self.responses.get(question_clean, "Sorry, I don't know the answer to that question.")

    async def perform_task(self, stop_event):
        self.show_available_questions()
        while not stop_event.is_set():
            await asyncio.sleep(1)

        self.send_message("OracleBot task interrupted.")

    def show_available_questions(self):
        self.mc.postToChat(f"{self.name}: You can ask the following questions:")
        for question in self.responses.keys():
            self.mc.postToChat(f"- {question}")