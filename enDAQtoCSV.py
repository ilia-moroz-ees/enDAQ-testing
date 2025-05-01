import endaq.device
import endaq.ide
import endaq
import pandas as pd
import numpy as np
import time
import os
import sys


# Check if the user provided a filename
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_file>")
    sys.exit(1)

filename = sys.argv[1]


path = filename

print("Reading the file")
doc = endaq.ide.get_doc(path)

# Get All Data
data = {doc.channels[ch].name : endaq.ide.to_pandas(doc.channels[ch], time_mode='seconds') for ch in doc.channels}

frames = [endaq.ide.to_pandas(doc.channels[ch], time_mode='seconds') for ch in doc.channels]

print("Saving 25g CSV")
try:
    frames[0].to_csv("25g.csv")
except PermissionError:
    print("file is opened. Cannot override the file")
    sys.exit()

print("Saving 40g CSV")

try:
    frames[1].to_csv("40g.csv")
except PermissionError:
    print("file is opened. Cannot override the file")
    sys.exit()

print("generated 25g.csv and 40g.csv files")

# Get Dashboard of All Channels
dashboard = endaq.plot.dashboards.rolling_enveloped_dashboard(
    data,
    num_rows=None,
    num_cols=1
)
dashboard.show()

