from InsultBot import InsultBot
from TNTbot import TNTBot
from BotManager import BotManager

def main():
    manager = BotManager()

    # Create instances of different bots (agents)
    insult_bot = InsultBot()
    tnt_bot = TNTBot()

    # Add bots to the BotManager
    manager.add_agent(tnt_bot)
    manager.add_agent(insult_bot)

    # Execute tasks for all bots periodically
    manager.execute_all_tasks_periodically(10)  # Cambiar de bot cada 10 segundos

if __name__ == "__main__":
    main()
