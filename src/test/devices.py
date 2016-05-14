#!/usr/bin/env python2

import glob


def get_device():
    devices = glob.glob('/dev/rfcomm*')
    if len(devices) == 0:
        raise Exception('No rfcomm device(s) found')
    else:
        devices.sort()
        return devices[-1]


if __name__ == "__main__":
    device = get_device()
    print device
