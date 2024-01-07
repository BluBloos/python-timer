# python-timer

Countdown timer invoked from cmdline for macOS.

## Features

- Specify the countdown duration using hours (h), minutes (m), and seconds (s).
  You can include or omit any of these units. e.g. '10h 30m 3s'.
- Specify the task description.
- Integration with Toggl Track to log the timed task once complete.

## Usage

```bash
python timer.py -h 
```

```bash
python script_name.py [-h] duration description
```

## Prerequisites

Install a text file called "toggl_track.token.txt" in home directory. It should
contain a single line with the Toggl Track API token.

```bash
brew install terminal-notifier
```

```
python -m pip install -r requirements.txt
```

### Force past focus status

Set `terminal-notifier` allowed for notifs during whatever focus session you expect yourself to be in when you are running these timers.
For some reason there seems to be two `terminal-notifier` apps getting recognized by macOS - safe to set both.

<img width="662" alt="Screen Shot 2023-02-11 at 5 30 21 PM" src="https://user-images.githubusercontent.com/38915815/218283827-3da29994-a64b-4747-9e63-977cd9f67fcf.png">
