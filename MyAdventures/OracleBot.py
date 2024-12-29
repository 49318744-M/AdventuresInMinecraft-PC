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

    def respond_to_chat(self):
        chat_events = self.mc.events.pollChatPosts()

        for event in chat_events:
            message = event.message

            if message.endswith("?"):  # If the message is a question
                answer = self.get_response(message)
                self.mc.postToChat(f"{self.name}: {answer}")

    def show_available_questions(self):
        questions = [f"- {question}" for question in self.responses.keys()]
        
        # Send the available questions to the chat
        self.mc.postToChat(f"{self.name}: You can ask the following questions:")
        
        # Send each question
        for question in questions:
            self.mc.postToChat(question)

    def perform_task(self, stop_event):
        self.show_available_questions()
        time.sleep(10)  # Wait for a while before responding (can be adjusted)
        self.respond_to_chat()  # Respond to any questions in the chat
        if stop_event.is_set():  # Check if the task was interrupted
            self.send_message("OracleBot task interrupted.")
