# tests/test_tnt_bot.py
import asyncio
import unittest
from unittest.mock import Mock, AsyncMock
import sys
import os

# Agregar el directorio raíz del proyecto al sys.path para resolver importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TNTbot import TNTBot

class TestTNTBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_mc = Mock()
        self.tnt_bot = TNTBot(self.mock_mc)

    async def test_perform_task_normal_execution(self):
        # Configurar posición del jugador
        mock_position = Mock(x=50, y=70, z=50)
        self.mock_mc.player.getTilePos.return_value = mock_position

        # Parchear send_message
        self.tnt_bot.send_message = AsyncMock()

        # Iniciar la tarea
        stop_event = asyncio.Event()
        task = asyncio.create_task(self.tnt_bot.perform_task(stop_event))

        # Permitir que perform_task ejecute todas las iteraciones
        await asyncio.sleep(0.2)  # Permite que el event loop procese las coroutines pendientes

        # Detener el bucle
        stop_event.set()
        await task

        # Verificar que se envió el mensaje "Boom!"
        self.tnt_bot.send_message.assert_called_with("Boom!")

    async def test_perform_task_with_exception(self):
        # Configurar para lanzar una excepción al obtener la posición del jugador
        self.mock_mc.player.getTilePos.side_effect = Exception("Test exception")

        # Parchear send_message
        self.tnt_bot.send_message = AsyncMock()

        # Iniciar la tarea
        stop_event = asyncio.Event()
        await self.tnt_bot.perform_task(stop_event)

        # Verificar que se envió el mensaje de error
        self.tnt_bot.send_message.assert_called_with("Error getting player position: Test exception")

    async def test_perform_task_interrupted(self):
        # Configurar posición del jugador
        mock_position = Mock(x=50, y=70, z=50)
        self.mock_mc.player.getTilePos.return_value = mock_position

        # Parchear send_message
        self.tnt_bot.send_message = AsyncMock()

        # Iniciar la tarea
        stop_event = asyncio.Event()
        task = asyncio.create_task(self.tnt_bot.perform_task(stop_event))

        # Interrumpir la tarea inmediatamente
        stop_event.set()
        await task

        # Verificar que se envió el mensaje de interrupción
        self.tnt_bot.send_message.assert_called_with("TNT task interrupted.")

if __name__ == "__main__":
    unittest.main()