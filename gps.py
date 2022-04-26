import serial
import pynmea2

def get_coords():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
    while True:
        try:
            line = ser.readline().decode("ascii")
            # print(line)
            msg = pynmea2.parse(line)
            if isinstance(msg, pynmea2.types.talker.RMC):
                if msg.status == 'V':
                    print('no fix')
                    continue
                else:
                    coords = (msg.longitude, msg.latitude)
                    return coords
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
        except pynmea2.ParseError as e:
            print(f'[navigation] Parse error: {e}')
            continue
    return ()  # (181, 91)


def fix():
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
    print('[navigation] searching for fix...')
    while True:
        try:
            msg = pynmea2.parse(ser.readline().decode("ascii"))
            if isinstance(msg, pynmea2.types.talker.GGA):
                if msg.gps_qual != 0:
                    # print(f'got a fix of type {msg.gps_qual}, {msg.num_sats} satellites')
                    return
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
        except pynmea2.ParseError as e:
            print(f'\t[navigation] Parse error: {e}')
