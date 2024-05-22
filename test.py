import win32api
import win32con
import pyperclip
import time
from core.mouse_keyboard import Mouse, Keyboard

def get_mouse_position():
    return win32api.GetCursorPos()

def copy_to_clipboard(text):
    pyperclip.copy(text)

# Find the target window
window_name = "Owa - Dofus 2.71.6.10"
mouse = Mouse(window_name)
keyboard = Keyboard(window_name)

def main():
    print("Press 'Ctrl+C' to copy the mouse position to the clipboard.")
    print("Press 'Ctrl+Q' to exit.")

    try:
        while True:
            if win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetAsyncKeyState(ord('C')):
                # Get mouse position in screen coordinates
                screen_pos = get_mouse_position()
                print(f"Screen position: {screen_pos}")

                # Copy to clipboard
                pos_str = f"({screen_pos[0]}, {screen_pos[1]})"
                copy_to_clipboard(pos_str)
                print(f"Copied to clipboard: {pos_str}")

                # Debounce the key press
                time.sleep(0.5)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Script terminated by user")

if __name__ == "__main__":
    main()
