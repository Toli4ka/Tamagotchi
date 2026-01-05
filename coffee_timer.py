import utime

class CoffeeTimer:
    def __init__(self, total_seconds=0):
        self.running = False
        self.total_seconds = total_seconds
        self.seconds_left = total_seconds
        self.last_update = utime.ticks_ms()

    def set_time(self, total_seconds):
        self.total_seconds = total_seconds
        self.seconds_left = self.total_seconds

    def update(self):
        if self.running:
            now = utime.ticks_ms()
            if utime.ticks_diff(now, self.last_update) >= 1000:
                if self.seconds_left > 0:
                    self.seconds_left -= 1
                    self.last_update = now
                else:
                    self.running = False
                    
    def stop(self):
        self.running = False
        self.seconds_left = self.total_seconds

    def get_time(self):
        return f"{self.seconds_left // 60:02}:{self.seconds_left % 60:02}"