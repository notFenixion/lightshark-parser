import math

def serialise_section_header(section_name: str) -> bytes:
    return (
        (len(section_name)+1).to_bytes(4, "big") +
        (len(section_name) + 0xA0).to_bytes(1, "big") +
        section_name.encode("utf-8")
    )

def serialise_attr_name(attr_name: str) -> bytes:
    return (len(attr_name) + 0xA0).to_bytes(1, "big") + attr_name.encode("utf-8")

def serialise_num_attr(num_attr: int) -> bytes:
    if num_attr < 16:
        return (num_attr + 0x80).to_bytes(1, "big")
    else:
        return (0xDE).to_bytes(1, "big") + num_attr.to_bytes(2, "big")

def serialise_num_value(num_value: int, cc_check: bool = False) -> bytes:
    # NOTE: threshold unconfirmed
    threshold = 0x79 if cc_check else 0xFF
    if num_value <= threshold:
        return num_value.to_bytes(1, "big")
    else:
        num_bytes = 1 << (math.ceil(num_value.bit_length() / 8) - 1).bit_length()
        return (0xCC + int(math.log(num_bytes,2))).to_bytes(1, "big") + num_value.to_bytes(num_bytes, "big")

def serialise_bool_value(bool_value: bool) -> bytes:
    return (0xC3 if bool_value else 0xC2).to_bytes(1, "big")

def serialise_str_value(str_value: str) -> bytes:
    encoded = str_value.encode("utf-8")
    byte_len = len(encoded)
    if byte_len < 32:  # 0xA0 + len < 0xC0
        return (byte_len + 0xA0).to_bytes(1, "big") + encoded
    else:
        # For longer strings, use 0xDA followed by 2-byte length
        return (0xDA).to_bytes(1, "big") + byte_len.to_bytes(2, "big") + encoded


def serialise_objlist_len(objlist_len: int) -> bytes:

    if objlist_len < 16:
        return (objlist_len + 0x90).to_bytes(1, "big")
    else:
        return (0xDC).to_bytes(1, "big") + objlist_len.to_bytes(2, "big")


def serialise_num_list(list_value: list[int], cc_check: bool = False) -> bytes:
    bytestr = bytearray()
    list_len = len(list_value)
    bytestr.extend(serialise_objlist_len(list_len))
    for value in list_value:
        bytestr.extend(serialise_num_value(value, cc_check))
    return bytes(bytestr)
    
def serialise_bool_list(list_value: list[bool]) -> bytes:
    bytestr = bytearray()
    list_len = len(list_value)
    bytestr.extend(serialise_objlist_len(list_len))
    for value in list_value:
        bytestr.extend(serialise_bool_value(value))
    return bytes(bytestr)

def serialise_content_length(content: bytes) -> bytes:
    return (len(content)).to_bytes(4, "big")