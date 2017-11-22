# iotjstest

## System I/O Test

### Hardware schematic
#### Raspberry PI
#### Artik053
  ![artik053](https://github.com/hs0225/iotjstest/blob/master/artik053-systemio.png)
#### Stm32f4 discovery

### Test guide
#### ADC
 - hardware: number3(illumination sensor) - test_adc.js
   - process
      1. Run test app 'iotjs run_pass/test_adc.js'.
      2. 'test1 start(read async test)' is printed.
      3. The numbers are printed. (read async test)
      4. 'test2 start(read sync test)' is printed.
      5. The numbers are printed. (read sync test)
   - result
      1. If the light is bright, the number will increase.
      2. If the light is dark, the number will decrease.
    
#### GPIO
 - hardware: number5(LED) - test_gpio_output.js
   - process
      1. Run test app 'iotjs run_pass/test_gpio_output.js'.
      2. 'gpio read: true' is printed.
      3. 'gpio read: false' is printed.
   - result
      1. If the read is true, the light is on.
      2. If the read is false, the light is off.
  
 - hardware: number2(switch), number5(LED) - test_gpio_input.js
   - process
      1. Run test app 'iotjs run_pass/test_gpio_input.js'.
      2. Press the switch.
   - result
      1. When the switch is pressed, 'led on' is printed and led is on.
  
#### I2C
 - hardware: number1(illumination sensor) - test_i2c.js
   - process
      1. Run test app 'iotjs run_pass/test_i2c.js'.
      2. 'result: %d, %d' is printed.
      3. Try to run test app repeatedly.
   - result
      1. The initial value is '0, 0'.
      2. The brighter the light, the greater the number.
  
#### PWM
 - hardware: number5(LED) - test_pwm_async.js, test_pwm_sync.js
   - process
      1. Run test app 'iotjs run_pass/test_pwm_async.js'.
      2. 'dutycycle(%d)' is printed.
      3. 'frequency(%d)' is printed.
      4. Run test app 'iotjs run_pass/test_pwm_sync.js'
      5. 'test_pwm_async.js' and 'test_pwm_sync.js' result are the same.
   - result
      1. Each time the dutycycle increases, led becomes brighter.
      2. Each time frequency increases, led blinks faster.

#### SPI
 - hardware: number4(mcp3008), number3(illumination sensor) - test_spi_mcp3008.js
    - process
      1. Run test app 'iotjs run_pass/test_spi_mcp3008.js'.
      2. The numbers are printed.
    - result
      1. If the light is bright, the number will increase.
      2. If the light is dark, the number will decrease.
 - hardware: None. Connect MISO(brown line), MOSI(red line). **important** - test_spi_buffer.js
    - process
        1. Run test app 'iotjs run_pass/test_spi_buffer.js'.
    - result
        1. print(Hello IoTjs\nHello IoTjs)
 
#### UART
 - hardware: number6(usb serial)
   - process
      1. Connect hardware 5 with your desktop. And run serial communication program(minicom).
      2. Try keyboard input in your desktop serial program.
   - result
      1. 'Hello IoT.js' and 'Hello there?' is printed in your desktop serial program.
      2. The entered character is printed.(read result: %c)











