import unittest
from unittest.mock import MagicMock, patch
from BotManager import BotManager
from InsultBot import InsultBot
from mcpi.minecraft import Minecraft  # Ahora InsultBot no requiere argumentos adicionales

class TestBotManager(unittest.TestCase):

    def setUp(self):
        # Mock de la clase Minecraft
        self.mock_mc = MagicMock()
        
        # Crear instancia de BotManager con el mock de Minecraft
        self.bot_manager = BotManager(self.mock_mc)

        # Crear y agregar un bot al bot_manager
        self.insult_bot = InsultBot()  # Se crea sin argumentos
        self.bot_manager.add_agent("insult", self.insult_bot)

    def test_execute_task(self):
        # Simular la ejecución de una tarea
        self.bot_manager.execute_task("insult")

        # Verificar que se haya enviado el mensaje de inicio
        self.mock_mc.postToChat.assert_any_call("Executing task for bot: insult")
        self.mock_mc.postToChat.assert_any_call("Bot 'insult' started successfully.")

    def test_receive_command_list(self):
        # Simular el evento de un mensaje de chat de tipo 'list'
        event = MagicMock()
        event.message = "list"
        self.mock_mc.events.pollChatPosts.return_value = [event]

        # Llamar al método listen_for_commands
        self.bot_manager.listen_for_commands()

        # Verificar que se haya respondido con la lista de bots
        self.mock_mc.postToChat.assert_any_call("Bots: insult")

    def test_stop_task(self):
        # Simular la parada de una tarea
        self.bot_manager.execute_task("insult")
        self.bot_manager.stop_current_task()

        # Verificar que se haya enviado el mensaje de parada
        self.mock_mc.postToChat.assert_any_call("Bot 'insult' has been stopped.")

    def test_no_insults_sent_when_stopped(self):
        # Simular la detención del bot
        stop_event = MagicMock()
        stop_event.is_set.return_value = True  # Bot debe detenerse

        # Ejecutar la tarea de InsultBot
        self.insult_bot.perform_task(stop_event)

        # Verificar que el bot haya enviado el mensaje de interrupción
        self.insult_bot.send_message.assert_any_call(f"{self.insult_bot.name} has been interrupted.")

    def test_send_insult(self):
        # Simular que el bot no está detenido
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Ejecutar la tarea de InsultBot
        self.insult_bot.perform_task(stop_event)

        # Verificar que se haya enviado un insulto
        self.insult_bot.send_message.assert_any_call("You suck!")

if __name__ == "__main__":
    unittest.main()
