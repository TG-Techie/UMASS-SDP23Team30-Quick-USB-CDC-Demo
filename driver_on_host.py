from msgpack import unpack
from io import BytesIO
from adafruit_board_toolkit import circuitpython_serial
from typing import Any

data_ports = circuitpython_serial.data_comports()

print(data_ports)

if len(data_ports) == 0:
    raise RuntimeError("no board plugged in")
elif len(data_ports) > 1:
    raise RuntimeError(
        "this is an example, please only plug in one circuitpython board",
        len(data_ports),
        data_ports,
    )


(info,) = data_ports

# print all related info
print(f"for the object {info}:")
for attrname in dir(info):
    if attrname.startswith("_"):
        continue
    print(f"    {attrname} = ", repr(getattr(info, attrname)))


print()  # often /dev/cu.usbmodem14503 on jay's mack

# print("connecting to the port")

# info.device

# with open(info.device, "r") as stream:
#     x = 0
#     while True:
#         print(x := x + 1)
#         print(unpack(stream))
# # msgpack.unpack()


print("connecting to the port")

START_SEQ = b"\x00\xff\xf0\x00"
END_SEQ = b"\x0f\xf0\x00\xff"


def read_packet() -> list[Any] | dict[Any, Any]:
    sync_bytes = stream.read(len(START_SEQ))
    if sync_bytes != START_SEQ:
        raise RuntimeError(
            f"got illformed sync data {repr(sync_bytes)}, expected {repr(START_SEQ)}"
        )

    del sync_bytes  # for sanity

    # the next is the length
    datalen = stream.read(1)[0]

    print(f"{datalen=}")

    rawdata = stream.read(datalen)

    print(f"{rawdata=}")

    # then check for the end of the packet

    end_sync = stream.read(len(END_SEQ))

    if end_sync != END_SEQ:
        raise RuntimeError(
            f"got illformed end sync data {repr(end_sync)}, expected {repr(END_SEQ)}"
        )

    buf = BytesIO(rawdata)
    decoded_data = unpack(buf)

    return decoded_data


with open(info.device, "rb") as stream:
    while True:
        data = read_packet()
        print()
        print(f"The send data, decoded {data=}")
        print()


# msgpack.unpack()
