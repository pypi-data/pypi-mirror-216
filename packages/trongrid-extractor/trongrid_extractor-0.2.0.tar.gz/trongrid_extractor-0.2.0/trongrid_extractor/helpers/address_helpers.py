"""
https://stackoverflow.com/questions/57200685/how-to-convert-tron-address-to-different-format
"""
from typing import Optional

import base58
import logging

from trongrid_extractor.helpers.dict_helper import get_dict_key_by_value

TOKEN_ADDRESSES = {
    'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t': 'USDT',
    'TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9': 'BTCT',
    'TPYmHEhy5n8TCEfYGqW2rPxsghSfzghPDn': 'USDD',
    'TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8': 'USDC',
    'TUpMhErZL2fhh4sVNULAbNKLokS4GjC1F4': 'TUSD',
    'TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT': 'USDJ',
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


def is_contract_address(address: str) -> bool:
    """Returns true if it looks like a Tron contract address."""
    return address[0] == 'T' and len(address) == 34


def symbol_address(symbol: str) -> Optional[str]:
    try:
        return get_dict_key_by_value(TOKEN_ADDRESSES, symbol)
    except ValueError:
        logging.warning(f"No address found for '{symbol}'!")
