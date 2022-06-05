import sys
import time
import threading
from pynput import mouse
from pynput import keyboard


class AutoClicker(threading.Thread):
    def __init__(self, button_or_key=None, delay=None, is_button=True):
        super().__init__()

        self.button_or_key = button_or_key
        self.delay = delay
        self.is_button = is_button

        self.running = False
        self.program_running = True

        if is_button:
            self.controller = mouse.Controller()
        else:
            self.controller = keyboard.Controller()

    def run(self):
        while self.program_running:
            while self.running:
                if self.is_button:
                    self.controller.click(self.button_or_key)
                else:
                    self.controller.tap(self.button_or_key)

                time.sleep(self.delay / 1000)

    def toggle(self):
        self.running = not self.running
        print("[toggle]")

    def exit(self):
        self.running = False
        self.program_running = False
        print("[exit]")
        sys.exit(0)
