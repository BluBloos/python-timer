import rumps
import time
import argparse
from subprocess import Popen
import os
import requests
import base64

def send_notification(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def formatTimeLeft(remaining, desc):
    hours, remainder = divmod(remaining, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{desc} - {int(hours)}h {int(minutes)}m {int(seconds)}s remaining"

TOGGL_API_TOKEN = "token"
TOGGL_PROJECT_ID = None
DEBUG = False

chosen_workspace_id = 0
mapping = None # shortname to project ID.

def init_toggl_api_token():

    global TOGGL_API_TOKEN

    # Construct the file path for the token file
    token_file_path = os.path.join(os.path.expanduser('~'), 'toggl_track.token.txt')

    try:
        # Open the file and read the token
        with open(token_file_path, 'r') as file:
            token = file.read().strip()  # strip() removes any leading/trailing whitespace
        TOGGL_API_TOKEN = token
        print("found API token", TOGGL_API_TOKEN)
    except FileNotFoundError:
        print("Toggl Track token file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def encode_auth():
    global TOGGL_API_TOKEN
    token = f'{TOGGL_API_TOKEN}:api_token'
    encoded_token = base64.b64encode(token.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_token}'
    }
    return headers

def get_projects(workspace_id):
    headers = encode_auth()
    response = requests.get(f"https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/projects", headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response
        return response.json()
    else:
        # Handle errors (you can expand on this as needed)
        return f"Error: {response.status_code}"

# Function to read project mappings from the file
def read_project_mappings(file_path):
    mapping = {}
    with open(file_path, 'r') as file:
        for line in file:
            toggl_name, short_name = line.strip().split(' = ')
            mapping[toggl_name] = short_name
    return mapping

# Main function to create the shortname to project ID mapping
def create_shortname_to_id_mapping(workspace_id , file_path):
    toggl_projects = get_projects(workspace_id )
    file_mappings = read_project_mappings(file_path)

    shortname_to_id = {}
    for project in toggl_projects:
        toggl_name = project['name']
        if toggl_name in file_mappings:
            short_name = file_mappings[toggl_name]
            shortname_to_id[short_name] = project['id']

    return shortname_to_id


def get_workspaces():

    headers = encode_auth()
    response = requests.get('https://api.track.toggl.com/api/v9/workspaces', headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed to fetch workspaces", response)
        return None

def log_time_to_toggl(description, duration, project_shortname):

    global mapping
    global start_time

    headers = encode_auth()
    headers['Content-Type'] = 'application/json'
    data = {
        "description": description,
        "duration": duration,
        "tags": [],
        "start": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_time)) + 'Z',
        "created_with": "python-timer",
        "workspace_id": chosen_workspace_id,
    }

    if project_shortname != None and project_shortname in mapping:
        data["project_id"] = mapping[project_shortname]

    if DEBUG:
        print(data)
        print(headers)

    response = requests.post(f'https://api.track.toggl.com/api/v9/workspaces/{chosen_workspace_id}/time_entries', json=data, headers=headers)
    print(response)
    return response.ok

class TimerApp(rumps.App):

    def __init__(self, description, project_shortname):
        super().__init__("Timer")
        
        # Add menu items for Finish Early and Pause
        self.menu.add(rumps.MenuItem("Finish Early", callback=self.finish_early))
        #self.menu.add(rumps.MenuItem("Pause", callback=self.toggle_pause))
        
        self.description = description  # Store the timer description
        self.project_shortname = project_shortname
        self.timer = rumps.Timer(self.update_timer, 1)
        self.start_timer(None)

    def finish_early(self, _):
        actual_duration = int(time.time() - start_time)
        self.complete_timer(actual_duration)

    @rumps.clicked("Start Timer")
    def start_timer(self, _):
        global start_time, timer_duration
        start_time = time.time()
        self.timer.start()

    def complete_timer(self, duration):
        self.timer.stop()
        self.title = "0 seconds remaining"
        # TODO: can we make this a time-sensitive notification?
        send_notification(title    = 'python-timer',
                            subtitle = f'task "{self.description}" complete.',
                            message  = 'Enjoy your break!')
        if log_time_to_toggl(self.description, duration, self.project_shortname):
            print("Time logged to Toggl Track successfully.")
        else:
            print("Failed to log time to Toggl Track.")
        Popen(["afplay", "/System/Library/Sounds/Hero.aiff"])  

    def update_timer(self, _):
        global start_time, timer_duration
        current_time = int(time.time() - start_time)
        if current_time >= timer_duration:
            self.complete_timer(timer_duration)          
        else:
            self.title = formatTimeLeft(timer_duration - current_time, self.description)

if __name__ == "__main__":

    init_toggl_api_token()

    workspaces = get_workspaces()
    if workspaces:
        print("Workspaces loaded successfully.")
        if DEBUG:
            print(workspaces)
        # You can now choose a workspace and use its ID for logging time
        chosen_workspace_id = workspaces[0]['id']  # Example: choosing the first workspace
        # Then, use log_time_to_toggl() function with the chosen_workspace_id
        print("chosen workspace ID=", chosen_workspace_id)

    # init the project ID mapping.
    try:
        projects_file_path = os.path.join(os.path.expanduser('~'), 'toggl_track.projects.txt')
        mapping = create_shortname_to_id_mapping(chosen_workspace_id,  projects_file_path )
        print(mapping)
    except Exception as e:
        print(f"An error occurred: {e}")

    parser = argparse.ArgumentParser(description="Start a timer")
    parser.add_argument("duration", type=str, help="duration of the timer in the format '10h 30m 3s', for example")
    parser.add_argument("description", type=str, help="description of the timer")  # New argument for description
    # Add an optional argument for project shortname with `-p`
    parser.add_argument("-p", "--project", type=str, help="project shortname", default=None)

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

    app = TimerApp(args.description,  args.project )  # Pass the description to the TimerApp
    app.title = formatTimeLeft(timer_duration, app.description)
    app.run()
