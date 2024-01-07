import rumps
import time
import argparse
from subprocess import Popen
import os

def send_notification(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def formatTimeLeft(remaining):
    hours, remainder = divmod(remaining, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s remaining"

class TimerApp(rumps.App):
    def __init__(self, description):
        super().__init__("Timer")
        self.description = description  # Store the timer description
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
            # TODO: can we make this a time-sensitive notification?
            send_notification(title    = 'python-timer',
                              subtitle = f'task "{self.description}" complete.',
                              message  = 'Enjoy your break!')
            Popen(["afplay", "/System/Library/Sounds/Hero.aiff"])            
        else:
            self.title = formatTimeLeft(timer_duration - current_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a timer")
    parser.add_argument("duration", type=str, help="duration of the timer in the format '10h 30m 3s', for example")
    parser.add_argument("description", type=str, help="description of the timer")  # New argument for description
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

    app = TimerApp(args.description)  # Pass the description to the TimerApp
    app.title = formatTimeLeft(timer_duration)
    app.run()
