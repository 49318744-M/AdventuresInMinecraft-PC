import asyncio
from MinecraftAgent import MinecraftAgent

class OracleBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OracleBot", mc)
        self.questions = [
            "How do I move in Minecraft?",
            "How do I open my inventory?",
            "How do I break blocks?",
            "How do I place blocks?"
        ]
        self.responses = {
            "how do i move in minecraft": "Use the W, A, S, and D keys to move around.",
            "how do i open my inventory": "Press the E key to open your inventory.",
            "how do i break blocks": "Left-click and hold on a block to break it.",
            "how do i place blocks": "Right-click to place a block."
        }

    def get_response(self, question):
        question_lower = question.lower().strip("?")  # Normalize the question
        return self.responses.get(question_lower, "Sorry, I don't know the answer to that question.")

    async def respond_to_chat(self, stop_event):
        while not stop_event.is_set():  
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                if stop_event.is_set():  # Stop if interrupted
                    return
                message = event.message.strip().lower()

                #questions
                if message.endswith("?"):  
                    answer = self.get_response(message)
                    self.mc.postToChat(f"{self.name}: {answer}")
                #chage bot
                if message in self.agents:  
                    stop_event.set()  
                    self.send_message(f"Stopping OracleBot and switching to {message}.")
                    return
            await asyncio.sleep(0.1)  

    def show_available_questions(self):
        self.mc.postToChat("OracleBot: You can ask the following questions:")
        for question in self.questions:
            self.mc.postToChat(f"- {question}")

    async def perform_task(self, stop_event):
        self.show_available_questions()
        while not stop_event.is_set():
            try:
                await asyncio.wait_for(self.respond_to_chat(stop_event), timeout=0.1)
            except asyncio.TimeoutError:
                pass
        self.send_message("OracleBot task interrupted.")