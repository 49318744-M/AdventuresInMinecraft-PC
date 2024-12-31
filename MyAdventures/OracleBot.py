import time
from MinecraftAgent import MinecraftAgent

class OracleBot(MinecraftAgent):
    def __init__(self, mc):
        super().__init__("OracleBot")
        self.mc = mc
        self.responses = {
            "How do I move in Minecraft?": "Use the W, A, S, and D keys to move, and the spacebar to jump.",
            "How do I open my inventory?": "Press the E key to open your inventory.",
            "How do I break blocks?": "Left-click and hold on a block to break it.",
            "How do I place blocks?": "Right-click on a surface to place the block you're holding.",
        }

    def get_response(self, question):
        question_lower = question.lower()
        for key in self.responses.keys():
            if key.lower() == question_lower:
                return self.responses[key]
        return "Sorry, I don't know the answer to that question."

    def respond_to_chat(self, stop_event):
        while not stop_event.is_set():  # Verificar el evento de interrupción en cada iteración
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                if stop_event.is_set():  # Stop if interrumped
                    return
                message = event.message
                if message.endswith("?"):  # If its a question
                    answer = self.get_response(message)
                    self.mc.postToChat(f"{self.name}: {answer}")
            time.sleep(0.1)  

    def show_available_questions(self):
        questions = [f"- {question}" for question in self.responses.keys()]
        self.mc.postToChat(f"{self.name}: You can ask the following questions:")
        for question in questions:
            self.mc.postToChat(question)

    def perform_task(self, stop_event):
        self.show_available_questions()
        while not stop_event.is_set():  #
            self.respond_to_chat(stop_event)  # Respond
            time.sleep(1)  # Wait a second
        self.send_message("OracleBot task interrupted.")