import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InsultBot import InsultBot

class TestInsultBot(unittest.IsolatedAsyncioTestCase):
    
    #Test 1
    def test_initialization(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        
        self.assertEqual(bot.name, "InsultBot")
        self.assertIsInstance(bot.insults, list)
        self.assertTrue(len(bot.insults) > 0)


    #Test 2
    # Prueba para verificar que el bot maneja correctamente una lista vacía de insultos
    def test_empty_insult_list(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        bot.insults = []  # Establecer la lista de insultos como vacía
        
        self.assertEqual(bot.insults, [])
        self.assertEqual(bot.get_random_insult(), "No insults available.")

    #Test 3
    # Prueba para verificar que el bot maneja correctamente un solo insulto
    def test_single_insult(self):
        mock_mc = MagicMock()
        bot = InsultBot(mock_mc)
        bot.insults = ["You fight like a dairy farmer!"]
        
        self.assertEqual(bot.get_random_insult(), "You fight like a dairy farmer!")

if __name__ == '__main__':
    unittest.main()