import os
import sys
from time import sleep
plugin_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.abspath(os.path.join(plugin_dir, "..", "libs"))
if common_dir not in sys.path:
    sys.path.insert(0, common_dir)
from lib_for_mover_glaze import GlazeClient, collect_windows_with_location, do_flow_glaze, move_workspace
import asyncio

GC = GlazeClient()
#GC.connect()

query = "1 te"
flows = do_flow_glaze(GC, query)
for flow in flows:
    print(flow)
    move_workspace(GC, flow['JsonRPCAction']['parameters'])
