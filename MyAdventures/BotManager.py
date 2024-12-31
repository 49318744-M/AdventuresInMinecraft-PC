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
        agent = self.agents.get(name.lower())
        if agent:
            if self.current_task and self.current_task != name.lower():
                # Interrumpir la tarea actual
                self.mc.postToChat(f"Interrupting '{self.current_task}' bot.")
                self.stop_current_task()

            # Iniciar la nueva tarea
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
            thread, event = self.current_threads[self.current_task]
            event.set()  # Detener el hilo actual
            thread.join()  # Esperar a que termine
            del self.current_threads[self.current_task]  # Limpiar el hilo del bot detenido
            self.mc.postToChat(f"Bot '{self.current_task}' has been stopped.")
            self.current_task = None

    def list_agents(self):
        return list(self.agents.keys())

    def list_tasks(self, bot_name):
        agent = self.agents.get(bot_name.lower())
        if agent:
            # Returns the names of the callable methods of the agent
            return [method for method in dir(agent) if callable(getattr(agent, method)) and not method.startswith("__")]
        return None

    def listen_for_commands(self):
        self.mc.postToChat("BotManager is now listening for commands. Type 'list', 'tasks <bot_name>', 'invoke <bot_name> <method_name>', or 'exit'.")
        while True:
            for event in self.mc.events.pollChatPosts():
                command = event.message.strip().lower()
                #list of agents
                if command == "list":
                    self.mc.postToChat(f"Bots: {', '.join(self.list_agents())}")
                #list of tasks of an agent
                elif command.startswith("tasks "):
                    bot_name = command.split(" ")[1]
                    tasks = self.list_tasks(bot_name)
                    if tasks:
                        self.mc.postToChat(f"Available tasks for '{bot_name}': {', '.join(tasks)}")
                    else:
                        self.mc.postToChat(f"No tasks found for '{bot_name}'.")
                #exit
                elif command == "exit":
                    self.mc.postToChat("Exiting BotManager...")
                    return
                # Execute the task for the requested bot by name
                elif command in self.agents:
                    self.execute_task(command)
                # If the OracleBot is active, delegate questions to it
                elif self.current_task == "oracle" and "?" in command:
                    oracle_bot = self.agents.get("oracle")
                    if oracle_bot:
                        answer = oracle_bot.get_response(command)
                        self.mc.postToChat(f"OracleBot: {answer}")
                else:
                    self.mc.postToChat(f"Unknown command or bot: {command}")