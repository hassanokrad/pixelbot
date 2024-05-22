from time import sleep
import constants as c


class Map:
    def __init__(self, core, trajet):
        self.trajet = trajet
        self.core = core
        self.current = None

    def get_trajet(self):
        map_id = self.get_map_id()
        if map_id and int(map_id) in self.trajet:
            return self.trajet[int(map_id)]
        return self.trajet['404']

    def change(self, direction):
        if direction in c.DIRECTIONS:
            print(f'Changing map direction: {direction}')
            self.core.click(c.DIRECTIONS[direction])
            sleep(10)
        else:
            print(f'Invalid direction: {direction}')

    def get_map_id(self):
        for command in ['/clear', '/mapid']:
            self.core.press('space')
            self.core.write(command)
            sleep(0.1)
            self.core.press('enter')
            sleep(0.1)  # Wait a bit for the game to process the command

        self.current = self.core.copy_text(c.CHAT_POS).strip()
        if self.current and len(self.current) == 9 and self.current.isdigit():
            print(f'Current map ID: {self.current}')
            return self.current
        else:
            print('Failed to retrieve map ID')
            return None
