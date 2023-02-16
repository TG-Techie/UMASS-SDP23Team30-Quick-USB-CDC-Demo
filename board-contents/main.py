import board
import time
import adafruit_vcnl4040
import usb_cdc
import msgpack
from io import BytesIO

if not usb_cdc.data:
    raise RuntimeError(
        "usb CDC data channel not enabled. ensure "
        + "usb_cdc.enable(console=True, data=True) is called in boot.py"
    )

port = board.I2C()
port.try_lock()
(addr,) = port.scan()
port.unlock()
del port

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_vcnl4040.VCNL4040(i2c, address=addr)


# set no timeout, always wait to transmit everything
usb_cdc.data.write_timeout = None

START_SEQ = b"\x00\xff\xf0\x00"
END_SEQ = b"\x0f\xf0\x00\xff"

# def init_host_interface():
#     assert usb_cdc.data is not None
#     usb_cdc.data.write(START_SEQ)


def send_packet_to_host(source):
    buf = BytesIO()

    dataport = usb_cdc.data
    assert dataport is not None

    msgpack.pack(source, buf)

    data = buf.getvalue()
    datalen = len(data)
    assert datalen <= 255

    dataport.write(START_SEQ)
    # then send the length in bytes
    dataport.write(bytes([len(data)]))

    data_remaining = data
    while len(data_remaining):
        written = dataport.write(data_remaining)
        data_remaining = data_remaining[written:]

    dataport.write(END_SEQ)

    print(usb_cdc.data.out_waiting)
    print("start msgpack data (example)")
    print("```")
    print(buf.getvalue())
    print("```")
    print("sent")

    # written = 0
    # while written < len(data):
    #     assert usb_cdc.data is not None
    #     written += usb_cdc.data.write(data)
    # if written > len(data):
    #     raise ValueError("more bytes trasnmistted than expected")


while True:

    data = {"prox": sensor.proximity}

    print(f"sending the following data: raw = {repr(data)}, sent in msgpack")

    send_packet_to_host(data)
    # print("Light: %d lux" % sensor.lux)
    time.sleep(1.0)
