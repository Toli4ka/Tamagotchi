from machine import Pin
import utime

class Button:
    def __init__(self, pin_num, name, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.name = name
        self.debounce_ms = debounce_ms
        self._last_state = self.pin.value()
        self._last_time = utime.ticks_ms()
        self._just_pressed = False

    def update(self):
        current_state = self.pin.value()
        now = utime.ticks_ms()
        self._just_pressed = False
        if current_state != self._last_state:
            if utime.ticks_diff(now, self._last_time) > self.debounce_ms:
                self._last_state = current_state
                self._last_time = now
                if current_state == 0:  # Button pressed (active low)
                    self._just_pressed = True

    def was_pressed(self):
        # Returns True only once, on the frame the button was pressed.
        return self._just_pressed


class Buttons():
    def __init__(self, button_pins):
        self.buttons = [Button(pin, name) for name, pin in button_pins.items()]
        self.button_map = {btn.name: btn for btn in self.buttons}

    def update(self):
        for btn in self.buttons:
            btn.update()

    def was_pressed(self, name):
        return self.button_map[name].was_pressed()

# --- Example usage in main.py ---

# from buttons import Buttons
# BUTTON_PINS = {'left': 2, 'middle': 3, 'right': 4}
# buttons = Buttons(BUTTON_PINS)
# 
# while True:
#     buttons.update()
#     if buttons.was_pressed('left'):
#         print("Left pressed")
#     if buttons.was_pressed('middle'):
#         print("Middle pressed")
#     if buttons.was_pressed('right'):
#         print("Right pressed")
#     utime.sleep_ms(10)