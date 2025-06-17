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

def _read_multibyte_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str, check: bytes = None) -> int:
    # If value is >= \xCC, it could be a length indicator for a value that is >255
    # NOTE: Might have edge cases that could cause this to break
    if file_bytes[ptr] <= 0xCB:
        return _read_byte_attribute(file_bytes, ptr, obj, attr_name)
    else:
        value_length = 2**(file_bytes[ptr] - 0xCC)
        # If no check given assume that multibyte is correct
        if check is None:
            obj[attr_name] = int.from_bytes(file_bytes[ptr+1:ptr+1+value_length], 'big')
            return ptr + value_length + 1
        else:
            #Check if the bytes after match check. If they don't then it's likely that value just happened to be >= \xCC
            if file_bytes[ptr+1+value_length:ptr+1+value_length+len(check)] == check:
                obj[attr_name] = int.from_bytes(file_bytes[ptr+1:ptr+1+value_length], 'big')
                return ptr + value_length + 1
            else:
                #Single byte case
                ptr = _read_byte_attribute(file_bytes, ptr, obj, attr_name)
                assert file_bytes[ptr+1+value_length:ptr+1+value_length+len(check)] == check, "Error reading multibyte value attribute"
                return ptr
def _read_boolean_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    assert file_bytes[ptr] in [0xC2, 0xC3], f"Error: {attr_name} value is not a boolean (0xC2 or 0xC3)"
    obj[attr_name] = file_bytes[ptr] == 0xC3
    return ptr + 1

def _read_string_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    str_len = file_bytes[ptr] - 0xA0
    obj[attr_name] = file_bytes[ptr+1:ptr+1+str_len].decode('utf-8')
    return ptr + 1 + str_len

def _read_obj_list_len(file_bytes: bytes, ptr: int) -> tuple[int, int]:
    if file_bytes[ptr] > 0x9f:
        assert file_bytes[ptr] in [0xDC, 0xDE], "Error: Invalid list length indicator"
        # logging.debug("List Length starting byte: " + hex(file_bytes[ptr]))
        # Read 2 bytes for value
        length = int.from_bytes(file_bytes[ptr+1:ptr+3], 'big')
        return length, ptr + 3
    else:
        length = file_bytes[ptr] - 0x90  # For small lists, length is stored as 0x90 + length
        return length, ptr + 1


def _read_list_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str, attribute_type: str = "byte") -> int:
    num_items = file_bytes[ptr] - 0x90
    obj[attr_name] = []
    ptr += 1
    for _ in range(num_items):
        if attribute_type == "bool":
            # Convert byte to boolean (0x00 = False, anything else = True)
            assert file_bytes[ptr] in [0xC2, 0xC3], "Byte found in list does not correspond to True/False"
            obj[attr_name].append(file_bytes[ptr] == 0xC3)
        elif attribute_type == "byte":
            obj[attr_name].append(file_bytes[ptr])
        else:
            raise ValueError(f"Unsupported attribute_type: {attribute_type}")
        ptr += 1
    return ptr


def _obj_checker(initial_ptr: int, ptr: int, obj_bytelength: int, num_attr: int, num_attr_indicated: int):
    logging.debug("Current pointer: %s, Expected end: %s", ptr, initial_ptr + obj_bytelength)
    assert initial_ptr + obj_bytelength == ptr, "Error: object bytelength indicated does not match actual object bytelength"
    logging.debug("Number of attributes found: %d, Expected: %d", num_attr, num_attr_indicated)
    assert num_attr == num_attr_indicated, "Error: number of attributes does not match expected number of attributes" 