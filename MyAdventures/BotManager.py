import threading
import time
from mcpi import minecraft

class BotManager:
    def __init__(self, mc):
        self.agents = {}
        self.mc = mc
        self.current_threads = {}  # Store current threads of bots
        self.current_task = None  # Track the current task
        self.thread_lock = threading.Lock()  # Lock for thread-safe operations

    def add_agent(self, name, agent):
        self.agents[name.lower()] = agent

    def execute_task(self, name):
        agent = self.agents.get(name.lower())
        if agent:
            if self.current_task and self.current_task != name.lower():
                # Detener la tarea actual
                self.stop_current_task()
            
            # Ejecutar la nueva tarea
            self.mc.postToChat(f"Executing task for bot: {name}")
            task_event = threading.Event()
            task_thread = threading.Thread(target=agent.perform_task, args=(task_event,))
            self.current_threads[name.lower()] = (task_thread, task_event)

            try:
                task_thread.start()
                self.mc.postToChat(f"Bot '{name}' started successfully.")
            except Exception as e:
                self.mc.postToChat(f"Error starting bot '{name}': {e}")

            self.current_task = name.lower()
        else:
            self.mc.postToChat(f"Bot '{name}' not found.")

    def stop_current_task(self):
        if self.current_task:
            with self.thread_lock:
                thread, event = self.current_threads[self.current_task]
                event.set()
                thread.join(timeout=5)  # Esperar a que el thread termine
                if thread.is_alive():
                    self.mc.postToChat(f"Warning: Bot '{self.current_task}' did not stop gracefully.")
                del self.current_threads[self.current_task]
            self.mc.postToChat(f"Bot '{self.current_task}' has been stopped.")
            self.current_task = None

    def list_agents(self):
        return list(self.agents.keys())

    def listen_for_commands(self):
        self.mc.postToChat("BotManager is now listening for commands. Type 'list', or 'exit'.")
        while True:
            try:
                for event in self.mc.events.pollChatPosts():
                    command = event.message.strip().lower()
                    if command == "list":
                        self.mc.postToChat(f"Bots: {', '.join(self.list_agents())}")
                    elif command.startswith("reflective "):  # Comandos específicos para ReflectiveBot
                        subcommand = command.split(" ", 1)[1] if " " in command else ""
                        bot = self.agents.get("reflective")
                        if bot:
                            bot.respond(subcommand)
                        else:
                            self.mc.postToChat("ReflectiveBot is not available.")
                    elif command == "exit":
                        self.mc.postToChat("Exiting BotManager...")
                        self.stop_current_task()
                        return
                    elif command in self.agents:
                        self.execute_task(command)
                    else:
                        self.mc.postToChat(f"Command '{command}' not recognized.")
            except Exception as e:
                self.mc.postToChat(f"Error in listen_for_commands: {e}")
