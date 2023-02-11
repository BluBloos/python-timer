# python-timer
One-shot timer invoked from cmdline for macOS

## Prerequisites

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

## Use

```bash
python timer.py -h 
```

