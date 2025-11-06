
import threading, time
from pynput.mouse import Controller, Button
import keyboard

mouse = Controller()
clicking = False
cps = 15 # clicks per second
interval = 1 / cps

def clicker():
    global clicking
    next_click = time.perf_counter()
    while True:
        if clicking:
            now = time.perf_counter()
            if now >= next_click:
                mouse.click(Button.left)
                next_click = now + interval
        else:
            time.sleep(0.01)

def toggle_clicking():
    global clicking
    clicking = not clicking
    print("STARTED" if clicking else "STOPPED")

threading.Thread(target=clicker, daemon=True).start()

print("Press I to toggle. ESC to quit.")
keyboard.add_hotkey("i", toggle_clicking)
keyboard.wait("esc")
