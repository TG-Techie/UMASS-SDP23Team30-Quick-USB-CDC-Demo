# UMASS-SDP23Team30-Quick-USB-CDC-Demo

This was a quick (and rought) demo whipped together to demonstrate transporting msgpack objects over USB CDC data streams using circuit python.

## software

#### Setup
- Install circuitpython 8.0 or greater onto your board (tested with 8.0.2)
- Drage the contents of, well,  `./board-contents` onto the `CIRCUITPY` USB Device
- Run `./driver_on_host.py` on your local device
- Enjoy?

When restating either script, be sure to restart the other as well.

#### Error handling
If any data is missing or mal-encoded the program(s) is not built to recover or re-try transmission. Instead, it will ~~throw a fit~~ raise excetions accordingly.

#### about
Each packet is composed of four sections (l)
1. Sync start `b"\x00\xff\xf0\x00"`
1. One byte indicating the length of the data (in bytes)
1. Msgpack encoded binary data
1. Sync end `b"\x0f\xf0\x00\xff"`

This format was choosen to
A. Somewhat mirror a packet base protocl we'll be implemnting later.
B. To format msgpack so it can be transmitted over a stream
C. The format is quick, easy, and clear.

## Hardware
- 1x Adafruit RP2040 Feather (or any CP board w/ a qwiic connector attached to `board.I2C()`)
- 1x Sparkfun's VCNL4040 breakout board (or equivalent)
- 1x Compatible USB cable 
- 1x quiic I2C cable (just to make it more quick... most fast.. much easy: there we go)


<img src="https://user-images.githubusercontent.com/39284876/219295642-8ef15731-eaa0-4e73-b0dc-da34b8b81d20.jpeg" style="width: 20em; ">
