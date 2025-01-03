import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Añadir el directorio raíz del proyecto al path para que Python pueda encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar las clases necesarias
from BotManager import BotManager
from InsultBot import InsultBot


class TestInsultBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')  # Mockear la creación de Minecraft
    @patch('mcpi.minecraft.Minecraft.postToChat')  # Mockear el método postToChat
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        # Mockear la instancia de Minecraft
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar el InsultBot
        self.insult_bot = InsultBot()

        # Mockear el método send_message
        self.insult_bot.send_message = MagicMock()

    def test_perform_task(self):
        # Simular que el bot no debe detenerse
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Ejecutar la tarea del bot
        self.insult_bot.perform_task(stop_event)

        # Verificar que se enviaron algunos insultos
        self.insult_bot.send_message.assert_any_call("Do you even know how to play?")
        self.insult_bot.send_message.assert_any_call("You're slower than a turtle!")

    def test_stop_task_sends_interrupt_message(self):
        # Simular que el bot debe detenerse
        stop_event = MagicMock()
        stop_event.is_set.return_value = True

        # Ejecutar la tarea del bot
        self.insult_bot.perform_task(stop_event)

        # Verificar que se envió el mensaje de interrupción
        self.insult_bot.send_message.assert_any_call(f"{self.insult_bot.name} has been interrupted.")

    def test_random_shuffling_of_insults(self):
        # Copiar la lista original de insultos
        original_insults = self.insult_bot.insults[:]

        # Simular que el bot no debe detenerse
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Ejecutar la tarea del bot
        self.insult_bot.perform_task(stop_event)

        # Verificar que el orden de los insultos ha cambiado
        self.assertNotEqual(self.insult_bot.insults, original_insults)


if __name__ == "__main__":
    unittest.main()