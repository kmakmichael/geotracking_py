import serial
from struct import pack, unpack
import pynmea2
import re

mp = re.compile(r"(\d):([-\d]+\.\d+),([-\d]+\.\d+)")

def parse(msg):
    d = mp.search(msg)
    return (int(d[1]), float(d[2]), float(d[3]))


def get_coords():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
    while True:
        try:
            line = ser.readline().decode("ascii")
            (fix, lat, lng) = parse(line)
            if fix:
                return (lat, lng)
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
    return ()  # (181, 91)


def fix():
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
    print('[navigation] searching for fix...')
    while True:
        try:
            (fix, lat, lng) = parse(ser.readline().decode('ascii'))
            if fix:
                print('[navigation] got a fix')
                return
        except serial.SerialException as e:
            print(f'[navigation] Device error: {e}')
            break
