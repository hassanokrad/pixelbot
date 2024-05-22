from core import Core, Map
from time import sleep
import core.exceptions as e
import core.constants as c

class Bot:
    def __init__(self, bot_name):
        self.core = Core(bot_name, c.DOFUS_VERSION)
        self.map = Map(self.core)
        self.map_echec = 0

    def ui_remover(self):
        for _ in range(6):
            sleep(0.4)
            if self.core.pixel_match(*c.MENU_TITLE_POS):
                self.core.press('escape')
                break
            else:
                self.core.press('escape')
        print("UI removed if present.")

    def check_action(self, pos_rgb):
        return self.core.pixel_match(pos_rgb[:2], pos_rgb[2:])

    def make_action(self, pos, timeout=6):
        self.core.click(pos)
        sleep(timeout)

    def execute_action(self, actions):
        for action in actions:
            if isinstance(action, str):
                self.map_404(action)
                continue

            # Convert list to tuple if necessary
            if isinstance(action, list):
                action = tuple(action)

            self.make_action(action[:2])
            if len(action) == 7:
                if not self.check_action(action[2:]):
                    self.ui_remover()
                    raise e.ActionFailed

    def execute_move(self, move):
        print(f'Executing move: {move}')
        self.map.change(move)

    def execute_trajet(self):
        try:
            trajet = self.map.get_trajet()
            if 'action' in trajet:
                self.execute_action(trajet['action'])
            if 'move' in trajet:
                self.execute_move(trajet['move'])
        except e.TooManyAttempts:
            print("Too many failed attempts. Stopping bot.")
            self.stop()
        except e.ActionFailed:
            print("Action failed. Retrying...")
            # Continue to retry as per the initial logic.
        except Exception as ex:
            print(f"Unexpected errors: {ex}")
            self.stop()

    def map_404(self, action):
        if self.map_echec >= 3:
            raise e.TooManyAttempts
        print(f'Action not found, attempting recovery action: {action}')
        self.core.press(action)
        self.map_echec += 1

    def connect(self):
        if self.is_disconnect():
            self.core.beep()
            for _ in range(3):
                self.core.press('enter')
                sleep(10)
        return True

    def is_disconnect(self):
        try:
            self.core.get_window()
            return False
        except IndexError:
            print("Disconnected detected.")
            raise e.Disconnected

    def stop(self):
        print(f"Stopping bot.")
        # Implement additional cleanup if needed

