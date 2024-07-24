import pytest
from helpers import unhex

EMACS_VIM = """\
00000000: 0102 0304 0506 0708 090a 0b0c 0d0e 0f10  ................
00000010: 4142 4344 4546 4748 494a 4b4c 4d4e 4f44  ABCDEFGHIJKLMNOD
"""

HEXDUMP_C = """\
00000000  01 02 03 04 05 06 07 08  09 0a 0b 0c 0d 0e 0f 10  |................|
00000010  41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 44  |ABCDEFGHIJKLMNOD|
00000020
"""


EXPECTED = b"\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10ABCDEFGHIJKLMNOD"


@pytest.mark.parametrize(
    "hexdump",
    [
        pytest.param(EMACS_VIM, id="Vim-Emacs"),
        pytest.param(HEXDUMP_C, id="hexdump-C"),
    ],
)
def test_hexdump(hexdump):
    binary = unhex(hexdump)
    assert binary == EXPECTED


WITH_SQUEEZED_DATA = """\
00: 0102 0304 0506 0708 090a 0b0c 0d0e 0f10  ................
10: FF00 FF00 FF00 FF00 FF00 FF00 FF00 FF00  ................
*
30: 4142 4344 4546 4748 494a 4b4c 4d4e 4f44  ABCDEFGHIJKLMNOD
"""


def test_with_squized_data():
    binary = unhex(WITH_SQUEEZED_DATA)
    assert binary[:0x10] == EXPECTED[:0x10]
    assert binary[0x10:0x30] == b"\xff\x00" * 0x10
    assert binary[0x30:] == EXPECTED[0x10:]


WITH_SQUEEZED_END = """\
00: FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF  ................
*
40
"""


def test_with_squized_end():
    binary = unhex(WITH_SQUEEZED_END)
    assert len(binary) == 0x40
    assert binary == b"\xff" * 0x40


WITH_SQUEEZE_AFTER_SQUEEZE = """\
00000000  20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20  |                |
*
00000040  78 78 78 78 78 78 78 78  78 78 78 78 78 78 78 78  |xxxxxxxxxxxxxxxx|
*
00000080  20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20  |                |
*
000000C0
"""


def test_with_squeeze_after_squeeze():
    binary = unhex(WITH_SQUEEZE_AFTER_SQUEEZE)
    assert len(binary) == 0xC0
    assert binary[:0x40] == b" " * 0x40
    assert binary[0x40:0x80] == b"x" * 0x40
    assert binary[0x80:] == b" " * 0x40
