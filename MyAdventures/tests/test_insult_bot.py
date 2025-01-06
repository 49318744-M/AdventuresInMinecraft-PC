# tests/test_insult_bot.py
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import asyncio
import sys
import os

# Agregar el directorio raíz del proyecto al sys.path para resolver importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from InsultBot import InsultBot

class TestInsultBot(unittest.IsolatedAsyncioTestCase):
    
    def test_initialization(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        self.assertEqual(bot.name, "InsultBot")
        self.assertIsInstance(bot.insults, list)
        self.assertTrue(len(bot.insults) > 0)

   
    @patch("asyncio.sleep", new_callable=AsyncMock)  # Parchear asyncio.sleep
    async def test_perform_task_stop_event(self, mock_sleep):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        # Mock send_message como AsyncMock (asíncrono)
        bot.send_message = AsyncMock()
        
        stop_event = asyncio.Event()
        stop_event.set()  # Establecer el evento de parada inmediatamente
        
        # Ejecutar perform_task
        await bot.perform_task(stop_event)
        
        # Verificar que no se enviaron mensajes
        self.assertFalse(bot.send_message.called)

    @patch('random.shuffle')
    @patch("asyncio.sleep", new_callable=AsyncMock)  # Parchear asyncio.sleep
    async def test_insult_shuffling(self, mock_sleep, mock_shuffle):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        # Mock send_message como AsyncMock (asíncrono)
        bot.send_message = AsyncMock()
        
        stop_event = asyncio.Event()
        
        # Ejecutar perform_task en segundo plano
        task = asyncio.create_task(bot.perform_task(stop_event))
        
        # Permitir que perform_task ejecute algunas iteraciones
        await asyncio.sleep(0.2)  # Permite que el event loop procese las coroutines pendientes
        
        # Detener la tarea
        stop_event.set()
        await task
        
        # Verificar que random.shuffle fue llamado al menos una vez
        self.assertTrue(mock_shuffle.called)
    
    

if __name__ == '__main__':
    unittest.main()