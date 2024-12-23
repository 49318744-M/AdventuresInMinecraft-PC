import mcpi.minecraft as minecraft
import time

class OracleBot:
    def __init__(self, mc):
        self.mc = mc
        self.name = "OracleBot"
        self.responses = {
            "How do I move in Minecraft?": "Use the W, A, S, and D keys to move, and the spacebar to jump.",
            "How do I open my inventory?": "Press the E key to open your inventory.",
            "How do I break blocks?": "Left-click and hold on a block to break it.",
            "How do I place blocks?": "Right-click on a surface to place the block you're holding.",
        }

    def get_response(self, question):
        # Convert both the question and input to lowercase
        question_lower = question.lower()
        for key in self.responses.keys():
            if key.lower() == question_lower:
                return self.responses[key]
        return "Sorry, I don't know the answer to that question."

    def respond_to_chat(self):
        while True:
            chat_events = self.mc.events.pollChatPosts()

            for event in chat_events:
                message = event.message

                if message.endswith("?"):  # If the message is a question
                    answer = self.get_response(message)
                    self.mc.postToChat(f"{self.name}: {answer}")

    def show_available_questions(self):
        questions = [f"- {question}" for question in self.responses.keys()]
        
        # Send the initial message
        self.mc.postToChat(f"{self.name}: You can ask the following questions:")
        
        # Send each question
        for question in questions:
            self.mc.postToChat(question)

def main():
    # Connect to Minecraft
    mc = minecraft.Minecraft.create()

    # Initialize the OracleBot
    oracle = OracleBot(mc)

    # Display the available questions in the chat
    oracle.show_available_questions()

    # Start listening to chat messages
    oracle.respond_to_chat()

if __name__ == "__main__":
    main()

