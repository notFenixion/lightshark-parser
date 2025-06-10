import logging

def _read_attribute_name(file_bytes: bytes, ptr: int, valid_attributes: list, section_name: str) -> tuple[str, int]:

    attr_name_len = file_bytes[ptr] - 0xA0
    attr_name = file_bytes[ptr+1:ptr+1+attr_name_len].decode('utf-8')
    # logging.debug(hex(file_bytes[ptr]))
    assert attr_name in valid_attributes, f"Error: Attribute '{attr_name}' is not a valid {section_name} attribute / Attribute length byte ({attr_name_len}) is incorrect"
    return attr_name, ptr + attr_name_len + 1


def _read_byte_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    """I don't think these go beyond 255 in normal circumstances"""
    obj[attr_name] = file_bytes[ptr]
    return ptr + 1

def _read_boolean_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    assert file_bytes[ptr] in [0xC2, 0xC3], f"Error: {attr_name} value is not a boolean (0xC2 or 0xC3)"
    obj[attr_name] = file_bytes[ptr] == 0xC3
    return ptr + 1

def _read_string_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    str_len = file_bytes[ptr] - 0xA0
    obj[attr_name] = file_bytes[ptr+1:ptr+1+str_len].decode('utf-8')
    return ptr + 1 + str_len

def _read_list_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    num_items = file_bytes[ptr] - 0x90
    obj[attr_name] = []
    ptr += 1
    for i in range(num_items):
        obj[attr_name].append(file_bytes[ptr])
        ptr += 1
    return ptr


def _obj_bytelength_check(initial_ptr: int, ptr: int, obj_bytelength: int, num_attr: int, num_attr_indicated: int):
    logging.debug("Current ptr: %s, Initial+indicated: %s", ptr, initial_ptr + obj_bytelength)
    assert initial_ptr + obj_bytelength == ptr, "Error: object bytelength indicated does not match actual object bytelength"
    logging.debug("Number of attributes: %s, Indicated: %s", num_attr, num_attr_indicated)
    assert num_attr == num_attr_indicated, "Error: number of attributes does not match expected number of attributes" 