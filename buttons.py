from machine import Pin, Timer

class Button:
    def __init__(self, pin_num, name, debounce_ms=200):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.button_pressed)
        self.debounce_ms = debounce_ms
        self.name = name
        self._just_pressed = False
        self.debounce_timer = None

    def reset_debounce(self, timer): # timer parameter for callback
        self.debounce_timer = None

    def button_pressed(self, pin): # pin parameter for handler
        if self.debounce_timer is None:
            self._just_pressed = True
            self.debounce_timer = Timer(-1)
            self.debounce_timer.init(
                mode=Timer.ONE_SHOT, 
                period=self.debounce_ms, 
                callback=self.reset_debounce)

    def was_pressed(self):
        if self._just_pressed:
            self._just_pressed = False
            return True
        return False
    

class Buttons():
    def __init__(self, button_pins):
        self.buttons = [Button(pin, name) for name, pin in button_pins.items()]
        self.button_map = {btn.name: btn for btn in self.buttons}

    def get_all_pressed(self):
        """Get dict of all button states and clear all flags"""
        return {btn.name: btn.was_pressed() for btn in self.buttons}

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