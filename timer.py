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

'''
import rumps
import time

app = rumps.App("Timer")

@rumps.timer(1)
def update_timer(sender):
    global start_time, timer_duration
    current_time = int(time.time() - start_time)
    if current_time >= timer_duration:
        sender.stop()
        rumps.notification("Timer Complete", "Time's up!", "icon.png")
    else:
        sender.title = f"{timer_duration - current_time} seconds remaining"

@app.menu("Start Timer")
@rumps.clicked
def start_timer(sender):
    global start_time, timer_duration
    timer_duration = int(rumps.Window(title="Enter Timer Duration", default_text="60", cancel=True).run().text)
    start_time = time.time()
    update_timer.start()

if __name__ == "__main__":
    app.run()
'''

'''
import rumps

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp().run()
'''

import rumps
import time
import argparse

class TimerApp(rumps.App):
    def __init__(self):
        super().__init__("Timer")
        self.timer = rumps.Timer(self.update_timer, 1)

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
            rumps.notification("Timer Complete", "Time's up!", "icon.png")
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

    app = TimerApp()
    app.title = f"{timer_duration} seconds remaining"
    app.run()
