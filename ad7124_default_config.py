ad7124_register_settings = {
    'AD7124_STATUS_REG': {
        'address': 0x00,
        'default_value': 0x00,
        'size': 1,
        'r/w': 'r'},

    'AD7124_ADC_CTRL_REG': {
        'address': 0x01,
        'default_value': 0x0480,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_DATA_REG': {
        'address': 0x02,
        'default_value': 0xFFFFFF,
        'size': 3,
        'r/w': 'r'},

    'AD7124_IO_CTRL1_REG': {
        'address': 0x03,
        'default_value': 0x002432,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_IO_CTRL2_REG': {
        'address': 0x04,
        'default_value': 0x0000,
        'size': 2,
        'r/w': 'rw'},

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

    'AD7124_CH0_MAP_REG': {
        'address': 0x09,
        'default_value': 0x8011,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH1_MAP_REG': {
        'address': 0x0A,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH2_MAP_REG': {
        'address': 0x0B,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH3_MAP_REG': {
        'address': 0x0C,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH4_MAP_REG': {
        'address': 0x0D,
        'default_value': 0xC085,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH5_MAP_REG': {
        'address': 0x0E,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH6_MAP_REG': {
        'address': 0x0F,
        'default_value': 0xE0D1,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH7_MAP_REG': {
        'address': 0x10,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH8_MAP_REG': {
        'address': 0x11,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH9_MAP_REG': {
        'address': 0x12,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH10_MAP_REG': {
        'address': 0x13,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH11_MAP_REG': {
        'address': 0x14,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH12_MAP_REG': {
        'address': 0x15,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH13_MAP_REG': {
        'address': 0x16,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH14_MAP_REG': {
        'address': 0x17,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CH15_MAP_REG': {
        'address': 0x18,
        'default_value': 0x0001,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG0_REG': {
        'address': 0x19,
        'default_value': 0x0058,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG1_REG': {
        'address': 0x1A,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG2_REG': {
        'address': 0x1B,
       'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG3_REG': {
        'address': 0x1C,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG4_REG': {
        'address': 0x1D,
        'default_value': 0x01E4,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG5_REG': {
        'address': 0x1E,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG6_REG': {
        'address': 0x1F,
        'default_value': 0x0148,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_CFG7_REG': {
        'address': 0x20,
        'default_value': 0x0860,
        'size': 2,
        'r/w': 'rw'},

    'AD7124_FILT0_REG': {
        'address': 0x21,
        'default_value': 0x460001,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT1_REG': {
        'address': 0x22,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT2_REG': {
        'address': 0x23,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT3_REG': {
        'address': 0x24,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT4_REG': {
        'address': 0x25,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT5_REG': {
        'address': 0x26,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT6_REG': {
        'address': 0x27,
        'default_value': 0x460001,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_FILT7_REG': {
        'address': 0x28,
        'default_value': 0x060180,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS0_REG': {
        'address': 0x29,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS1_REG': {
        'address': 0x2A,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS2_REG': {
        'address': 0x2B,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS3_REG': {
        'address': 0x2C,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS4_REG': {
        'address': 0x2D,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS5_REG': {
        'address': 0x2E,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS6_REG': {
        'address': 0x2F,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_OFFS7_REG': {
        'address': 0x30,
        'default_value': 0x800000,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN0_REG': {
        'address': 0x31,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN1_REG': {
        'address': 0x32,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN2_REG': {
        'address': 0x33,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN3_REG': {
        'address': 0x34,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN4_REG': {
        'address': 0x35,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN5_REG': {
        'address': 0x36,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN6_REG': {
        'address': 0x37,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'},

    'AD7124_GAIN7_REG': {
        'address': 0x38,
        'default_value': 0x5558CC,
        'size': 3,
        'r/w': 'rw'}
}