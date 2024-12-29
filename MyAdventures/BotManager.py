import time

class BotManager:
    def __init__(self):
        self.agents = []
        self.current_agent_index = 0

    def add_agent(self, agent):
        """Add an agent to the manager."""
        self.agents.append(agent)

    def execute_all_tasks_periodically(self, interval):
        """Execute the 'perform_task' method for each agent at a fixed interval."""
        while True:
            if self.agents:
                current_agent = self.agents[self.current_agent_index]
                current_agent.perform_task()  # Ejecuta la tarea del bot activo
                time.sleep(interval)  # Espera un intervalo especificado antes de cambiar
                self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)  # Cambia al siguiente bot
