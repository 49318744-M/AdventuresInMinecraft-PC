# tests/test_reflective_bot.py
import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import sys
import os

# Agregar el directorio raíz del proyecto al sys.path para resolver importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ReflectiveBot import ReflectiveBot

class TestReflectiveBot(unittest.IsolatedAsyncioTestCase):

    @patch('mcpi.minecraft.Minecraft.create')  # Mockear la creación de Minecraft
    @patch('mcpi.minecraft.Minecraft.postToChat')  # Mockear el método postToChat
    def setUp(self, mock_post_to_chat, mock_minecraft_create):
        # Mockear la instancia de Minecraft
        self.mock_mc = MagicMock()
        mock_minecraft_create.return_value = self.mock_mc

        # Instanciar el ReflectiveBot con el mock_mc
        self.reflective_bot = ReflectiveBot(self.mock_mc)

    @patch("time.sleep", return_value=None)
    async def test_perform_task_reflect_command(self, mock_sleep):
        # Configurar eventos de chat simulados con comandos reflectivos
        mock_event_command = Mock()
        mock_event_command.message = "reflective greet"
        mock_event_unknown = Mock()
        mock_event_unknown.message = "reflective dance"
        self.mock_mc.events.pollChatPosts.return_value = [mock_event_command, mock_event_unknown]

        # Parchear métodos de ReflectiveBot
        self.reflective_bot.greet = Mock()
        self.reflective_bot.respond = Mock()

        # Iniciar la tarea
        stop_event = asyncio.Event()
        perform_task = asyncio.create_task(self.reflective_bot.perform_task(stop_event))

        # Permitir que la tarea ejecute una iteración
        await asyncio.sleep(0.1)

        # Detener la tarea
        stop_event.set()
        await perform_task

        # Verificar que greet haya sido llamado
        self.reflective_bot.greet.assert_called_once()

        # Verificar que respond haya sido llamado con comando desconocido
        self.reflective_bot.respond.assert_called_with("dance")

        # Verificar que se haya enviado mensaje de comando desconocido
        self.mock_mc.postToChat.assert_called_with("Unknown command: dance")

    @patch("time.sleep", return_value=None)
    async def test_perform_task_with_switching_agent(self, mock_sleep):
        # Configurar eventos de chat simulados para cambiar de agente
        mock_event_switch = Mock()
        mock_event_switch.message = "oracle"  # Suponiendo que "oracle" es otro agente
        self.mock_mc.events.pollChatPosts.return_value = [mock_event_switch]

        # Parchear send_message
        self.reflective_bot.send_message = AsyncMock()

        # Iniciar la tarea
        stop_event = asyncio.Event()
        perform_task = asyncio.create_task(self.reflective_bot.perform_task(stop_event))

        # Permitir que la tarea ejecute una iteración
        await asyncio.sleep(0.1)

        # Detener la tarea
        stop_event.set()
        await perform_task

        # Verificar que se haya enviado el mensaje de detención
        self.reflective_bot.send_message.assert_called_with("Stopping ReflectiveBot and switching to oracle.")

    def test_reflect_message(self):
        message = "Hello, world!"
        expected_response = "ReflectiveBot: Hello, world!"
        actual_response = self.reflective_bot.reflect_message(message)
        self.assertEqual(expected_response, actual_response)

if __name__ == "__main__":
    unittest.main()