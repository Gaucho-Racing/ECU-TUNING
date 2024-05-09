import can

def send_one():
    try:
        # Instantiate the bus with specific settings
        with can.interface.Bus(interface='seeedstudio', channel='/dev/cu', bitrate=500000) as bus:
            msg = can.Message(
                arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
            )
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
    except can.CanError as e:
        print("Message NOT sent due to CAN error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    send_one()