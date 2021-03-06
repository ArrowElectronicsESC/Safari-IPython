# This is set up for the 3 sensors used in the Safari demo- accelerometer, RTD, pressure 
# Note: Channel 0 is used for the accelerometer, channel 4 for the RTD, channel 6 for the pressure sensor

# Before running in Demo mode, make sure jumpers are set as follows: J1 on, J2 off, J3 on, J4 off
# Jumper for JP5 is across pins 1-2 and jumper for JP6 is across pins 2-3 to enable on-board reference 

ad7124_register_settings = {
    'AD7124_STATUS_REG': {
        'address': 0x00,
        'default_value': 0x00,
        'size': 1,
        'r/w': 'r'},

    # Full power and continuous conversion modes are selected; all other parameters are set to default values
    'AD7124_ADC_CTRL_REG': {
        'address': 0x01,
        'default_value': 0x0480,
        'size': 2,
        'r/w': 'rw'},

    # This is a read-only register that stores the digital code representing the analog voltage measured
    'AD7124_DATA_REG': {
        'address': 0x02,
        'default_value': 0xFFFFFF,
        'size': 3,
        'r/w': 'r'},

    # IO CONTROL 1 REGISTER ENABLES GPIOS, ENABLES INTERNAL CURRENT SOURCES, SETS VALUES OF CURRENT 
    # SOURCES AND SELECTS WHICH PINS TO USE AS OUTPUTS FOR CURRENT SOURCES
    # For the demo two 500uA current sources are enabled via pins AIN2 and AIN3
    'AD7124_IO_CTRL1_REG': {
        'address': 0x03,
        'default_value': 0x002432,
        'size': 3,
        'r/w': 'rw'},

    # IO CONTROL 2 REGISTER ENABLES/DISABLES AN INTERNAL VOLTAGE SOURCE SET TO VDD/2 AND SELECTS 
    # WHICH PINS TO USE AS OUTPUTS
    # For the demo the internal bias voltages are disabled
    'AD7124_IO_CTRL2_REG': {
        'address': 0x04,
        'default_value': 0x0000,
        'size': 2,
        'r/w': 'rw'},

    # This identifies I.C. as the AD7124-8 B Grade
    'AD7124_ID_REG': {
        'address': 0x05,
        'default_value': 0x16,
        'size': 1,
        'r/w': 'r'},

    'AD7124_ERR_REG': {
        'address': 0x06,
        'default_value': 0x000000,
        'size': 3,
        'r/w': 'r'},

    # SPI_IGNORE_ERR bit set
    'AD7124_ERREN_REG': {
        'address': 0x07,
        'default_value': 0x000040,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_MCLK_COUNT': {
        'address': 0x08,
        'default_value': 0x00,
        'size': 1,
        'r/w': 'r'},

    # CHANNEL REGISTERS- SELECTS + AND - INPUTS, CHANNEL ENABLE/DISABLE, WHICH SETUP TO USE
    # For the demo only channels 0, 4 and 6 are used
    
    # Channel 0 connects the accelerometer to inputs AIN0 and AVSS(GND) and selects Setup 0
    'AD7124_CH0_MAP_REG': {
        'address': 0x09,
        'default_value': 0x8011,
        'size': 2,
        'r/w': 'rw'},

    # Channel 1 is disabled
    'AD7124_CH1_MAP_REG': {
        'address': 0x0A,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 2 is disabled
    'AD7124_CH2_MAP_REG': {
        'address': 0x0B,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 3 is disabled
    'AD7124_CH3_MAP_REG': {
        'address': 0x0C,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 4 connects the RTD to inputs AIN4 and AIN5 and selects Setup 4
    'AD7124_CH4_MAP_REG': {
        'address': 0x0D,
        'default_value': 0xC085,
        'size': 2,
        'r/w': 'rw'},

    # Channel 5 is disabled
    'AD7124_CH5_MAP_REG': {
        'address': 0x0E,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 6 connects the pressure sensor to inputs AIN6 and AVSS(GND) and selects Setup 6
    'AD7124_CH6_MAP_REG': {
        'address': 0x0F,
        'default_value': 0xE0D1,
        'size': 2,
        'r/w': 'rw'},

    # Channel 7 is disabled
    'AD7124_CH7_MAP_REG': {
        'address': 0x10,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 8 is disabled
    'AD7124_CH8_MAP_REG': {
        'address': 0x11,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 9 is disabled
    'AD7124_CH9_MAP_REG': {
        'address': 0x12,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 10 is disabled
    'AD7124_CH10_MAP_REG': {
        'address': 0x13,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 11 is disabled
    'AD7124_CH11_MAP_REG': {
        'address': 0x14,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 12 is disabled
    'AD7124_CH12_MAP_REG': {
        'address': 0x15,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 13 is disabled
    'AD7124_CH13_MAP_REG': {
        'address': 0x16,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 14 is disabled
    'AD7124_CH14_MAP_REG': {
        'address': 0x17,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # Channel 15 is disabled
    'AD7124_CH15_MAP_REG': {
        'address': 0x18,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    # CONFIGURATION (aka SETUP) REGISTERS- Selects which of 8 configuration settings to use (Setup 0-7)
    # EACH CONFIGURATION SPECIFIES BIPOLAR (+ INPUT CAN GO ABOVE OR BELOW - INPUT), OR 
    # UNIPOLAR (+ INPUT MUST NOT GO BELOW - INPUT) OPERATION, WHETHER BUFFERS ARE ENABLED ON THE INPUTS, 
    # GAIN (1-128), WHICH VOLTAGE REFERENCE TO USE (INTERNAL, EXTERNAL REF 1, EXTERNAL REF 2, VDD), 
    # AND WHETHER BUFFERS ARE ENABLED ON THE VOLTAGE REFERENCE.  ALSO ENABLES BURNOUT CURRENT SOURCES IF DESIRED
    # 
    # For the demo only Setups 0, 4 and 6 are used
    
    # Configuration 0 (used for accelerometer) has these settings: Gain=1, Buffer on + Input only, Unipolar operation, 
    # Reference used is AVdd, reference buffers off
    'AD7124_CFG0_REG': {
        'address': 0x19,
        'default_value': 0x0058,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 1 is not used
    'AD7124_CFG1_REG': {
        'address': 0x1A,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 2 is not used
    'AD7124_CFG2_REG': {
        'address': 0x1B,
       'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 3 is not used
    'AD7124_CFG3_REG': {
        'address': 0x1C,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 4 (used for RTD temperature sensor) has these settings: Gain=16, Buffers on both + and - Inputs, 
    # Unipolar operation, Reference used is REFIN1, both reference buffers on
    'AD7124_CFG4_REG': {
        'address': 0x1D,
        'default_value': 0x01E4,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 5 is not used
    'AD7124_CFG5_REG': {
        'address': 0x1E,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    # Setup 6 (used for pressure sensor) has these settings: Gain=1, Buffer on + input, Unipolar operation
    # Reference used is REFIN2 (on-board 2.5V reference), + reference buffer on
    'AD7124_CFG6_REG': {
        'address': 0x1F,
        'default_value': 0x0148,
        'size': 2,
        'r/w': 'rw'},

    # Configuration 7 is not used
    'AD7124_CFG7_REG': {
        'address': 0x20,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    # FILTER REGISTERS- SELECTS TYPE OF DIGITAL FILTER USED AFTER CONVERTING INPUT SIGNAL TO DIGITAL FORMAT, 
    # AND OUTPUT DATA RATE. EACH FILTER REGISTER CORRESPONDS TO A SPECIFIC SETUP- SETUP 0 USES FILTER REGISTER 0 FOR EXAMPLE
    
    # Filter Register 0 is setup for maximum sampling of 19.2ksps and the Sinc3 filter; 60Hz notch filter off
    'AD7124_FILT0_REG': {
        'address': 0x21,
        'default_value': 0x460001,
        'size': 3,
        'r/w': 'rw'},

    # Filter 1 is not used
    'AD7124_FILT1_REG': {
        'address': 0x22,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # Filter 2 is not used
    'AD7124_FILT2_REG': {
        'address': 0x23,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # Filter 3 is not used
    'AD7124_FILT3_REG': {
        'address': 0x24,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # Filter Register 4 is setup for a sampling rate of 50sps and the Sinc4 filter; 60Hz notch filter off
    'AD7124_FILT4_REG': {
        'address': 0x25,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # Filter 5 is not used
    'AD7124_FILT5_REG': {
        'address': 0x26,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # Filter Register 6 is setup for maximum sampling of 19.2ksps and the Sinc3 filter; 60Hz notch filter off
    'AD7124_FILT6_REG': {
        'address': 0x27,
        'default_value': 0x460001,
        'size': 3,
        'r/w': 'rw'},

    # Filter 7 is not used
    'AD7124_FILT7_REG': {
        'address': 0x28,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    # OFFSET REGISTERS-
    
    # Offset 0 is not used 
    'AD7124_OFFS0_REG': {
        'address': 0x29,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 1 is not used
    'AD7124_OFFS1_REG': {
        'address': 0x2A,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 2 is not used
    'AD7124_OFFS2_REG': {
        'address': 0x2B,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 3 is not used
    'AD7124_OFFS3_REG': {
        'address': 0x2C,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 4 is not used
    'AD7124_OFFS4_REG': {
        'address': 0x2D,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 5 is not used
    'AD7124_OFFS5_REG': {
        'address': 0x2E,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 6 is not used
    'AD7124_OFFS6_REG': {
        'address': 0x2F,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # Offset 7 is not used
    'AD7124_OFFS7_REG': {
        'address': 0x30,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    # GAIN REGISTERS- GAIN IS CALIBRATED AT THE FACTORY
    
    # Gain 0 is not used
    'AD7124_GAIN0_REG': {
        'address': 0x31,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 1 is not used
    'AD7124_GAIN1_REG': {
        'address': 0x32,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 2 is not used
    'AD7124_GAIN2_REG': {
        'address': 0x33,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 3 is not used
    'AD7124_GAIN3_REG': {
        'address': 0x34,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 4 is not used
    'AD7124_GAIN4_REG': {
        'address': 0x35,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 5 is not used
    'AD7124_GAIN5_REG': {
        'address': 0x36,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 6 is not used
    'AD7124_GAIN6_REG': {
        'address': 0x37,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    # Gain 7 is not used
    'AD7124_GAIN7_REG': {
        'address': 0x38,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'}
}