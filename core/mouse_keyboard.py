import win32gui, win32con, win32api
from time import sleep
from random import randint


def find_window(name):
    def enum_windows(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowTextLength(hwnd) > 0:
            win_text = win32gui.GetWindowText(hwnd)
            if name in win_text:
                results.append(win_text)
    window_list = []
    win32gui.EnumWindows(enum_windows, window_list)
    return window_list[0] if window_list else None

class Mouse:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            raise Exception(f"Window not found: {window_name}")
        else:
            print(f"Window found: {window_name} (HWND: {self.hwnd})")

    def click(self, pos):
        # Convert screen coordinates to client coordinates
        client_pos = win32gui.ScreenToClient(self.hwnd, pos)
        # print(f"Clicking at client position {client_pos}")

        # Send WM_LBUTTONDOWN and WM_LBUTTONUP messages to the window
        lparam = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        sleep(randint(20, 80) / 1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lparam)

    def moveto(self, pos):
        # Convert screen coordinates to client coordinates
        client_pos = win32gui.ScreenToClient(self.hwnd, pos)
        # print(f"Moving to client position {client_pos}")

        # Send WM_MOUSEMOVE message to the window
        lparam = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lparam)

class Keyboard:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if self.hwnd == 0:
            raise Exception(f"Window not found: {window_name}")
        else:
            print(f"Window found: {window_name} (HWND: {self.hwnd})")

        self.keys = {
            'enter': win32con.VK_RETURN,
            'shift': win32con.VK_SHIFT,
            'down': win32con.VK_DOWN,
            'escape': win32con.VK_ESCAPE,
            'space': win32con.VK_SPACE,
            'ctrl': win32con.VK_CONTROL,
            'lctrl': win32con.VK_LCONTROL,
            'f1': win32con.VK_F1,
            'f4': win32con.VK_F4,
            'f5': win32con.VK_F5,
            'numpad2': win32con.VK_NUMPAD2,
        }

    def keydown(self, key, interval=0.1):
        # print(f"Key down: {key}")
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN, self.keys.get(key), 0)
        sleep(interval)

    def keyup(self, key, interval=0.1):
        # print(f"Key up: {key}")
        win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP, self.keys.get(key), 0)
        sleep(interval)

    def presskey(self, key, wait_after=0.1, duration=0.05):
        # print(f"Pressing key: {key}")
        if len(key) == 1:
            win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN, ord(key), 0)
            sleep(duration)
            win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP, ord(key), 0)
        else:
            win32gui.SendMessage(self.hwnd, win32con.WM_KEYDOWN, self.keys.get(key), 0)
            sleep(duration)
            win32gui.SendMessage(self.hwnd, win32con.WM_KEYUP, self.keys.get(key), 0)

        sleep(wait_after)

    def write(self, text, duration=0.01):
        for c in text:
            # print(f"Writing: {c}")
            win32gui.SendMessage(self.hwnd, win32con.WM_CHAR, ord(c), 0)
            sleep(duration)
