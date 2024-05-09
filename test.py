import can
import time

def send_one():
    try:
        # Instantiate the bus with specific settings
    #    /dev/tty.usbmodem139128701 
    #  /dev/tty.usbserial-2110
        with can.interface.Bus(interface='seeedstudio', channel='/dev/tty.usbserial-2110', baud=1000000, frame_type='EXT', timeout=0.1, operation_mode='normal', bitrate=1000000) as bus:
            msg = can.Message(
                arbitration_id=0x6969, data=[0, 0, 0, 0, 0, 0, 0, 1], is_extended_id=True
            )
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
    except can.CanError as e:
        print("Message NOT sent due to CAN error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    while True:
        send_one()
        time.sleep(1)