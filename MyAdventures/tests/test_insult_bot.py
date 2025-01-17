import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InsultBot import InsultBot

class TestInsultBot(unittest.IsolatedAsyncioTestCase):
    
    def test_initialization(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        self.assertEqual(bot.name, "InsultBot")
        self.assertIsInstance(bot.insults, list)
        self.assertTrue(len(bot.insults) > 0)

    @patch("random.shuffle", lambda x: x)  # Evitar la aleatoriedad en las pruebas
    @patch("asyncio.sleep", new_callable=AsyncMock)  # Parchear asyncio.sleep
    async def test_perform_task(self, mock_sleep):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        # Mock send_message como AsyncMock (asíncrono)
        bot.send_message = AsyncMock()
        
        stop_event = asyncio.Event()
        
        # Ejecutar perform_task en segundo plano
        task = asyncio.create_task(bot.perform_task(stop_event))
        
        # Permitir que perform_task ejecute algunas iteraciones
        await asyncio.sleep(2)  # Aumentar el tiempo de espera para permitir más iteraciones
        
        # Verificar que se enviaron algunos insultos
        self.assertTrue(bot.send_message.called)
        
        # Detener la tarea
        stop_event.set()
        await task
        
        # Verificar que send_message fue llamado con al menos un insulto
        self.assertTrue(bot.send_message.called)


    # Prueba para verificar que el bot maneja correctamente una lista vacía de insultos
    def test_empty_insult_list(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        bot.insults = []  # Establecer la lista de insultos como vacía
        
        self.assertEqual(bot.insults, [])
        self.assertEqual(bot.get_random_insult(), "No insults available.")

    # Prueba para verificar que el bot maneja correctamente un solo insulto
    def test_single_insult(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        bot.insults = ["You fight like a dairy farmer!"]
        
        self.assertEqual(bot.get_random_insult(), "You fight like a dairy farmer!")

if __name__ == '__main__':
    unittest.main()