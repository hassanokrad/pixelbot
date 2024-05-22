from bot import Bot
import constants as c
import exceptions as e
from trajets import trajet

from threading import Thread, Lock

lock = Lock()

class Main:
    def __init__(self, bot_config):
        self.trajet = trajet[bot_config['trajet_name']]
        self.bot_name = bot_config['bot_name']
        self._bot = Bot(self.bot_name, self.trajet)
        self.stopped = False
        self.thread = None

    def start(self):
        self.stopped = False
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join()

    def run(self):
        global lock

        while not self.stopped:
            try:
                self._bot.execute_trajet()
            except e.ActionFailed:
                continue
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                break
        print(f"Bot {self.bot_name} has stopped.")

configs = {
    '1': {'bot_name': 'Owa', 'trajet_name': 'elevage_01'},
    # '2': {'bot_name': 'Essaouira', 'trajet_name': 'elevage_01'}
}

if __name__ == "__main__":
    bots = []

    for key, config in configs.items():
        print(f'Start bot: {config}')
        main = Main(config)
        main.start()
        bots.append(main)

    # Example of stopping all bots (you can adjust this as needed
    # Stopping all bots after a certain condition or time (for example, after 10 seconds)
    # import time
    # time.sleep(10)
    # for bot in bots:
    #     bot.stop()
