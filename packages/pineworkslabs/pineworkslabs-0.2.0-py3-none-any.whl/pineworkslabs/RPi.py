from typing import NamedTuple
from gpiod import line_request, chip

OUT = 1
IN = 0
HIGH = 1
LOW = 0
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2


class Pin(NamedTuple):
    gpio: int
    io: int


LE_POTATO_LOOKUP = {
    18: Pin(0, 6), 19: Pin(1, 86), 20: Pin(1, 82), 21: Pin(1, 83), 22: Pin(0, 10), 23: Pin(1, 93), 24: Pin(1, 94),
    25: Pin(1, 79), 26: Pin(1, 84), 27: Pin(0, 9), 'SCL': Pin(0, 4), 'SDA': Pin(0, 5), 'ID_SC': Pin(1, 76),
    'ID_SD': Pin(1, 75), 17: Pin(0, 8), 16: Pin(1, 81), 13: Pin(1, 85), 12: Pin(1, 95), 6: Pin(1, 97), 5: Pin(1, 96),
    4: Pin(1, 98), 'CE1': Pin(1, 80), 'CE0': Pin(1, 89), 'MOSI': Pin(1, 87), 'MISO': Pin(1, 88), 'SCLK': Pin(1, 90),
    'RX': Pin(1, 92), 'TX': Pin(1, 91)
}
RASPBERRY_PI_LOOKUP = {
    16: Pin(0, 16), 13: Pin(0, 13), 12: Pin(0, 12), 6: Pin(0, 6), 5: Pin(0, 5), 4: Pin(0, 4), 11: Pin(0, 11),
    18: Pin(0, 18), 19: Pin(0, 19), 20: Pin(0, 20), 21: Pin(0, 21), 22: Pin(0, 22), 23: Pin(0, 23), 24: Pin(0, 24),
    25: Pin(0, 25), 26: Pin(0, 26), 27: Pin(0, 27)
}
LOOKUP_TABLE = dict()
boards = {i: chip(i) for i in [0, 1]}

pinStates = {}


def setmode(mode: dict):
    LOOKUP_TABLE.clear()
    LOOKUP_TABLE.update(mode)
    cleanup()


def setup(pin: int, direction: int, pull_up_down: int = PUD_DOWN):
    board = boards[LOOKUP_TABLE[pin].gpio]
    config = line_request()
    config.consumer = 'PIN'
    config.flags = line_request.FLAG_BIAS_DISABLE if direction else {
        PUD_OFF: line_request.FLAG_BIAS_DISABLE,
        PUD_DOWN: line_request.FLAG_BIAS_PULL_DOWN,
        PUD_UP: line_request.FLAG_BIAS_PULL_UP
    }[pull_up_down]
    config.request_type = {
        OUT: line_request.DIRECTION_OUTPUT,
        IN: line_request.DIRECTION_INPUT
    }[direction]
    pinLine = board.get_line(LOOKUP_TABLE[pin].io)
    pinLine.release()
    pinLine.request(config)
    pinStates.update(({pin: pinLine}))


def output(pin: int, value: int):
    pinStates[pin].set_value(value)


def input(pin: int):
    return pinStates[pin].get_value()


def cleanup():
    for pin in LOOKUP_TABLE:
        setup(pin, OUT, PUD_UP)
        output(pin, LOW)
