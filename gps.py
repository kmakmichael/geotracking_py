import serial
from struct import pack, unpack
import pynmea2


def parse(msg):
    if len(msg) > 4:
        fix = msg[1].decide('ascii')
        lat = pack('>d', unpack('<d', msg[3:7]))
        lng = pack('>d', unpack('<d', msg[8:12]))
        print(f'[navigation] parse: {msg} -> ({fix}:{lat},{lng})')
        return (fix, lat, lng)
    return ()


def get_coords():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
    while True:
        try:
            line = ser.readline().decode("ascii")
            # print(line)
            (fix, lat, lng) = parse(line)
            if fix:
                return (lat, lng)
            """msg = pynmea2.parse(line)
            if isinstance(msg, pynmea2.types.talker.RMC):
                if msg.status == 'V':
                    print('no fix')
                    continue
                else:
                    coords = (msg.longitude, msg.latitude)
                    return coords"""
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
        except:
            print('[navigation] unknown error')
            continue
    return ()  # (181, 91)


def fix():
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
    print('[navigation] searching for fix...')
    while True:
        try:
            (fix, lat, lng) = parse(ser.readline())
            if fix:
                print('[navigation] got a fix')
                return
            """msg = pynmea2.parse(ser.readline().decode("ascii"))
            if isinstance(msg, pynmea2.types.talker.GGA):
                if msg.gps_qual != 0:
                    # print(f'got a fix of type {msg.gps_qual}, {msg.num_sats} satellites')
                    return"""
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
