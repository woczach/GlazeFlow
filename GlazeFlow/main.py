from pyflowlauncher import Plugin, Result, send_results
from pyflowlauncher.result import ResultResponse
import os
import sys
plugin_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.abspath(os.path.join(plugin_dir, "..", "libs"))
if common_dir not in sys.path:
    sys.path.insert(0, common_dir)
#from lib_for_mover_glaze import  do_flow_glaze, focus_window_glaze
from lib_for_mover_glaze import GlazeClient, do_flow_glaze, move_workspace
# Monitor 0 (far left) win32gui.MoveWindow(hwnd, -5760, 0, 1536, 960, True)
# Monitor 2 win32gui.MoveWindow(hwnd, 0, 0, 1920, 1080, True)
# Monitor 1  win32gui.MoveWindow(hwnd, -1920, 0, 1920, 1080, True)

plugin = Plugin()
GC = GlazeClient()
    

@plugin.on_method
def query(query: str) -> ResultResponse:
    to_sent = []
    for window in do_flow_glaze(GC, query):  
        r = Result(
            Title=window['Title'],
            SubTitle=window['SubTitle'],
            IcoPath=window['IcoPath'] if window['IcoPath'] else "",
            JsonRPCAction=window['JsonRPCAction']
        )
        to_sent.append(r)
    return send_results(to_sent)

@plugin.on_method    
def action(params: list[str]):
    hwnd = params[0] if isinstance(params, list) else params
    move_workspace(GC, hwnd)
    


plugin.run()
