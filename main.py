import endaq.device
import endaq.ide
import endaq
import pandas as pd
import numpy as np
import time
import os
import sys

try:
    device = endaq.device.getDevices()[0] 
except IndexError:
    print("no device found")
    sys.exit()
path = os.path.join(device.path, "DATA\\RECORD")

interface = endaq.device.command_interfaces.CommandInterface(device)

device.startRecording()

print("Recording Started!")

while len(endaq.device.getDevices()) == 0:
    print("waiting to finish recording")
    time.sleep(1)

print(endaq.device.getDevices())

newfile = os.listdir(path)[-1]
newfile = os.path.join(path, newfile)

doc = endaq.ide.get_doc(newfile)

# Get All Data
data = {doc.channels[ch].name : endaq.ide.to_pandas(doc.channels[ch], time_mode='seconds') for ch in doc.channels}

frames = [endaq.ide.to_pandas(doc.channels[ch], time_mode='seconds') for ch in doc.channels]


try:
    frames[0].to_csv("25g.csv")
except PermissionError:
    print("file is opened. Cannot override the file")
    sys.exit()

try:
    frames[1].to_csv("40g.csv")
except PermissionError:
    print("file is opened. Cannot override the file")
    sys.exit()

# Get Dashboard of All Channels
dashboard = endaq.plot.dashboards.rolling_enveloped_dashboard(
    data,
    num_rows=None,
    num_cols=1
)
dashboard.show()

