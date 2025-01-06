from mcpi.minecraft import Minecraft
from BotManager import BotManager
from InsultBot import InsultBot
from TNTbot import TNTBot
from OracleBot import OracleBot
from ReflectiveBot import ReflectiveBot
from BuildHouse import BuildHouse

if __name__ == "__main__":
    # Creates a connection to Minecraft
    mc = Minecraft.create()

    # Create a BotManager instance with the Minecraft
    bot_manager = BotManager(mc)

    # Inicializes the bots
    insult_bot = InsultBot(mc)
    tnt_bot = TNTBot(mc)
    oracle_bot = OracleBot(mc)
    build_house_bot = BuildHouse(mc)
    reflective_bot = ReflectiveBot(mc)

    # Add the bots to the BotManager
    bot_manager.add_agent("insult", insult_bot)
    bot_manager.add_agent("tnt", tnt_bot)
    bot_manager.add_agent("oracle", oracle_bot)
    bot_manager.add_agent("reflective", reflective_bot)
    bot_manager.add_agent("build_house", build_house_bot)

    # Run the BotManager to listen for commands
    bot_manager.run()
