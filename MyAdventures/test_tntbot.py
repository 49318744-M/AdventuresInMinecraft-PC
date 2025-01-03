import unittest
from unittest.mock import patch, MagicMock
from mcpi.block import TNT, FIRE
from TNTbot import TNTBot
import time
import os
import sys

# Añadir el directorio raíz del proyecto al path para que Python pueda encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTNTBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')  # Mockear la creación de Minecraft
    @patch('mcpi.minecraft.Minecraft.postToChat')  # Mockear el método postToChat
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        # Mockear la instancia de Minecraft
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar el TNTBot
        self.tnt_bot = TNTBot()

        # Mockear el método getTilePos para devolver una posición fija
        self.tnt_bot.mc = self.mock_mc
        self.tnt_bot.mc.player.getTilePos.return_value = MagicMock(x=10, y=64, z=10)

        # Mockear el método setBlock para evitar la colocación real de bloques
        self.tnt_bot.mc.setBlock = MagicMock()

        # Mockear el método send_message
        self.tnt_bot.send_message = MagicMock()

    def test_place_tnt(self):  # Simular la colocación de TNT y fuego
        # Asegurarse de que no se detenga
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Ejecutar el método perform_task
        self.tnt_bot.perform_task(stop_event)

        # Verificar que el TNT se colocó en la posición correcta (10, 64, 10)
        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 10, TNT, 1)

        # Verificar que el fuego se colocó en (10, 64, 11) utilizando el objeto de bloque FIRE correcto
        self.tnt_bot.mc.setBlock.assert_any_call(10, 64, 11, FIRE)

    def test_stop_task_sends_interrupt_message(self):  # Simular la interrupción del bot
        # Ahora simulamos la interrupción
        stop_event = MagicMock()
        stop_event.is_set.return_value = True

        # Ejecutar el método perform_task
        self.tnt_bot.perform_task(stop_event)

        # Verificar que el usuario interrumpió el bot
        self.tnt_bot.send_message.assert_any_call("TNT task interrupted.")

    def test_send_message_boom(self):  # Simular el mensaje "Boom!"
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Ejecutar el método perform_task
        self.tnt_bot.perform_task(stop_event)

        # Verificar que se envió el mensaje "Boom!"
        self.tnt_bot.send_message.assert_any_call("Boom!")


if __name__ == "__main__":
    unittest.main()