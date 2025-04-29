import endaq.device
import endaq.ide
import endaq
import time
import os

device = endaq.device.getDevices()[0]
print(device.path)
path = os.path.join(device.path, "DATA\\RECORD")
print(path)

interface = endaq.device.command_interfaces.CommandInterface(device)

print(interface.canRecord)

print(device.channels)

device.startRecording()

print("Recording Started!")

while len(endaq.device.getDevices()) == 0:
    print("waiting to finish recording")
    time.sleep(1)

print(endaq.device.getDevices())

newfile = os.listdir(path)[-1] 
newfile = os.path.join(path, newfile)

doc = endaq.ide.get_doc(newfile)

# endaq.plot.utilities.set_theme('endaq')

# Get All Data
data = {doc.channels[ch].name: endaq.ide.to_pandas(doc.channels[ch], time_mode='datetime') for ch in doc.channels}

# Get Dashboard of All Channels
dashboard = endaq.plot.dashboards.rolling_enveloped_dashboard(
    data,
    num_rows=1,
    num_cols=None
)
dashboard.show()