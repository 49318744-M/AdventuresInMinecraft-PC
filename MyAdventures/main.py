from mcpi.minecraft import Minecraft
from BotManager import BotManager
from InsultBot import InsultBot
from TNTbot import TNTBot
from OracleBot import OracleBot
from ReflectiveBot import ReflectiveBot

if __name__ == "__main__":
    # Crear una única instancia de Minecraft
    mc = Minecraft.create()

    # Crear el BotManager con la instancia de Minecraft
    bot_manager = BotManager(mc)

    # Inicializar bots con la misma instancia de Minecraft
    insult_bot = InsultBot(mc)
    tnt_bot = TNTBot(mc)
    oracle_bot = OracleBot(mc)
    reflective_bot = ReflectiveBot(mc)

    # Agregar bots al BotManager
    bot_manager.add_agent("insult", insult_bot)
    bot_manager.add_agent("tnt", tnt_bot)
    bot_manager.add_agent("oracle", oracle_bot)
    bot_manager.add_agent("reflective", reflective_bot)

    # Escuchar comandos en el chat
    bot_manager.listen_for_commands()
