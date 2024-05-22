from bot.bot import Bot
import core.exceptions as e
from threading import Thread, Lock
from core.map import Map

lock = Lock()

class Main:
    def __init__(self, bot_config):
        self.bot_name = bot_config['bot_name']
        self._bot = Bot(self.bot_name)
        self.map = Map(self._bot.core)

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.thread.join()

    def run(self):
        global lock

        while True:
            try:
                self._bot.execute_trajet()
            except e.ActionFailed:
                continue
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                break
        print(f"Bot {self.bot_name} has stopped.")

configs = {
    '1': {'bot_name': 'Owa'},
}

if __name__ == "__main__":

    for key, config in configs.items():
        print(f'Start bot: {config}')
        main = Main(config)
        main.start()
