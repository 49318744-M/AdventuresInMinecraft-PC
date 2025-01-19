import unittest
import asyncio
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ReflectiveBot import ReflectiveBot

class TestReflectiveBot(unittest.IsolatedAsyncioTestCase):

    @patch.object(ReflectiveBot, 'send_message')
    def test_greet(self, mock_send_message):
        """
        Verifica que greet() llama a send_message con el texto correcto.
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        # Llamamos directamente, sin await, porque greet() es sincrónico
        bot.greet()

        mock_send_message.assert_called_once_with("Hello, I'm your reflective bot")

    @patch.object(ReflectiveBot, 'send_message')
    def test_bye(self, mock_send_message):
        """
        Verifica que bye() llama a send_message con el texto correcto.
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        bot.bye()

        mock_send_message.assert_called_once_with("Bye, see you next time!")

    @patch.object(ReflectiveBot, 'send_message')
    def test_help(self, mock_send_message):
        """
        Verifica que help() llama a send_message con la lista de comandos.
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        bot.help()

        mock_send_message.assert_called_once_with("Available commands: greet, help, joke, bye, place_block")

    @patch.object(ReflectiveBot, 'send_message')
    def test_joke(self, mock_send_message):
        """
        Verifica que joke() llama a send_message con la broma.
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        bot.joke()

        mock_send_message.assert_called_once_with("joke joke joke.")

    @patch.object(ReflectiveBot, 'send_message')
    def test_place_block(self, mock_send_message):
        """
        Verifica que place_block():
          - Pide la posición al jugador,
          - Coloca el bloque diamante (id=57),
          - Manda mensaje "Placed a diamond block..."
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        # Preparamos la posición
        pos_mock = MagicMock()
        pos_mock.x = 10
        pos_mock.y = 64
        pos_mock.z = 10
        mc_mock.player.getTilePos.return_value = pos_mock

        with patch('mcpi.block.DIAMOND_BLOCK.id', new=57):
            bot.place_block()
            mc_mock.setBlock.assert_called_with(10, 63, 10, 57)
            mock_send_message.assert_called_once_with("Placed a diamond block under your feet!")

    @patch.object(ReflectiveBot, 'send_message')
    async def test_interrupt_functionality(self, mock_send_message):
        """
        Testea que perform_task() se detiene cuando se setea stop_event,
        y postea 'ReflectiveBot has been interrupted.'
        """
        mc_mock = MagicMock()
        bot = ReflectiveBot(mc_mock)

        stop_event = asyncio.Event()
        task = asyncio.create_task(bot.perform_task(stop_event))

        # Dejamos que arranque un poco (envíe su mensaje inicial)
        await asyncio.sleep(0.1)

        # Detenemos
        stop_event.set()
        await task

        # Revisamos que en algún momento haya posteado "ReflectiveBot has been interrupted."
        mock_send_message.assert_any_call("ReflectiveBot has been interrupted.")

        # También debe haber posteado algo como "ReflectiveBot is active..." y help()
        mock_send_message.assert_any_call("ReflectiveBot is active. Type 'reflective <command>' to interact.")
        mock_send_message.assert_any_call("Available commands: greet, help, joke, bye, place_block")


if __name__ == '__main__':
    unittest.main()