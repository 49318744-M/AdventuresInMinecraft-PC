import asyncio
from mcpi import minecraft

class BotManager:
    def __init__(self, mc):
        self.mc = mc
        self.agents = {}
        self.tasks = {}
        self.current_agent_name = None  # Active bot

    def add_agent(self, name, agent):
        self.agents[name] = agent

    async def list_agents(self):
        return list(self.agents.keys())

    async def handle_command(self, message):
        message = message.strip().lower()

        # bot list
        if message == "list":
            agents = await self.list_agents()
            self.mc.postToChat("Available agents: " + ", ".join(agents))
            return

        if message in self.agents:
            for t_info in self.tasks.values():
                t_info['stop_event'].set()
                t_info['task'].cancel()
            self.tasks.clear()

            stop_event = asyncio.Event()
            agent = self.agents[message]
            task = asyncio.create_task(agent.perform_task(stop_event))
            self.tasks[message] = {'task': task, 'stop_event': stop_event}
            self.current_agent_name = message

            self.mc.postToChat(f"Switched to {message} bot.")
            return

        # reflective 
        if self.current_agent_name == "reflective" and message.startswith("reflective "):
            command = message.split("reflective ", 1)[1]
            reflective_bot = self.agents["reflective"]
            reflective_bot.respond(command)
            return

        # none
        self.mc.postToChat(f"Unknown command: {message}")

    async def listen_for_commands(self):
        while True:
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                message = event.message.strip().lower()

              #questions
                if message.endswith("?"):
                    if self.current_agent_name == "openai": # OpenAI
                        openai_bot = self.agents["openai"]
                        response = await openai_bot.get_response(message)
                        self.mc.postToChat(f"OpenAIBot: {response}")
                    elif  self.current_agent_name == "oracle": # Oracle
                        active_bot = self.agents[self.current_agent_name]
                        if hasattr(active_bot, "get_response"):
                            answer = active_bot.get_response(message)
                            self.mc.postToChat(f"{active_bot.name}: {answer}")
                        else:
                            self.mc.postToChat(f"{active_bot.name} doesn't support questions.")
                    else:
                        self.mc.postToChat("No active bot to answer questions.") # No active bot
                else:
                    # Not a question
                    await self.handle_command(message)

            await asyncio.sleep(0.1)

    def send_welcome_message(self):
        self.mc.postToChat("Welcome to the Minecraft Bot platform!")
        self.mc.postToChat("To activate a bot, use the command: <bot_name>")
        self.mc.postToChat("Use 'list' to see available bots.")
        self.mc.postToChat("Enjoy!")

    def run(self):
        self.send_welcome_message()
        asyncio.run(self.listen_for_commands())