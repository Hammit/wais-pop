#!/usr/bin/env python2

import os, re
import sys, time
import datetime
import logging
import signal
import argparse
from Nonin import *

POLLING_INTERVAL = 105

# When we receive a HUP signal, make sure we exit (cleanly)
def sighup_handler(signame, frame):
    # TODO: Add logging
	sys.exit()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("address", help="the MAC address of the connecting device")
    parser.add_argument("name", help="the name of the device connecting")
    parser.add_argument("service_name", help="the service name. e.g. Serial Port")
    parser.add_argument("uuid", help="UUID, which can be a comma separated list. e.g. 0x1011")
    parser.add_argument("device", help="the device node. e.g. /dev/rfcomm0")
    args = parser.parse_args()
    return args


def log_filename(filename=None):
    if filename is None:
        dt = datetime.datetime.now()
        dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
        filename = 'bluetooth-connected.%s.log' % dt_str
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, '..', '..', 'tmp', filename)
    return path


# TODO: Remove all but the PIN from the device name
def csv_filename(device_name=None):
    if device_name is None:
        device_name = 'UNKNOWN_DEVICE'

    # re.sub(r'\D', '', device_name)

    dt = datetime.datetime.now()
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
    filename = 'wristox-session.%s.%s.log' % (device_name, dt_str)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, '..', '..', 'tmp', filename)
    return full_path


if __name__ == "__main__":
    args = parse_args()

    # Verify the MAC address belongs to Nonin Medical Inc.
    match = re.search('^00:1C:05', args.address, re.IGNORECASE)
    if match is None:
        print 'Not a Nonin device!'
        sys.exit(1)

    # Setup Logging
    logfile = log_filename()
    print 'Log filename: {}'.format(logfile)
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(levelname)s: %(asctime)s %(message)s')

    # Signal Handling
    signal.signal(signal.SIGHUP, sighup_handler)

    # Main Loop
    finished = False
    while not finished:
        try:
            nonin = Nonin3150(args.device)
            logging.info('Connected to %s' % args.device)

            # NOTE: Do we need to configure anything here?
            config = nonin.get_config()
            config['BluetoothEnable'] = '1'
            config['ActivationOption'] = '1'
            config['StorageRate'] = '1'
            nonin.set_config(config)
            logging.info('Configured the device')

            # nonin.enable_logging() # already done above (ActivationOption)
            nonin.set_bluetooth_timeout(0)
            nonin.set_current_time()
            logging.info('Set Bluetooth Timeout and Date/Time')

            # It's important to clear before the main loop to prevent reads of
            # previous sessions, which may be quite large and cause read failures
            logging.info('Clearing session data...')
            nonin.clear_sessions()

            # Collect data forever, or until a SIGHUP is received
            while True:
                try:
                    logging.info('Reading session data...')
                    sessions = nonin.read_sessions()

                    if sessions is not None:
                        filename = csv_filename(device_name=args.name)
                        exporter = Exporter(sessions)
                        exporter.export(format='csv', filename=filename)
                        logging.info('Saved data to %s' % filename)

                        logging.info('Clearing session data...')
                        nonin.clear_sessions()

                        logging.info('Sleeping (gathering data) for %d seconds' % POLLING_INTERVAL)
                        time.sleep(POLLING_INTERVAL)

                except Exception as e:
                    logging.error('Exception raised: %s' % e)
                    time.sleep(1)

        except Exception as e:
            logging.error('Exception raised: %s' % e)
            time.sleep(1)

