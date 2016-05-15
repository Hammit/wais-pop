# Note:  if you are missing the "serial" package, you'll want to install pySerial
# On a mac, we've had luck installing by typing
# easy_install pySerial
# from the commandline


# Interface to Nonin 3150
#
# Using references from Nonin:
#    "3150-Specifications_7970_000-Rev-A.pdf"
#    "3150 Commands.docx" (includes format of memory playback)

from collections import OrderedDict
import datetime
import glob
from dateutil import tz
import serial
import struct
import csv

class Nonin3150:
    """Interface to Nonin WristOx2 3150"""
    
    fields = OrderedDict([
        ('Reserved1',                    'c'), # Length 1.  
        ('BluetoothEnable',              'c'), # ASCII len 1. enabled:'1', disabled:'2'
        ('ActivationOption',             'c'), # ASCII len 1.  always log:'1', use start/stop time:'2', display only:'3'
        ('StorageRate',                  'c'), # ASCII len 1.  every second:'1', 2 seconds: '2', 4 seconds: '4'
        ('DisplayOption',                'c'), # ASCII len 1.  full display while logging:'1', partial display:'2'
        ('StartTime1',                 '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('StopTime1',                  '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('StartTime2',                 '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('StopTime2',                  '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('StartTime3',                 '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('StopTime3',                  '10s'), # ASCII YYMMDDhhmm.  Only used for ActivationOption '2'
        ('ProgrammableIdentification', '50s'), # ASCII len 50.  Arbitrary ID settable by user
        ('SoftwarePartNumber',          '4s'), # ASCII len 50.  First 4 digits
        ('SoftwareRevision',            '3s'), # ASCII len 3
        ('SoftwareRevDate',             '6s'), # ASCII YYMMDD
        ('Reserved2',                   '6s'), # Length 6
    ])

    format = ''.join(fields.values())
    
    date_format = '%Y-%m-%d %H:%M:%S %Z'
    
    def __init__(self, device_path):
        #candidates = glob.glob('/dev/cu.usbmodem*')
        #if len(candidates) == 0:
        #    raise Exception("Can't find Nonin device.  Please be sure it's plugged in using the USB cable.")
        #if len(candidates) > 1:
        #    raise Exception("Hmm, found multiple USB serial ports.  Need to address this issue in the software.")
        #self.device_path = candidates[0]
        self.device_path = device_path
        print 'Opening %s...' % self.device_path
        self.device = serial.Serial(self.device_path, timeout=4)
        print 'Opened %s' % self.device_path
        config = self.get_config()
        print ('Found Nonin 3150 at %s, software %s.%s.20%s' % 
               (self.device_path, config['SoftwarePartNumber'], 
                config['SoftwareRevision'], config['SoftwareRevDate']))
        time = self.get_current_time()
        print 'Current time as reported by device in GMT: %s' % time.strftime(self.date_format)
        localtime = time.astimezone(tz.tzlocal())
        print '  (Converted to your current local timezone: %s)' % localtime.strftime(self.date_format)

    @staticmethod
    def get_device():
        devices = glob.glob('/dev/rfcomm*')
        if len(devices) == 0:
            raise Exception('No rfcomm device(s) found')
        else:
            devices.sort()
            return devices[-1]
    
    def get_config(self):
        self.device.flushInput()
        self.device.write('CFG?\r\n')
        self.require_ack()
        data = self.require_bytes(134)
        checksum = struct.unpack('>H', self.require_bytes(2))[0]
        if checksum != sum([ord(ch) for ch in data]):
            raise Exception('CFG? incorrect checksum')
        unpacked = struct.unpack(self.format, data)
        return OrderedDict(zip(self.fields.keys(), unpacked))
    
    def set_config(self, config):
        if config.keys() != self.fields.keys():
            raise Exception('config must be an OrderedDict with keys as returned from get_config')
        data = struct.pack(self.format, *config.values())
        checksum = struct.pack('>H', sum([ord(ch) for ch in data]))
        self.device.flushInput()
        self.device.write('CFG=' + data + checksum + '\r\n')
        self.require_ack()
        self.require_crlf()
        
    def enable_logging(self, interval=1):
        config = self.get_config()
        
        # Always log when sensor detects signal
        config['ActivationOption'] = '1'
        
        interval = int(interval)
        valid_intervals = [1,2,4]
        if not interval in valid_intervals:
            raise Exception('interval must be one of %s' % valid_intervals)
        config['StorageRate'] = str(interval)
        
        self.set_config(config)
    
    # By convention, this library always stores time on the 3150 in UTC, since the 3150
    # supports neither daylight savings time nor timezones.
    
    def get_current_time(self):
        self.device.flushInput()
        self.device.write('DTM?\r\n')
        self.require_ack();
        time = self.require_bytes(12)
        self.require_crlf();
        return datetime.datetime.strptime(time, '%y%m%d%H%M%S').replace(tzinfo=tz.tzutc())
    
    def set_current_time(self):
        self.device.flushInput()
        # Write time in UTC, format YYMMDDhhmmss
        self.device.write(datetime.datetime.utcnow().strftime('DTM=%y%m%d%H%M%S\r\n'))
        self.require_ack()
        self.require_crlf()

    def set_bluetooth_timeout(self, period=3):
        self.device.flushInput()
        self.device.write('SBT=%03d\r\n' % period)
        self.require_ack()
    
    def get_header(self):
        self.device.flushInput()
        self.device.write('HDR?\r\n')
        self.require_ack()
        return self.read_until_timeout()
    
    def clear_sessions(self):
        self.device.flushInput()
        self.device.write(datetime.datetime.utcnow().strftime('MCL!\r\n'))
        self.require_ack()
        self.require_crlf()
        
    def read_sessions(self):
        self.device.flushInput()
        self.device.write('MPB?\r\n')
        self.require_ack()
        print 'Reading memory from Nonin...'
        memory = self.read_until_timeout()
        print 'Read %d bytes' % len(memory)
        if len(memory) % 3 != 0:
            raise Exception('MPB?: Invalid memory length read')
    
        # Check and strip checksums
        data = []
        for i in range(0, len(memory) / 3):
            bytes = [ord(ch) for ch in memory[i * 3 : (i + 1) * 3]]
            if (bytes[0] + bytes[1]) % 256 != bytes[2]:
                raise Exception('MPB?: invalid checksum in triplet %d' % i)
            data.append((bytes[0], bytes[1]))

        # Decode sessions
        header = (254, 253)
        i = 0
        sessions = []
        while i < len(data):
            if data[i] != header:
                raise Exception('MPB?: invalid header at triplet %d' % i)
            print 'Session header starting at triplet %d' % i
            i += 1
    
            (seconds_per_sample, format) = data[i]
            if format != 2:
                raise Exception('MPB?: unknown format at triplet %d' % i)
            i += 1
            print '  Seconds per sample: %d' % seconds_per_sample
    
            current_time = self.decode_memory_time(data, i); i += 3
        
            # Don't read start and stop time unless we confirm there are samples
            # The Nonin tends to have an empty session, with invalid start and stop time
            stop_time_index = i; i += 3;
            start_time_index = i; i += 3;
    
            session = []
            valid = False
            while i < len(data) and data[i] != header:
                if len(session) == 0:
                    # We have a non-empty session.  Go ahead and parse the times
                    # Samples are reversed in time
                    sample_time = stop_time = self.decode_memory_time(data, stop_time_index);
                    start_time = self.decode_memory_time(data, start_time_index);
    
                    if start_time and stop_time:
                        print '  Time range: %s to %s' % (start_time.strftime(self.date_format),
                                                          stop_time.strftime(self.date_format))
                        valid = True
                    else:
                        print '  Invalid start or stop time'

                (pulse_rate, spo2) = data[i]; i += 1
                if pulse_rate == 255:
                    pulse_rate = None
                elif pulse_rate > 200:
                    # Values over 200 are compressed to handle high pulse rates
                    pulse_rate = 200 + (pulse_rate - 200) * 2
                if spo2 == 255:
                    spo2 = None
                session.append((sample_time, pulse_rate, spo2))
                if sample_time:
                    sample_time -= datetime.timedelta(seconds=1)
            session.reverse()
                    
            print '  %s data samples' % len(session)
            if valid and len(session) > 0:
                sessions.append(session)
        
        print 'Total of %d valid sessions' % len(sessions)
        return sessions

    @staticmethod
    def decode_memory_time(memory, i):
        [(month, day), (year, minute), (second, hour)] = memory[i : i + 3]
        try:
            return datetime.datetime(year + 2000, month, day, hour, minute, second, tzinfo=tz.tzutc())
        except:
            print "Couldn't make a time from YY=%d MM=%d DD=%d HH:MM:SS=%d:%d:%d" % (year, month, day, hour, minute, second)
            return None

    def read_until_timeout(self):
        ret = ''
        while True:
            read = self.device.read(1000)
            if read == '':
                return ret
            ret += read
            
    def require_bytes(self, n):
        ret = ''
        while len(ret) < n:
            read = self.device.read(n - len(ret))
            ret += read
            if read == '':
                raise Exception('Expected %d bytes but only received %d' % (n, len(ret)))
        return ret
    
    def require_ack(self):
        byte = self.device.read(1)
        if byte != '\x06':
            raise Exception('Expected ACK not received')
    
    def require_crlf(self):
        if self.device.read(2) != '\r\n':
            raise Exception('Expected CRLF not received')


class Exporter():
    """
    Export facilities for saving session data on the device to various file-
    formats.
    """

    def __init__(self, sessions):
        self.sessions = sessions

    def export(self, format='csv', filename=None):
        if format == 'csv':
            self._export_as_csv(filename)

    def _export_as_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            for session in self.sessions:
                for sample in session:
                    csvwriter.writerow(sample)

