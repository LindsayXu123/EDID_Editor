
def encode_manufacturer_id(manufacturer: str) -> bytes:
    """
    Convert a 3-letter manufacturer ID into 2 encoded bytes
    """
    if len(manufacturer) != 3 or not manufacturer.isalpha():
        raise ValueError("Manufacturer ID must be 3 alphabetic characters.")
    
    manufacturer = manufacturer.upper()
    b1 = ((ord(manufacturer[0]) - 64) << 2) | ((ord(manufacturer[1]) - 64) >> 3)
    b2 = (((ord(manufacturer[1]) - 64) & 0x07) << 5) | (ord(manufacturer[2]) - 64)
    return bytes([b1, b2])


def encode_product_id(product_id: int) -> bytes:
    """
    Convert product ID (int) to 2 bytes in little endian format.
    """
    if not (0 <= product_id <= 0xFFFF):
        raise ValueError("Product ID must be a 16-bit unsigned integer.")
    return product_id.to_bytes(2, byteorder='little')


def encode_serial_number(serial: int) -> bytes:
    """
    Convert serial number (int) to 4 bytes in little endian format.
    """
    if not (0 <= serial <= 0xFFFFFFFF):
        raise ValueError("Serial number must be a 32-bit unsigned integer.")
    return serial.to_bytes(4, byteorder='little')


def encode_manufacture_date(week: int, year: int) -> tuple[int, int]:
    """
    Convert manufacture week and year into EDID-compatible values.
    """
    if not (1 <= week <= 53):
        raise ValueError("Invalid week")
    if not (1990 <= year <= 254 + 1990):
        raise ValueError("Invalid year")
    return week, year - 1990


def calculate_checksum(edid_data: bytearray) -> int:
    """
    Calculate EDID checksum (last byte such that sum of 128 bytes == 0 mod 256).
    """
    if len(edid_data) != 128:
        raise ValueError("EDID data must be 128 bytes")
    checksum = (256 - (sum(edid_data[:127]) % 256)) % 256
    return checksum