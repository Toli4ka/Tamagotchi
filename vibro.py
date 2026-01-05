from machine import Pin, Timer

class VibroMotor():
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.OUT)
        self.vibro_timer = Timer(-1)
    
    def vibro_off(self, timer):
        self.pin.value(0)

    def vibrate(self, duration_ms):
        self.pin.value(1) # start vibration
        self.vibro_timer.init(mode=Timer.ONE_SHOT, period=duration_ms, callback=self.vibro_off)

    # TODO: implement multiple pulses