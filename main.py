from bot.bot import Bot
import core.exceptions as e
from threading import Thread, Lock
from core.map import Map
from core.config import Config
from core.mouse_keyboard import find_window

lock = Lock()

class Main:
    def __init__(self, bot_name, config):
        self.bot_name = bot_name
        self._bot = Bot(self.bot_name, config)
        self.map = Map(self._bot.core, config)

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        if self.thread.is_alive():
            self.thread.join()

    def run(self):
        global lock

        while True:
            try:
                # Use the map's get_trajet method to perform actions
                trajet = self.map.get_trajet()
                print(trajet)
                self._bot.execute_trajet(trajet)
            except e.ActionFailed:
                continue
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                break
        print(f"Bot {self.bot_name} has stopped.")

if __name__ == "__main__":
    config = Config('trajets/trajets.json')
    dofus_window = find_window("Owa")
    if not dofus_window:
        print("Error: No Dofus window found.")
    else:
        bot_name = dofus_window  # Assuming the window name is the bot name
        bot_config = config.get_bot_config(bot_name)
        print(bot_config)
        if not bot_config:
            print(f"No configuration found for bot: {bot_name}")
        else:
            print(f'Starting bot: {bot_name}')
            main_instance = Main(bot_name, config)
            main_instance.start()

            # Optional: Add logic to stop the bot gracefully
            try:
                main_instance.thread.join()
            except KeyboardInterrupt:
                main_instance.stop()
