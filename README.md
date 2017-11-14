# iotjstest

## System I/O Test

### Hardware schematic
#### Raspberry PI
#### Artik053
  ![artik053](https://github.com/hs0225/iotjstest/blob/master/artik053-systemio.png)
#### Stm32f4 discovery

### Test guide
#### ADC
  - Hardware: number3 (illumination sensor)
  - Test App: test_adc.js
  - process
    1. Run test app 'iotjs run_pass/test_adc.js'.
    2. 'test1 start(read async test)' is printed.
    3. The numbers are printed. (read async test)
    4. 'test2 start(read sync test)' is printed.
    5. The numbers are printed. (read sync test)
  - result
    1. If the light is bright, the number will increase.
    2. If the light is dark, the number will decrease.

