"""
https://stackoverflow.com/questions/57200685/how-to-convert-tron-address-to-different-format
"""
from typing import Optional

import base58

TOKEN_ADDRESSES = {
    'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t': 'USDT'
}


def symbol_for_address(address: str) -> Optional[str]:
    return TOKEN_ADDRESSES.get(address)


def hex_to_tron(address: str) -> str:
    """Convert a hex address to the more commonly used Txxxxxxxxx style."""
    if (address.startswith('0x')):
        address = '41' + address[2:]

    if (len(address) % 2 == 1):
        address = '0' + address

    return base58.b58encode_check(bytes.fromhex(address)).decode()
