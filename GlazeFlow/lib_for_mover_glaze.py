import json
import subprocess


def move_workspace(GC, input_string):
    parameters = input_string.split(";")
    if str(parameters[3]) < str(parameters[2]):
        #print("left")
        GC.send_command(["glazewm", "command", "focus", "--workspace", parameters[1]])
        GC.send_command(["glazewm",'command', 'move-workspace', '--direction', 'left'])
    elif str(parameters[3]) > str(parameters[2]):
        #print("right")
        GC.send_command(["glazewm","command", "focus", "--workspace", parameters[1]])
        GC.send_command(["glazewm",'command', 'move-workspace', '--direction', 'right'])
    else:
        GC.send_command(["glazewm","command", "focus", "--workspace", parameters[1]])
        #print("equal")
    return

def do_flow_glaze(GC, query_input):
    try:
        monitor_chosen, query = query_input.split(" ", 1)
    except:
        monitor_chosen = 1
        query = 0
    monitors = GC.get_monitors()
    windows = collect_windows_with_location(monitors['data']['monitors'])
    to_send = []
    if not query:
        for title, window in windows.items():
            r = {
                "Title":title,
                "SubTitle":"Click to activate this window",
                "IcoPath":"",
                "JsonRPCAction":{"method": "action", "parameters": [f'{window['id']};{window['workspace_name']};{str(window['monitor_idx'])};{monitor_chosen}']}
                #"JsonRPCAction":{"method": "action", "parameters": [window['id'], window['workspace_name'], str(window['monitor_idx']), monitor_chosen]}
                #JsonRPCAction=plugin.action(action, [window['hwnd']])
            }
            to_send.append(r)     
        return to_send
    query_lower = query.lower()
    matching_windows = filter_by_key_substring(windows, query_lower)
    for title, window in matching_windows.items():
        r = {
            "Title":title,
            "SubTitle":"Click to activate this window",
            "IcoPath":"",
            "JsonRPCAction":{"method": "action", "parameters": [f'{window['id']};{window['workspace_name']};{str(window['monitor_idx'])};{monitor_chosen}']}
                  #JsonRPCAction=plugin.action(action, [window['hwnd']])
            }
        to_send.append(r)
    return to_send

def filter_by_key_substring(data: dict, substring: str) -> dict:
    return {k: v for k, v in data.items() if substring in k.lower()}    

def collect_windows_with_location(monitors):
    all_windows = {}
    def recurse(node, monitor_idx=None, workspace_name=None):
        node_type = node.get("type")
        if node_type == "monitor":
            monitor_idx = monitors.index(node)
        elif node_type == "workspace":
            workspace_name = node.get("name")
        elif node_type == "window":
            title = node.get("title")
            while title in all_windows:
                title += 'I' 
            all_windows[title] = {
                "id": node.get("id"),
                "workspace_name": workspace_name,
                "monitor_idx": monitor_idx
            }     
        # Recurse into children
        for child in node.get("children", []):
            recurse(child, monitor_idx, workspace_name)
    for monitor in monitors:
        recurse(monitor)
    return all_windows

class GlazeClient:
    # === Sync versions ===
    def get_monitors(self):
        proc = subprocess.run(["glazewm", "query", "monitors"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        #print(f'yello {proc.stdout}')
        data = json.loads(proc.stdout.decode("utf-8"))
        return data
#    def get_monitors(self):
#        return self._run(self._get_monitors())
#    def get_monitors(self):

#    def get_workspaces(self):

    def send_command(self, command):
        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
