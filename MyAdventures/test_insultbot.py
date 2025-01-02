import unittest
from unittest.mock import MagicMock, patch  #We simulate minecraft
from InsultBot import InsultBot
import time

class TestInsultBot(unittest.TestCase):

    def setUp(self):
        #Mock to avoid interacting with real Minecraft
        self.mock_mc = MagicMock()
        
        #Instance of InsultBot
        self.insult_bot = InsultBot()  # Aquí instanciamos el InsultBot sin parámetros

        # Mock of send_message method
        self.insult_bot.send_message = MagicMock()

    def test_perform_task(self):#simulate the task of the bot (sending insults)
        # Ensure that doesnt stop
        stop_event = MagicMock()
        stop_event.is_set.return_value = False  # non stop

        # Execute perform task
        self.insult_bot.perform_task(stop_event)

        # Verifiy that the bot has sent some of the insults
        self.insult_bot.send_message.assert_any_call("Do you even know how to play?")
        self.insult_bot.send_message.assert_any_call("You're slower than a turtle!")  

    def test_stop_task_sends_interrupt_message(self): #simulate the interruption of the bot
        # Now we simulate the interruption
        stop_event = MagicMock()
        stop_event.is_set.return_value = True  # El bot debe detenerse

        # Execute perform task 
        self.insult_bot.perform_task(stop_event)

        # Verify that the user interrupted the bot
        self.insult_bot.send_message.assert_any_call(f"{self.insult_bot.name} has been interrupted.")

    def test_random_shuffling_of_insults(self): #simulate the shuffling of the insults
        # Copy the original list of insults
        original_insults = self.insult_bot.insults[:]
        
        # Ensure that the bot does not stop
        stop_event = MagicMock()
        stop_event.is_set.return_value = False

        # Execute the perform_task method
        self.insult_bot.perform_task(stop_event)

        # Verify that the order is not the same
        self.assertNotEqual(self.insult_bot.insults, original_insults)

if __name__ == "__main__":
    unittest.main()
