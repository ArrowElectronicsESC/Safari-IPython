########################################################################################################################
#                                            Imports Required                                                          #
########################################################################################################################
import ad7124
import time
import logging


########################################################################################################################
#                                            Global Variables                                                          #
########################################################################################################################
ACCELEROMETER_CHANNEL = 0       # Channel connected to accelerometer
TEMPERATURE_CHANNEL = 4         # Channel connected to RTD temperature sensor
PRESSURE_CHANNEL = 6            # Channel connected to differential pressure sensor
ALERT_THRESHOLD_VOLTAGE = 2.0   # Voltage threshold for detecting a fault condition


########################################################################################################################
#                                            Support Functions                                                         #
########################################################################################################################


def convert_pressure(voltage):
    ''' Convert the supplied voltage to Pascals

    :param voltage: Voltage to convert
    :return: Pressure measured in Pascals (Pa)


    DP = (190 * Vmeas)/Vdd - 38Pa
    Example:
    Vmeas = 875mV, Vdd = 3.3V
    Differential Pressure = (190 * 0.875V)/3.3V - 38Pa = 12.37Pa
    '''
    vdd = 3.3
    r1 = 132000
    r2 = 100000
    return round(((190.0 * voltage * (r1/r2)) / vdd - 38), 3)


def convert_temperature(code):
    ''' Convert the supplied code to temperature

    :param code: Raw ADC value received from AD7124
    :return: Temperature in degrees Celsius.


    RTD Resistance = (Code * 5.11kOhms) / ((2^24) * 16)
    Temperature (Degrees C) = (RTD Resistance - 100ohms) / (0.385 ohms/degC)
    '''
    r_rtd = (code * 5110) / ((2**24) * 16)
    temp = (r_rtd - 100) / 0.385
    return round(temp, 3)


# Function for reading data from the AD7124 sensor
def ad7124_read_data():

    # Wait until the AD7124 indicates it is ready before reading data
    while not ad7124.check_data_ready():
        # wait for conversion to complete
        pass

    # Read from the AD7124 data register
    #
    # Byte 0 - Garbage
    # Bytes 1, 2, 3 - Raw ADC reading
    # Byte 4 - Status register Contents
    ret_val = ad7124.read_data_reg()

    # Shift the bytes into the proper position and OR them together to get the raw ADC value or 'Code'
    adc_raw_value = (ret_val[1] << 16) | (ret_val[2] << 8) | (ret_val[3] << 0)

    # Mask the status register byte to identify the channel the raw value corresponds to
    channel = ret_val[4] & 0x0F

    # Read the config number from the AD7124_DEFAULT_REGISTER_SETTINGS array
    config = (ad7124.ad7124_register_settings[ad7124.AD7124_CHANNELS[channel]]['default_value'] & ad7124.AD7124_CH_MAP_REG_CH_CONFIG) >> 12

    # Convert the config number into an array index to look up values from the AD7124_DEFAULT_REGISTER_SETTINGS array
    ad7124_config = ad7124.ad7124_register_settings[ad7124.AD7124_CONFIGS[config]]['default_value']

    # Read the voltage reference from the AD7124_DEFAULT_REGISTER_SETTINGS array
    ad7124_reference = (ad7124_config & ad7124.AD7124_CFG_REG_REF_SEL) >> 3

    # Look up the corresponding VREF voltage from the reference_voltage array
    vref = ad7124.reference_voltage[ad7124_reference]

    # Look up the polarity from the AD7124_DEFAULT_REGISTER_SETTINGS array
    polarity = (ad7124_config & ad7124.AD7124_CFG_REG_BIPOLAR) >> 11

    # Look up the gain from the AD7124_DEFAULT_REGISTER_SETTINGS array
    gain = ad7124.gain_values[(ad7124_config & ad7124.AD7124_CFG_REG_GAIN) >> 0]

    # Convert the raw ADC value (Code) to a voltage
    voltage = ad7124.convert_raw_value(adc_raw_value, polarity, vref, gain)

    # We always want to send the accelerometer data across the serial connection and never to the cloud.
    # This is done to limit the amount of data sent to the cloud.
    if channel == ACCELEROMETER_CHANNEL:
        print('channel,{},timestamp,{},voltage,{},code,{}'
              .format(channel, int(round(time.time() * 1000000)), voltage, adc_raw_value))
    elif channel == TEMPERATURE_CHANNEL:
        print('channel,{},timestamp,{},voltage,{},code,{}'
              .format(channel, int(round(time.time() * 1000000)), voltage, adc_raw_value))
    elif channel == PRESSURE_CHANNEL:
        print('channel,{},timestamp,{},voltage,{},code,{}'
              .format(channel, int(round(time.time() * 1000000)), voltage, adc_raw_value))
    else:
        print('channel,{},timestamp,{},voltage,{},code,{}'
              .format(channel, int(round(time.time() * 1000000)), voltage, adc_raw_value))


########################################################################################################################
#                                                   Main Loop                                                          #
########################################################################################################################
if __name__ == '__main__':

    # Attempt to initialize the AD7124.
    #
    # If there is a problem communicating with the AD7124, this function will hang
    ad7124.init()
    print('Starting AD7124 Data Collection...')

    while True:
        # Continuously read data from the AD7124
        ad7124_read_data()