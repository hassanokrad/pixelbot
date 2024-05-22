import random
import pygetwindow
from time import sleep
import winsound
import mouse_keyboard as inactive
import win32gui
from pyperclip import paste


class Core:
    def __init__(self, name, version):
        self.window_name = f"{name} - Dofus {version}"
        self.mouse = inactive.Mouse(self.window_name)
        self.keyboard = inactive.Keyboard(self.window_name)
        self.resize_window(800, 600)
        print(f"Initialized Core for {self.window_name}")

    def keydown(self, key):
        self.keyboard.keydown(key)
        print(f"Key down: {key}")

    def keyup(self, key):
        self.keyboard.keyup(key)
        print(f"Key up: {key}")

    def press(self, key):
        self.keyboard.presskey(key)
        print(f"Key pressed: {key}")

    def write(self, message):
        self.keyboard.write(message)
        print(f"Written message: {message}")

    def move(self, pos):
        self.mouse.moveto(pos)
        print(f"Moved to position: {pos}")

    def click(self, pos):
        self.mouse.click(pos)
        print(f"Clicked at position: {pos}")

    def double_click(self, pos):
        self.click(pos)
        sleep(0.05)
        self.click(pos)
        print(f"Double clicked at position: {pos}")

    def pixel(self, pos):
        hwnd = win32gui.FindWindow(None, self.window_name)
        sleep(0.05)
        i_x, i_y = pos
        i_desktop_window_dc = win32gui.GetWindowDC(hwnd)
        long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
        i_colour = int(long_colour)
        win32gui.ReleaseDC(hwnd, i_desktop_window_dc)
        rgb = (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)
        print(f"Pixel at {pos}: {rgb}")
        return rgb

    def pixel_match(self, pos, rgb):
        sleep(0.05)
        match = rgb == self.pixel(pos)
        print(f"Pixel match at {pos}: {match}")
        return match

    def get_window(self):
        window = pygetwindow.getWindowsWithTitle(self.window_name)[0]
        print(f"Got window: {self.window_name}")
        return window

    def resize_window(self, width, height):
        window = self.get_window()
        if window.size != (width, height):
            window.maximize()
            window.resizeTo(width, height)
            if not window.isActive:
                window.moveTo(0, 0)
                window.activate()
            print(f"Resized window to: {width}x{height}")

    @staticmethod
    def beep():
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        print("Beeped")

    def random_click(self, pos):
        random_pos = (pos[0] + random.randint(1, 3), pos[1] + random.randint(1, 3))
        self.mouse.click(random_pos)
        print(f"Randomly clicked at position: {random_pos}")

    def copy_text(self, pos):
        sleep(0.1)
        self.double_click(pos)
        sleep(0.1)
        self.hotkey_copy()
        copied_text = paste()
        print(f"Copied text: {copied_text}")
        return copied_text

    def hotkey_copy(self, duration=0.05):
        sleep(duration)
        self.keydown('ctrl')
        sleep(duration)
        self.press('C')
        sleep(duration)
        self.keyup('ctrl')
        sleep(duration)
        print("Performed hotkey copy")
