import asyncio
from mcpi import minecraft

class BotManager:
    def __init__(self, mc):
        self.mc = mc
        self.agents = {}
        self.tasks = {}

    def add_agent(self, name, agent):
        self.agents[name] = agent

    async def list_agents(self):
        return list(self.agents.keys())

    async def handle_command(self, message):
        command_parts = message.split()
        command = command_parts[0]
        if command == "list":
            agents = await self.list_agents()
            self.mc.postToChat("Available agents: " + ", ".join(agents))
        elif command in self.agents:
            # Check if the agent is already active
            if command in self.tasks:
                self.mc.postToChat(f"{command} is already active.")
                return

            # Cancel all existing tasks
            for task in self.tasks.values():
                task['stop_event'].set()
                task['task'].cancel()
            self.tasks.clear()

            stop_event = asyncio.Event()
            agent = self.agents[command]
            task = asyncio.create_task(agent.perform_task(stop_event))
            self.tasks[command] = {'task': task, 'stop_event': stop_event}
        else:
            self.mc.postToChat(f"Unknown command: {message}")

    async def listen_for_commands(self):
        while True:
            chat_events = self.mc.events.pollChatPosts()
            for event in chat_events:
                message = event.message.strip().lower()
                await self.handle_command(message)
            await asyncio.sleep(1)

    def run(self):
        asyncio.run(self.listen_for_commands())
