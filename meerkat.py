########################################################################################################################
#                                            Imports Required                                                          #
########################################################################################################################
import paho.mqtt.client as mqtt
import serial
import datetime as dt
import time
import sys
import glob
import matplotlib.dates as mdates
from enum import Enum, auto
import json
import requests
import logging


########################################################################################################################
#                                            Global Variables                                                          #
########################################################################################################################
# Set DEBUG to True to allow for verbose printing to the terminal
DEBUG = False


########################################################################################################################
#                                            Class Definitions                                                         #
########################################################################################################################
class Response(Enum):
    """
    Response codes to be returned to the main application. The value of the response is irrelevant so values
    are assigned using the auto() function.
    """
    LOGIN = auto()
    SETUP = auto()
    IP_ADDRESS = auto()
    WIFI_DISCONNECTED = auto()
    WIFI_CONNECTED = auto()
    WIFI_ERROR = auto()
    SAFARI_ERROR = auto()
    SAFARI_SERIAL_STREAMING = auto()
    SAFARI_CLOUD_STREAMING = auto()
    SAFARI_DATA_RECEIVED = auto()
    SAFARI_FAULT_DETECTED = auto()
    SAFARI_FAULT_CLEARED = auto()
    ACN_MQTT_CONNECTED = auto()
    ACN_MQTT_DISCONNECTED = auto()
    ACN_MQTT_MSG_RECEIVED = auto()


class Safari:
    def __init__(self):
        # Maximum number of data points to store for each channel's data arrays.
        self.max_elements = 300
        self.ch0_timestamps = []
        self.ch1_timestamps = []
        self.ch2_timestamps = []
        self.ch3_timestamps = []
        self.ch4_timestamps = []
        self.ch5_timestamps = []
        self.ch6_timestamps = []
        self.ch7_timestamps = []
        self.ch8_timestamps = []
        self.ch9_timestamps = []
        self.ch10_timestamps = []
        self.ch11_timestamps = []
        self.ch12_timestamps = []
        self.ch13_timestamps = []
        self.ch14_timestamps = []
        self.ch15_timestamps = []
        self.ch0_voltages = []
        self.ch1_voltages = []
        self.ch2_voltages = []
        self.ch3_voltages = []
        self.ch4_voltages = []
        self.ch5_voltages = []
        self.ch6_voltages = []
        self.ch7_voltages = []
        self.ch8_voltages = []
        self.ch9_voltages = []
        self.ch10_voltages = []
        self.ch11_voltages = []
        self.ch12_voltages = []
        self.ch13_voltages = []
        self.ch14_voltages = []
        self.ch15_voltages = []
        self.ch0_values = []
        self.ch1_values = []
        self.ch2_values = []
        self.ch3_values = []
        self.ch4_values = []
        self.ch5_values = []
        self.ch6_values = []
        self.ch7_values = []
        self.ch8_values = []
        self.ch9_values = []
        self.ch10_values = []
        self.ch11_values = []
        self.ch12_values = []
        self.ch13_values = []
        self.ch14_values = []
        self.ch15_values = []
        self.running = False
        self.test_mode_enabled = False
        self.motor_running = False

    def reset(self):
        """ Reset all the lists.

        :return: Nothing
        """
        self.__init__()


class Meerkat:
    def __init__(self):
        self.BAUD = 115200  # Serial Baud Rate
        self.cloud_connected = False
        self.safari = Safari()
        self.acn = Acn(self)
        self.serial = None
        self.serial_buffer = ""
        self.mac_address = "00:00:00:00:00:00"
        self.ip_address = "0.0.0.0"

    def serial_connect(self, port):
        """ The function initiates the Connection to the UART device with the specified Port.
        The radio button selects the platform, as the serial object has different key phrases
        for Linux and Windows. Some Exceptions have been made to prevent the app from crashing,
        such as blank entry fields and value errors, this is due to the state-less-ness of the
        UART device, the device sends data at regular intervals irrespective of the master's state.
        The other Parts are self explanatory.

        :param port: Serial port to connect to.
        :returns:
            0 if the serial connection is successfully opened.
            -1 if the connection fails to open.
        """

        if DEBUG:
            print("Attempting to open port {}".format(port))

        try:
            self.serial = serial.Serial(port, self.BAUD,
                                        timeout=0, writeTimeout=0)  # ensure non-blocking
            return 0
        except Exception as e:
            logging.exception(e)
            print("Cant Open Specified Port")
            return -1

    def serial_disconnect(self):
        """ This function is for disconnecting and quitting the application.
            Sometimes the application throws a couple of errors while it is being shut down, the fix isn't out yet
            but will be pushed to the repo once done.
            simple GUI.quit() calls.

        :returns:
            0 if the serial connection is successfully closed.
            -1 if the connection fails to close.
        """
        try:
            self.serial.close()
            return 0

        except AttributeError:
            print("Closed without Using it -_-")
            return -1

    def serial_port_open(self):
        """ Check if the serial port is open.

        :returns:
            True if the serial port is open.
            False if the serial port is closed.
        """

        if self.serial:
            if self.serial.isOpen():
                return True

        return False

    def serial_port_scan(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                self.serial = serial.Serial(port)
                self.serial.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result

    def serial_ctrl_c(self):
        """ Send a ctrl+c command to the terminal

        :return: Nothing
        """
        if self.serial_port_open():
            self.serial.write("\x03\n".encode('utf-8'))

    def serial_parse(self, serial_string):
        """ Parses the strings received from the serial port

        :param serial_string: String received from the serial port
        :return: A unique response based on the string received from the serial port
        """
        if "login" in serial_string:
            return Response.LOGIN
        elif "-sh: root: not found" in serial_string:
            return Response.SETUP
        elif "inet addr" in serial_string:
            strings = serial_string.lstrip().split("  ")
            strings = strings[0].split(":")
            self.ip_address = (strings[1])
            return Response.IP_ADDRESS
        elif "ESSID" in serial_string:
            if "off/any" in serial_string:
                return Response.WIFI_DISCONNECTED
            else:
                return Response.WIFI_CONNECTED
        elif "Access Point: Not-Associated" in serial_string:
            return Response.WIFI_DISCONNECTED
        elif "DFS Master region: unset" in serial_string:
            return Response.WIFI_DISCONNECTED
        elif "No lease, failing" in serial_string:
            return Response.WIFI_ERROR
        elif "AD7124 error" in serial_string:
            return Response.SAFARI_ERROR
        elif "Serial Data Streaming Enabled" in serial_string:
            self.cloud_connected = False
            return Response.SAFARI_SERIAL_STREAMING
        elif "Cloud Data Streaming Enabled" in serial_string:
            self.cloud_connected = True
            return Response.SAFARI_CLOUD_STREAMING
        elif "channel" in serial_string \
                and "timestamp" in serial_string \
                and "voltage" in serial_string \
                and "code" in serial_string:
            return Response.SAFARI_DATA_RECEIVED
        elif "FAULT DETECTED!" in serial_string:
            return Response.SAFARI_FAULT_DETECTED

    def login(self):
        """ Login to the device

        :return: Nothing
        """
        if self.serial_port_open():
            if DEBUG:
                print("Logging in as root...")
            self.serial.write("root\n".encode('utf-8'))

    def setup(self):
        """ Setup the device

        :return: Nothing
        """
        self.set_time_utc()
        self.get_mac()
        self.get_device_name()
        self.get_device_uid()

    def set_time_utc(self):
        """ Set the UTC time of the device to match the UTC time of the host

        The response will be parsed by the serial_parse function.

        :return: Nothing
        """
        if DEBUG:
            print("MEERKAT - Setting UTC Time")
        self.serial.write(
            'date -s "{}"\n'.format(dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")).encode('utf-8'))

        time.sleep(1)

    def wifi_check(self):
        """ Check the Wi-Fi connection of the device.

        The response will be parsed by the serial_parse function.

        :return: Nothing
        """

        self.serial.write(
            'iwconfig\n'.encode('utf-8'))

        time.sleep(1)

        self.serial.write(
            'ifconfig wlan0\n'.encode('utf-8'))

        time.sleep(1)

    def wifi_connect(self, ssid, password):
        """ Connect to the Wi-Fi network matching the specified ssid and password

        Set both the ssid and password fields to "" (empty strings) to clear any previous Wi-Fi network information
        or to disconnect from any current networks.

        :param ssid: SSID of the desired Wi-Fi network.
        :param password: Password of the desired Wi-Fi network
        :return: Nothing
        """

        if ssid == "" or password == "":
            self.serial.write(
                'ifdown wlan0\n'.encode('utf-8'))
            time.sleep(2)
            self.serial.write(
                'rm /etc/wpa_supplicant.conf\n'.encode('utf-8'))
            time.sleep(2)
            self.serial.write(
                'ifup wlan0\n'.encode('utf-8'))
            time.sleep(2)

            self.wifi_check()
        else:
            self.serial.write(
                'ifdown wlan0\n'.encode('utf-8'))
            time.sleep(2)
            self.serial.write(
                'rm /etc/wpa_supplicant.conf\n'.encode('utf-8'))
            time.sleep(2)
            self.serial.write(
                'wpa_passphrase "{}" {} | tee /etc/wpa_supplicant.conf\n'.format(ssid, password).encode(
                    'utf-8'))
            time.sleep(2)
            self.serial.write(
                'ifup wlan0\n'.encode('utf-8'))
            time.sleep(2)

            self.wifi_check()

    def get_mac(self):
        """ Get the MAC address of the device

        :return: Nothing
        """
        if DEBUG:
            print("MEERKAT - Getting MAC Address")
        self.serial.write(
            '\ncat /sys/class/net/wlan0/address\n'.encode('utf-8'))

        # Wait for the MAC address to be displayed
        mac_address = self.serial.readline().decode('unicode_escape')
        while mac_address.count(':') != 5:
            mac_address = self.serial.readline().decode('unicode_escape')
            if "No such file or directory" in mac_address:
                self.mac_address = "00:00:00:00:00:00"
                return

        self.mac_address = mac_address.rstrip()
        if DEBUG:
            print("MEERKAT - MAC Address: {}".format(self.mac_address))

    def reboot(self):
        """ Reboot the device

        :return: Nothing
        """
        self.serial.write("reboot\n".encode('utf-8'))

    def safari_start(self):
        """ Start the Safari script on the device.

        :return: Nothing
        """
        self.safari.running = True
        self.serial.write("python /root/python/safari.py\n".encode('utf-8'))

    def safari_stop(self):
        """ Stop the Safari script, or any running script, on the device

        :return: Nothing
        """
        self.safari.running = False
        self.safari.test_mode_enabled = False
        self.serial_ctrl_c()

    def safari_test(self):
        """ Start the Safari test script on the device.

        :return: Nothing
        """
        self.safari.test_mode_enabled = True
        self.serial.write("python /root/python/safari_test.py\n".encode('utf-8'))

    def safari_sim_start(self):
        """ Start the Safari simulation script on the device.

        :return: Nothing
        """
        self.safari.running = True
        self.serial.write("python /root/python/safari_sim.py\n".encode('utf-8'))

    def safari_sim_local_start(self):
        """ Start the Safari local simulation script on the device.

        :return: Nothing
        """
        self.safari.running = True
        self.serial.write("python /root/python/safari_sim_local.py\n".encode('utf-8'))

    def safari_sim_cloud_start(self):
        """ Start the Safari cloud simulation script on the device.

        :return: Nothing
        """
        self.safari.running = True
        self.serial.write("python /root/python/safari_sim_cloud.py\n".encode('utf-8'))

    def get_device_name(self):
        """ Build the DEVICE_NAME off the SAFARI_DEVICE_KEYWORD and Mac address

        :return: Nothing
        """
        if DEBUG:
            print("MEERKAT - Getting Device Name")
        self.acn.DEVICE_NAME = self.acn.SAFARI_DEVICE_KEYWORD + " " + self.mac_address
        if DEBUG:
            print("MEERKAT - Device Name: {}".format(self.acn.DEVICE_NAME))

    def get_device_uid(self):
        """ Build the DEVICE_UID based off the DEVICE_UID_PREFIX and MAC address

        :return: Nothing
        """
        if DEBUG:
            print("MEERKAT - Getting Device UID")
        self.acn.DEVICE_UID = self.acn.DEVICE_UID_PREFIX + self.mac_address[0:17].replace(":", "")
        if DEBUG:
            print("MEERKAT - Device UID: {}".format(self.acn.DEVICE_UID))

    def mqtt_parse_message(self, message):
        """ Parse MQTT message

        :param message: message to parse
        :return rc: Response Code
        """

        if DEBUG:
            print("Parsing received MQTT message")
            print(message)
            for key in message:
                print('"Key": {}, "Value": {}'.format(key, message[key]))

        rc = Response.SAFARI_DATA_RECEIVED

        for key in message:
            if key == "b|fault":
                if message[key]:
                    rc = Response.SAFARI_FAULT_DETECTED
                else:
                    rc = Response.SAFARI_FAULT_CLEARED
            if key == "f|channel_0_voltage":
                self.safari.ch0_voltages.append(round(float(message[key]), 4))
                self.safari.ch0_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch0_values.append(round(float(message[key]), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch0_timestamps = self.safari.ch0_timestamps[-self.safari.max_elements:]
                self.safari.ch0_voltages = self.safari.ch0_voltages[-self.safari.max_elements:]
                self.safari.ch0_values = self.safari.ch0_values[-self.safari.max_elements:]

            if key == "f|channel_1_voltage":
                self.safari.ch1_voltages.append(round(float(message[key]), 4))
                self.safari.ch1_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch1_values.append(round(float(message[key]), 2) * 3)
                # ch1_timestamps.append(mdates.date2num(dt.datetime.now()))

                # Limit lists to the max elements value
                self.safari.ch1_timestamps = self.safari.ch1_timestamps[-self.safari.max_elements:]
                self.safari.ch1_voltages = self.safari.ch1_voltages[-self.safari.max_elements:]
                self.safari.ch1_values = self.safari.ch1_values[-self.safari.max_elements:]

            if key == "f|channel_2_voltage":
                self.safari.ch2_voltages.append(round(float(message[key]), 4))
                self.safari.ch2_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch2_values.append(round(float(message[key]), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch2_timestamps = self.safari.ch2_timestamps[-self.safari.max_elements:]
                self.safari.ch2_voltages = self.safari.ch2_voltages[-self.safari.max_elements:]
                self.safari.ch2_values = self.safari.ch2_values[-self.safari.max_elements:]

            if key == "f|channel_3_voltage":
                self.safari.ch3_voltages.append(round(float(message[key]), 4))
                self.safari.ch3_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch3_values.append(round(float(message[key]), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch3_timestamps = self.safari.ch3_timestamps[-self.safari.max_elements:]
                self.safari.ch3_voltages = self.safari.ch3_voltages[-self.safari.max_elements:]
                self.safari.ch3_values = self.safari.ch3_values[-self.safari.max_elements:]

            if key == "f|channel_4_voltage":
                self.safari.ch4_voltages.append(round(float(message[key]) * 1000, 4))
                self.safari.ch4_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch4_values.append(self.convert_temperature(message["i|code"]))

                # Limit lists to the max elements value
                self.safari.ch4_timestamps = self.safari.ch4_timestamps[-self.safari.max_elements:]
                self.safari.ch4_voltages = self.safari.ch4_voltages[-self.safari.max_elements:]
                self.safari.ch4_values = self.safari.ch4_values[-self.safari.max_elements:]

            if key == "f|channel_5_voltage":
                self.safari.ch5_voltages.append(round(float(message[key]), 4))
                self.safari.ch5_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch5_values.append(round(float(message[key]), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch5_timestamps = self.safari.ch5_timestamps[-self.safari.max_elements:]
                self.safari.ch5_voltages = self.safari.ch5_voltages[-self.safari.max_elements:]
                self.safari.ch5_values = self.safari.ch5_values[-self.safari.max_elements:]

            if key == "f|channel_6_voltage":
                self.safari.ch6_voltages.append(round(float(message[key]), 4))
                self.safari.ch6_timestamps.append(
                    mdates.date2num(dt.datetime.fromtimestamp(int(message["i|timestamp"]) / 1000000.0)))
                self.safari.ch6_values.append(self.convert_pressure(float(message[key])))

                # Limit lists to the max elements value
                self.safari.ch6_timestamps = self.safari.ch6_timestamps[-self.safari.max_elements:]
                self.safari.ch6_voltages = self.safari.ch6_voltages[-self.safari.max_elements:]
                self.safari.ch6_values = self.safari.ch6_values[-self.safari.max_elements:]

        return rc

    def update_plot_data(self, data_string):
        """ Parse the data_string into key values and store the data into arrays

        :param data_string: String to parse into relevant data
        :return: Nothing
        """

        data_string = data_string.replace("channel,", '')
        data_string = data_string.replace("timestamp,", '')
        data_string = data_string.replace("voltage,", '')
        data_string = data_string.replace("code,", '')

        try:
            channel, timestamp, voltage, code = data_string.split(",")

            # Add data to lists
            if channel == "0":
                self.safari.ch0_voltages.append(round(float(voltage), 4))
                self.safari.ch0_values.append(self.convert_accelerometer(float(voltage)))

                # Limit lists to the max elements value
                self.safari.ch0_timestamps = self.safari.ch0_timestamps[-self.safari.max_elements:]
                self.safari.ch0_voltages = self.safari.ch0_voltages[-self.safari.max_elements:]
                self.safari.ch0_values = self.safari.ch0_values[-self.safari.max_elements:]

            elif channel == "1":
                self.safari.ch1_voltages.append(round(float(voltage), 4))
                self.safari.ch1_values.append(round(float(voltage), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch1_timestamps = self.safari.ch1_timestamps[-self.safari.max_elements:]
                self.safari.ch1_voltages = self.safari.ch1_voltages[-self.safari.max_elements:]
                self.safari.ch1_values = self.safari.ch1_values[-self.safari.max_elements:]

            elif channel == "2":
                self.safari.ch2_voltages.append(round(float(voltage), 4))
                self.safari.ch2_values.append(self.convert_accelerometer(float(voltage)))

                # Limit lists to the max elements value
                self.safari.ch2_timestamps = self.safari.ch2_timestamps[-self.safari.max_elements:]
                self.safari.ch2_voltages = self.safari.ch2_voltages[-self.safari.max_elements:]
                self.safari.ch2_values = self.safari.ch2_values[-self.safari.max_elements:]

            elif channel == "3":
                self.safari.ch3_voltages.append(round(float(voltage), 4))
                self.safari.ch3_values.append(round(float(voltage), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch3_timestamps = self.safari.ch3_timestamps[-self.safari.max_elements:]
                self.safari.ch3_voltages = self.safari.ch3_voltages[-self.safari.max_elements:]
                self.safari.ch3_values = self.safari.ch3_values[-self.safari.max_elements:]

            elif channel == "4":
                self.safari.ch4_voltages.append(round(float(voltage) * 1000, 4))
                self.safari.ch4_values.append(self.convert_temperature(float(code)))

                # Limit lists to the max elements value
                self.safari.ch4_timestamps = self.safari.ch4_timestamps[-self.safari.max_elements:]
                self.safari.ch4_voltages = self.safari.ch4_voltages[-self.safari.max_elements:]
                self.safari.ch4_values = self.safari.ch4_values[-self.safari.max_elements:]

            elif channel == "5":
                self.safari.ch5_voltages.append(round(float(voltage), 4))
                self.safari.ch5_values.append(round(float(voltage), 2) * 3)

                # Limit lists to the max elements value
                self.safari.ch5_timestamps = self.safari.ch5_timestamps[-self.safari.max_elements:]
                self.safari.ch5_voltages = self.safari.ch5_voltages[-self.safari.max_elements:]
                self.safari.ch5_values = self.safari.ch5_values[-self.safari.max_elements:]

            elif channel == "6":
                self.safari.ch6_voltages.append(round(float(voltage), 4))
                self.safari.ch6_values.append(self.convert_pressure(float(voltage)))

                # Limit lists to the max elements value
                self.safari.ch6_timestamps = self.safari.ch6_timestamps[-self.safari.max_elements:]
                self.safari.ch6_voltages = self.safari.ch6_voltages[-self.safari.max_elements:]
                self.safari.ch6_values = self.safari.ch6_values[-self.safari.max_elements:]

        except Exception as e:
            logging.exception(e)
            pass

    def motor_start(self):
        """ Start the motor

        :return: Nothing

        Toggles a GPIO pin to signal the motor to start
        """
        self.safari.motor_running = True
        self.serial.write("echo 100 > /sys/class/gpio/export\n".encode('utf-8'))
        self.serial.write("echo out > /sys/class/gpio/gpio100/direction\n".encode('utf-8'))
        self.serial.write("echo 1 > /sys/class/gpio/gpio100/value\n".encode('utf-8'))

    def motor_stop(self):
        """ Stop the motor

        :return: Nothing

        Toggles a GPIO pin to signal the motor to stop
        """
        self.safari.motor_running = False
        self.serial.write("echo 100 > /sys/class/gpio/export\n".encode('utf-8'))
        self.serial.write("echo out > /sys/class/gpio/gpio100/direction\n".encode('utf-8'))
        self.serial.write("echo 0 > /sys/class/gpio/gpio100/value\n".encode('utf-8'))

    @staticmethod
    def convert_pressure(voltage):
        """ Convert the supplied voltage to Pascals

        :param voltage: Voltage to convert
        :return: Pressure measured in Pascals (Pa)


        DP = (190 * Vmeas)/Vdd - 38Pa
        Example:
        Vmeas = 875mV, Vdd = 3.3V
        Differential Pressure = (190 * 0.875V)/3.3V - 38Pa = 12.37Pa
        """
        vcc = 3.3
        r1 = 132000
        r2 = 100000
        return round(((190.0 * voltage * (r1/r2)) / vcc - 38), 3)

    @staticmethod
    def convert_accelerometer(voltage):
        """ Convert the supplied voltage to g's

        :param voltage: Voltage to convert
        :return: Acceleration measured in g's


        Acceleration (g's) = (Vmeas-VCC/2) * 1g/620mV
        Example:
        Vmeas = 2.05V, Vcc = 3.3V
        Acceleration = (2.05V-1.65V) * 1g/0.620V = 0.645g
        """
        vcc = 3.3
        return round((voltage - vcc / 2) * 1 / 0.640, 3)

    @staticmethod
    def convert_temperature(code):
        """ Convert the supplied code to temperature

        :param code: Raw ADC value received from AD7124
        :return: Temperature in degrees Celsius.


        RTD Resistance = (Code * 5.11kOhms) / ((2^24) * 16)
        Temperature (Degrees C) = (RTD Resistance - 100ohms) / (0.385 ohms/degC)
        """
        r_rtd = (code * 5110) / ((2**24) * 16)
        temp = (r_rtd - 100) / 0.385
        return round(temp, 2)


class Acn:
    def __init__(self, parent):
        self.parent = parent
        self.SAFARI_DEVICE_KEYWORD = "Safari Device"
        self.APPLICATION_OWNER_RAW_API_KEY = "46ec0138c872454e50601abec5d72a105e4d312d4f28f1fd25a63e4ef22ccd40"
        self.GATEWAY_HID = ""
        self.DEVICE_HID = ""
        self.DEVICE_UID_PREFIX = "safari-dev-"
        self.DEVICE_UID = "safari-dev-000000000000"
        self.DEVICE_NAME = "Safari Device 00:00:00:00:00:00"
        self.SAFARI_DEVICE_KEYWORD = "Safari Device"
        mqtt.Client.connected_flag = False  # create flag in class
        self.mqtt_client = mqtt.Client("Safari")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.MQTT_USERNAME = "/pegasus:{}".format(self.GATEWAY_HID)
        self.MQTT_HOST = "mqtt-a01.arrowconnect.io"
        self.MQTT_PORT = 1883
        self.MQTT_SUBSCRIBE_TOPIC = "krs/cmd/stg/{}".format(self.GATEWAY_HID)
        self.MQTT_PUBLISH_TOPIC = "krs/tel/gts/{}".format(self.GATEWAY_HID)
        self.MQTT_TIMEOUT = 60
        self.callback = None

    def on_message(self, client, obj, mqtt_msg):
        """ Callback for when a PUBLISH message is received from the server.

        :param client: Ignored
        :param obj: Ignored
        :param mqtt_msg: Received Message
        :return: Nothing
        """
        # Ignored Parameters
        del client
        del obj

        if DEBUG:
            print("MQTT Message Received!")

        message = json.loads(mqtt_msg.payload)
        response = self.parent.mqtt_parse_message(message)

        self.callback(response)

    def on_connect(self, client, obj, flags, rc):
        """ Callback for when the client receives a CONNACK response from the server.

        :param client: MQTT Client
        :param obj: Ignored
        :param flags: Ignored
        :param rc: Result Code
        :return: Nothing
        """
        # Ignored Parameters
        del obj
        del flags

        if rc == 0:

            client.connected_flag = True  # set flag
            self.callback(Response.ACN_MQTT_CONNECTED)
            if DEBUG:
                print("connected OK Returned code=", rc)
                print('subscribing to {}'.format(self.MQTT_SUBSCRIBE_TOPIC))
            client.subscribe(self.MQTT_SUBSCRIBE_TOPIC)
        else:
            print("Bad connection Returned code= ", rc)

    def on_disconnect(self, client, obj, flags, rc):
        """ Callback for when a disconnect message is received from the server.

        :param client: MQTT Client
        :param obj: Ignored
        :param flags: Ignored
        :param rc: Result Code
        :return: Nothing
        """
        # Ignored Parameters
        del obj
        del flags

        print("MQTT Disconnected")

        if rc == 0:
            client.connected_flag = True  # clear flag
            self.callback(Response.ACN_MQTT_DISCONNECTED)
            if DEBUG:
                print('Client Disconnected: {}'.format(rc))
        else:
            client.loop_stop()

    def mqtt_init(self, callback):
        """ Initialize the MQTT connection

        :param callback: Function to be called when an MQTT callback is received.
        :return: Nothing
        """
        self.callback = callback
        self.mqtt_client.loop_start()

        self.mqtt_client.username_pw_set(self.MQTT_USERNAME, self.APPLICATION_OWNER_RAW_API_KEY)
        try:
            self.mqtt_client.connect(self.MQTT_HOST, self.MQTT_PORT, self.MQTT_TIMEOUT)
        except Exception as e:
            logging.exception(e)
            print("connection failed")

    def find_gateways(self):
        """ Find all gateways on Arrow Connect for the given APPLICATION_OWNER_RAW_API_KEY

        :return: JSON formatted data
        """
        # HTTP request URL
        url = 'https://api.arrowconnect.io/api/v1/kronos/gateways'

        # HTTP request parameters
        parameters = {
            "_page": 0,
            "_size": 100
        }

        # HTTP request headers
        headers = {
            "accept": "application/json",
            "x-auth-token": self.APPLICATION_OWNER_RAW_API_KEY
        }

        r = requests.get(url, params=parameters, headers=headers, verify=False)
        data = r.json()['data']

        if DEBUG:
            print(r.url)
            print(r.content)

            print("JSON Data: {}".format(data))
            for gateway in data:
                print("Gateway HID {}".format(gateway["hid"]))
                print("Gateway UID {}".format(gateway["uid"]))

        return data

    def find_device(self):
        """ Find device on Arrow Connect for the given DEVICE_UID and APPLICATION_OWNER_RAW_API_KEY

        :return: JSON formatted data if the device is found, otherwise None.
        """
        # HTTP request URL
        url = 'https://api.arrowconnect.io/api/v1/kronos/devices'

        # HTTP request parameters
        parameters = {
            "_page": 0,
            "_size": 100,
            "uid": self.DEVICE_UID
        }

        # HTTP request headers
        headers = {
            "accept": "application/json",
            "x-auth-token": self.APPLICATION_OWNER_RAW_API_KEY
        }

        r = requests.get(url, params=parameters, headers=headers, verify=False)
        if r.status_code == requests.codes.ok:
            try:
                data = r.json()['data']

                if DEBUG:
                    print(r.url)
                    print(r.content)

                    print("JSON Data: {}".format(data))
                    for device in data:
                        print("Device HID {}".format(device["hid"]))
                        print("Device UID {}".format(device["uid"]))
                        print("Gateway HID {}".format(device["gatewayHid"]))

                return data
            except KeyError:
                print("Find Device KeyError, print GET request & response\n{}\n{}".format(url, r.json()))
                return None

        elif r.status_code == requests.codes.unauthorized:
            print("Unauthorized - Try Again?")
            self.find_device()

    def find_devices(self):
        """ Find all devices on Arrow Connect for the given APPLICATION_OWNER_RAW_API_KEY

        :return: JSON formatted data received from Arrow Connect
        """
        # HTTP request URL
        url = 'https://api.arrowconnect.io/api/v1/kronos/devices'

        # HTTP request parameters
        parameters = {
            "_page": 0,
            "_size": 100
        }

        # HTTP request headers
        headers = {
            "accept": "application/json",
            "x-auth-token": self.APPLICATION_OWNER_RAW_API_KEY
        }

        r = requests.get(url, params=parameters, headers=headers, verify=False)
        data = r.json()['data']

        if DEBUG:
            print(r.url)
            print(r.content)

            print("JSON Data: {}".format(data))
            for device in data:
                print("Device HID {}".format(device["hid"]))
                print("Device UID {}".format(device["uid"]))

        return data

    def mqtt_send(self, data):
        """ Sends data to Arrow Connect

        :param data: JSON formatted data
        :return: Nothing
        """
        self.mqtt_client.publish(self.MQTT_PUBLISH_TOPIC, data, qos=1, retain=False)
