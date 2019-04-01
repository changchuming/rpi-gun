import RPi.GPIO as gpio
import smbus
import time
import sys
bus = smbus.SMBus(1)
address = 0x04
def main():
    gpio.setmode(gpio.BCM)
    status = False
    while 1:
        status = not status
        bus.write_byte(address, 1 if status else 5)
        print("Arduino answer to RPI: {}".format(bus.read_byte(address)))
        time.sleep(1)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        gpio.cleanup()
        sys.exit(0)