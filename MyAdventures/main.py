from mcpi import minecraft
from InsultBot import InsultBot
from TNTbot import TNTBot
from OracleBot import OracleBot
from BotManager import BotManager

if __name__ == "__main__":
    # Create connection to Minecraft
    mc = minecraft.Minecraft.create()

    # Create the BotManager
    bot_manager = BotManager(mc)

    # Initialize bots
    insult_bot = InsultBot()
    tnt_bot = TNTBot()
    oracle_bot = OracleBot(mc)

    # Add bots to the manager
    bot_manager.add_agent("insult", insult_bot)
    bot_manager.add_agent("tnt", tnt_bot)
    bot_manager.add_agent("oracle", oracle_bot)

    # Listen for commands from the Minecraft chat
    bot_manager.listen_for_commands()
