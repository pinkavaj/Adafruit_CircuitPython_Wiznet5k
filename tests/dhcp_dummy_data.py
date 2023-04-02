# SPDX-FileCopyrightText: 2022 Martin Stephens
#
# SPDX-License-Identifier: MIT
"""Data for use in test_dhcp_helper_files.py"""


def _pad_message(message_section: bytearray, target_length: int) -> bytearray:
    """Pad the message with 0x00."""
    return message_section + bytearray(b"\00" * (target_length - len(message_section)))


def _build_message(message_body: bytearray, message_options: bytearray) -> bytearray:
    """Assemble the padded message and body to make a 512 byte packet. The 'header'
    section must be 236 bytes and the entire message must be 512 bytes."""
    dhcp_message = _pad_message(message_body, 236) + _pad_message(message_options, 276)
    assert len(dhcp_message) == 512
    return dhcp_message


# Data for testing send data.
# DHCP DISCOVER messages.
# Default settings (DISCOVER, broadcast=False, default hostname, renew=False)
message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00\x17\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x05\x06\x07"
    b"\x08\t\x00\x00\x00\x00\x00\x00\x00\x00"
)
options = bytearray(
    b"c\x82Sc5\x01\x01\x0c\x12WIZnet040506070809=\x07\x01"
    b"\x04\x05\x06\x07\x08\t7\x03\x01\x03\x063\x04\x00v\xa7\x00\xff"
)
DHCP_SEND_01 = _build_message(message, options)

message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00\x17\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x05\x06\x07"
    b"\x08\t"
)
options = bytearray(
    b"c\x82Sc5\x01\x01\x0c\x12WIZnet040506070809=\x07\x01"
    b"\x04\x05\x06\x07\x08\t7\x03\x01\x03\x063\x04\x00v\xa7\x00\xff"
)
DHCP_SEND_02 = _build_message(message, options)

message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00#\x80\x00\xc0\xa8\x03\x04"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18#.9DO"
)
options = bytearray(
    b"c\x82Sc5\x01\x01\x0c\x04bert=\x07\x01\x18#.9DO7"
    b"\x03\x01\x03\x063\x04\x00v\xa7\x00\xff"
)
DHCP_SEND_03 = _build_message(message, options)

message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00#\x80\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xffa$e*c"
)
options = bytearray(
    b"c\x82Sc5\x01\x01\x0c\x05clash=\x07\x01\xffa$e*c7"
    b"\x03\x01\x03\x063\x04\x00v\xa7\x00\xff"
)
DHCP_SEND_04 = _build_message(message, options)

# DHCP REQUEST messages.
message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00\x10\x80\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xffa$e*c"
)

options = bytearray(
    b"c\x82Sc5\x01\x03\x0c\nhelicopter=\x07\x01\xffa$e*c7"
    b"\x03\x01\x03\x063\x04\x00v\xa7\x002\x04\n\n\n+6\x04\x91B-\x16\xff"
)
DHCP_SEND_05 = _build_message(message, options)

message = bytearray(
    b"\x01\x01\x06\x00o\xff\xff\xff\x00H\x80\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00K?\xa6\x04"
    b"\xc8e"
)

options = bytearray(
    b"c\x82Sc5\x01\x03\x0c\x12WIZnet4B3FA604C865=\x07\x01K?\xa6"
    b"\x04\xc8e7\x03\x01\x03\x063\x04\x00v\xa7\x002\x04def\x046"
    b"\x04\xf5\xa6\x05\x0b\xff"
)
DHCP_SEND_06 = _build_message(message, options)

# Data to test response parser.
# Basic case, no extra fields, one each of router and DNS.
message = bytearray(
    b"\x02\x00\x00\x00\x7f\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\xc0"
    b"\xa8\x05\x16\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x05\x07\t\x0b"
)

options = bytearray(
    b"c\x82Sc5\x01\x02\x01\x04\xc0\xa8\x06\x026\x04\xeao\xde"
    b"{3\x04\x00\x01\x01\x00\x03\x04yy\x04\x05\x06\x04\x05\x06"
    b'\x07\x08:\x04\x00""\x00;\x04\x0033\x00\xff'
)
GOOD_DATA_01 = _build_message(message, options)

# Complex case, extra field, 2 routers and 2 DNS servers.
message = bytearray(
    b"\x02\x00\x00\x004Vx\x9a\x00\x00\x00\x00\x00\x00\x00\x00\x12$@\n\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x01"
)
options = bytearray(
    b"c\x82Sc5\x01\x05<\x05\x01\x02\x03\x04\x05\x01\x04\n\x0b"
    b"\x07\xde6\x04zN\x91\x03\x03\x08\n\x0b\x0e\x0f\xff\x00"
    b"\xff\x00\x06\x08\x13\x11\x0b\x07****3\x04\x00\x00=;:\x04"
    b"\x00\x0e\x17@;\x04\x02\x92]\xde\xff"
)
GOOD_DATA_02 = _build_message(message, options)


#
message = bytearray(
    b"\x02\x00\x00\x00\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x12$@\n\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x01"
)
options = bytearray(b"c\x82Sc")
BAD_DATA = _build_message(message, options)
