#from pyflowlauncher import Plugin, Result, Method
#from pyflowlauncher.result import ResultResponse
import win32gui
import win32con
import win32api
import os
import sys

import asyncio
import websockets
import json
    
async def collect_windows_glaze():
    uri = "ws://localhost:6123"
    async with websockets.connect(uri) as websocket:
        await websocket.send("query windows")
        response = await websocket.recv()
        json_response = json.loads(response)
    return json_response
    
def enum_window_titles():
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER)
            visible = win32gui.IsWindowVisible(hwnd)
            exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            rect = win32gui.GetWindowRect(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if class_name == 'Windows.UI.Core.CoreWindow':
                return
            if exstyle & win32con.WS_EX_TOOLWINDOW:
                something = "1"
            else:
                something = "0"
                
            if title:
                titles.append({"owner": owner, "hwnd": hwnd, "title": title, "visible": visible, "something": something, "rect": rect, "class_name": class_name})
        return True

    titles = []
    win32gui.EnumWindows(callback, titles)
    return titles

windows = enum_window_titles()
for window in windows:
    r = window
    print(r)

monitors = win32api.EnumDisplayMonitors()
for i, (hMonitor, hdcMonitor, rect) in enumerate(monitors):
    print(f"Monitor {i}: {rect}")



windows = enum_window_titles() 
for w in windows:
    print(w)

some = asyncio.run(collect_windows_glaze())

print("##")
print("##")

for win in some['data']['windows']:
    print(win)

print("##")
print("##")
titles1 = {item['title'] for item in windows}
titles2 = {item['title'] for item in some['data']['windows']}
diff_titles = titles1.symmetric_difference(titles2)

diff_dicts = [d for d in windows + some['data']['windows'] if d['title'] in diff_titles]
for line in diff_dicts:
    print(line)

