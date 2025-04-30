import can

# === CAN Configuration ===
channel = 'PCAN_USBBUS1'        # Update if needed
bitrate = 500000
interface = 'pcan'

def construct_can_frame(physical_value):
    raw = int((physical_value - 0) / 1)  # Factor = 1, Offset = 0
    raw_bytes = raw.to_bytes(2, byteorder='little')  # 2 bytes, little-endian

    data = [0x00] * 8  # Initialize all 8 bytes to zero
    data[1] = raw_bytes[0]  # LSB goes to byte 1 (bit 8)
    data[2] = raw_bytes[1]  # MSB goes to byte 2 (bit 16)
    
    return data

# === Initialize CAN Bus ===
try:
    bus = can.interface.Bus(channel=channel, bustype=interface, bitrate=bitrate)
except Exception as e:
    print(f"Error initializing CAN bus: {e}")
    exit(1)

# === Function to Send Message ===
def send_can_message(value):
    can_id = 0x123
    data = construct_can_frame(value)
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    try:
        bus.send(msg)
        print(f"Message sent: ID={hex(can_id)}, Data={data}")
    except can.CanError as e:
        print(f"Failed to send CAN message: {e}")

# === Console Loop ===
print("Press Enter to send a CAN message (type 'q' to quit)")
while True:
    user_input = input()
    if user_input.lower() == 'q':
        print("Exiting.")
        break
    send_can_message(int(user_input))