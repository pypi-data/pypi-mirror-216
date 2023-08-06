# Pineworks Labs Breakout Interface

## Installation

```bash
pip install pineworkslabs
```

## RP2040 GPIO Standalone

The RP2040 GPIO is a standalone module which uses the `telemetrix` library to interface over serial.

### Importing

To import this package, run:
```py
import pineworkslabs.GPIO as GPIO
```

### Connecting to the GPIO

When the package is imported on a connected PC, the setup code will find a compatible GPIO board on a connected COM port.

#### Example: blink an LED

```py
import pineworkslabs.GPIO as GPIO
import time
GPIO.setmode(GPIO.PINEWORKS)

pin = 20

while True:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.25)
    except KeyboardInterrupt:
        GPIO.cleanup()
```

## Raspberry Pi 4 / LePotato

Pineworks Labs legacy GPIO boards are a breakout module to be used with a Raspberry Pi 4+ or a [Libre Computer Board (LePotato AML-905X-CC-V1.0-A)](https://libre.computer/products/aml-s905x-cc/).

### Importing

To import this package on the RPi or LePotato, run:
```py
import pineworkslabs.RPi as GPIO
```

### Setting the mode

The relevant difference between the Raspberry Pi and the LePotato for this package is the GPIO pinout. Use the following command to set the appropriate pinout lookup table:
```py
setmode(RASPBERRY_PI_LOOKUP)
```
or
```py
setmode(LE_POTATO_LOOKUP)
```

Not all pins are available for output, depending on the mode.

### Reading and writing pins

To read a pin, first set it up using the `IN` flag, then read it with `input`.
```py
pin: int | str = 20
setup(pin, IN)
print(input(pin))
```

Similarly, to write a pin, set it up using the `OUT` flag, then write to it with `output`.
```py
pin: int | str = 20
setup(pin, OUT)
output(pin, HIGH)
```

### Cleaning up

To reset all pins to `LOW`, run:
```py
cleanup()
```

#### Example: blink an LED (LePotato)

```py
import pineworkslabs.RPi as GPIO
import time
GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

pin = 20

while True:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.25)
    except KeyboardInterrupt:
        GPIO.cleanup()
```

## Acknowledgements

We are indebted to the work of the [`telemetrix`](https://pypi.org/project/telemetrix-rpi-pico/) team for serial connectivity between the PC and the GPIO board, and the [`gpiod`](https://pypi.org/project/gpiod/) team for the interface between the Raspberry Pi/LePotato and the GPIO.