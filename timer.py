'''
import time
import platform
import subprocess
#import winsound

def ding():
    #if platform.system() == "Windows":
    #    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    if platform.system() == "Darwin":
        subprocess.call(["afplay", "/System/Library/Sounds/Glass.aiff"])

def start_timer(seconds):
    time.sleep(seconds)
    ding()

if __name__ == '__main__':
    timer_duration = int(input("Enter the timer duration in seconds: "))
    start_timer(timer_duration)
'''

import rumps
import time
import argparse
from subprocess import Popen

class TimerApp(rumps.App):
    def __init__(self):
        super().__init__("Timer")
        self.timer = rumps.Timer(self.update_timer, 1)
        self.start_timer(None)

    @rumps.clicked("Start Timer")
    def start_timer(self, _):
        global start_time, timer_duration
        start_time = time.time()
        self.timer.start()

    def update_timer(self, _):
        global start_time, timer_duration
        current_time = int(time.time() - start_time)
        if current_time >= timer_duration:
            self.timer.stop()
            self.title = "0 seconds remaining"
            rumps.notification("python-timer", "Time's up!", "Enjoy your break!")            
            p = Popen(["afplay", "/System/Library/Sounds/Hero.aiff"])            
        else:
            self.title = f"{timer_duration - current_time} seconds remaining"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a timer")
    parser.add_argument("duration", type=str, help="duration of the timer in the format '10h 30m' or '30m'")
    args = parser.parse_args()

    timer_duration = 0
    parts = args.duration.split(" ")
    for part in parts:
        if "h" in part:
            timer_duration += int(part.strip("h")) * 3600
        elif "m" in part:
            timer_duration += int(part.strip("m")) * 60
        elif "s" in part:
            timer_duration += int(part.strip("s"))

    app = TimerApp()
    app.title = f"{timer_duration} seconds remaining"
    app.run()
