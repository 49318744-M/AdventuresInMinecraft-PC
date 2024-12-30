from mcpi import minecraft
from BotManager import BotManager
from InsultBot import InsultBot
from TNTbot import TNTBot
from OracleBot import OracleBot
from BuildHouse import BuildHouse

if __name__ == "__main__":
    # Connection to minecraft
    mc = minecraft.Minecraft.create()

    # Creating manager
    bot_manager = BotManager(mc)

    # Inicializing bots
    insult_bot = InsultBot()
    tnt_bot = TNTBot()
    oracle_bot = OracleBot(mc)
    build_house_bot = BuildHouse(mc)

    # Add bots to manager
    bot_manager.add_agent("insult", insult_bot)
    bot_manager.add_agent("tnt", tnt_bot)
    bot_manager.add_agent("oracle", oracle_bot)
    bot_manager.add_agent("build_house", build_house_bot)

    # Listen to commands in the chat
    bot_manager.listen_for_commands()
