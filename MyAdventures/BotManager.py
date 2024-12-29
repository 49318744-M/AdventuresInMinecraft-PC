import threading
import time
from mcpi import minecraft

class BotManager:
    def __init__(self, mc):
        self.agents = {}
        self.mc = mc
        self.current_threads = {}  # Store current threads of bots
        self.current_task = None  # Track the current task

    def add_agent(self, name, agent):
        self.agents[name.lower()] = agent

    def execute_task(self, name):
        """Execute the task of a specific bot by name."""
        agent = self.agents.get(name.lower())
        if agent:
            if self.current_task and self.current_task != name.lower():
                # Interrupt current bot task
                self.mc.postToChat(f"Interrupting '{self.current_task}' bot.")
                self.stop_current_task()

            # Start new bot task
            self.mc.postToChat(f"Executing task for bot: {name}")
            task_event = threading.Event()
            task_thread = threading.Thread(target=agent.perform_task, args=(task_event,))
            self.current_threads[name.lower()] = (task_thread, task_event)
            task_thread.start()
            self.current_task = name.lower()  # Set current task to the new bot
        else:
            self.mc.postToChat(f"Bot '{name}' not found.")

    def stop_current_task(self):
        """Stop the current bot task."""
        if self.current_task:
            thread, event = self.current_threads[self.current_task]
            event.set()  # Set event to interrupt the task
            thread.join()  # Wait for it to fully stop
            self.mc.postToChat(f"Bot '{self.current_task}' has been stopped.")
            self.current_task = None  # Reset the current task

    def list_agents(self):
        return list(self.agents.keys())

    def listen_for_commands(self):
        self.mc.postToChat("BotManager is now listening for commands. Type 'list', '<bot_name>', or 'exit'.")
        while True:
            for event in self.mc.events.pollChatPosts():
                command = event.message.strip().lower()
                if command == "list":
                    self.mc.postToChat(f"Bots: {', '.join(self.list_agents())}")
                elif command == "exit":
                    self.mc.postToChat("Exiting BotManager...")
                    return
                else:
                    self.execute_task(command)  # Execute the task for the requested bot
