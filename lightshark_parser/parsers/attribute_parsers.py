import logging

from ..utils.custom_errors import MarkerNotFoundError


def _read_attribute_name(file_bytes: bytes, ptr: int, valid_attributes: list, section_name: str, obj_dict: dict) -> tuple[str, int]:
    attr_name_len = file_bytes[ptr] - 0xA0
    if attr_name_len <= 0 or ptr + 1 + attr_name_len > len(file_bytes):
        raise ValueError(f"Invalid attribute name length {attr_name_len} at position {ptr} from value {hex(file_bytes[ptr])}")

    attr_name = file_bytes[ptr + 1 : ptr + 1 + attr_name_len].decode("utf-8")

    if attr_name not in valid_attributes:
        raise ValueError(f"Attribute '{attr_name}' is not a valid {section_name} attribute. Expected one of: {valid_attributes}")
    
    if attr_name in obj_dict:
        raise AttributeError(f"Duplicate instance of attribute '{attr_name}' found in {section_name}")
        
    return attr_name, ptr + attr_name_len + 1


# Global set to store unique markers
_unique_markers = set()

def _write_markers_to_file():
    if _unique_markers:
        with open('cc_markers_log.txt', 'a') as f:
            for marker_info in sorted(_unique_markers):
                f.write(f"{marker_info}\n")
            f.write("-"*80 + "\n")

def _read_number(file_bytes: bytes, ptr: int, attribute: str) -> tuple[int, int]:
    if file_bytes[ptr] <= 0xCB or file_bytes[ptr] > 0xCE:
        return file_bytes[ptr], ptr + 1
    else:
        # marker = file_bytes[ptr]
        # marker_hex = f"0x{marker:02X}"
        # marker_info = f"Found {marker_hex} marker in _read_number for '{attribute}'"
        # _unique_markers.add(marker_info)
        value_length = 2 ** (file_bytes[ptr] - 0xCC)
        value = int.from_bytes(file_bytes[ptr + 1 : ptr + 1 + value_length], "big")
        return value, ptr + value_length + 1


def _read_number_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str, check: bytes = None, obj_name: str = None) -> int:
    # If value is >= \xCC, it could be a length indicator for a value that is >255
    # NOTE: Might have edge cases that could cause this to break
    if file_bytes[ptr] <= 0xCB or file_bytes[ptr] > 0xCE:
        obj[attr_name] = file_bytes[ptr]
        return ptr + 1
    else:
        # Get the variable name from the calling frame's local variables
        # import inspect
        # frame = inspect.currentframe().f_back
        # try:
        #     # Look for the variable name in the caller's locals
        #     for name, value in frame.f_locals.items():
        #         if value is obj:
        #             obj_name = name
        #             break
        #     else:
        #         obj_name = 'unknown_dict'
        # finally:
        #     del frame  # Avoid reference cycles
        
        # marker = file_bytes[ptr]
        # marker_hex = f"0x{marker:02X}"
        # marker_info = f"Found {marker_hex} marker in dict '{obj_name}', attribute: {attr_name}"
        # _unique_markers.add(marker_info)
        
        value_length = 2 ** (file_bytes[ptr] - 0xCC)
        # If no check given assume that multibyte is correct
        if check is None:
            obj[attr_name] = int.from_bytes(file_bytes[ptr + 1 : ptr + 1 + value_length], "big")
            return ptr + value_length + 1
        else:
            # Check if the bytes after match check. If they don't then it's likely that value just happened to be >= \xCC
            if file_bytes[ptr + 1 + value_length : ptr + 1 + value_length + len(check)] == check:
                obj[attr_name] = int.from_bytes(file_bytes[ptr + 1 : ptr + 1 + value_length], "big")
                return ptr + value_length + 1
            else:
                # Single byte case
                obj[attr_name] = file_bytes[ptr]
                ptr += 1
                if file_bytes[ptr + 1 + value_length : ptr + 1 + value_length + len(check)] != check:
                    raise ValueError("Error reading number attribute")
                return ptr


def _read_boolean_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    if file_bytes[ptr] not in [0xC2, 0xC3]:
        raise ValueError(f"{attr_name} value is not a boolean. Expected 0xC2 (False) or 0xC3 (True), got {hex(file_bytes[ptr])}")
    obj[attr_name] = file_bytes[ptr] == 0xC3
    return ptr + 1


def _read_string_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str) -> int:
    if file_bytes[ptr] < 0xDA:
        str_len = file_bytes[ptr] - 0xA0
        if str_len < 0 or ptr + 1 + str_len > len(file_bytes):
            raise ValueError(f"Invalid string length {str_len} at position {ptr} from value {hex(file_bytes[ptr])}")
        obj[attr_name] = file_bytes[ptr + 1 : ptr + 1 + str_len].decode("utf-8")
        return ptr + 1 + str_len
    # Case where xDA + 2 bytes for length
    else:
        print("String attribute length indicator %s found at position %d", hex(file_bytes[ptr]), ptr)
        if file_bytes[ptr] != 0xDA:
            raise ValueError(f"Invalid string attribute length indicator. Expected 0xDA, got {hex(file_bytes[ptr])}")
        if ptr + 3 > len(file_bytes):
            raise ValueError("Unexpected end of file while reading string length")
        str_len = int.from_bytes(file_bytes[ptr + 1 : ptr + 3], "big")
        if ptr + 3 + str_len > len(file_bytes):
            raise ValueError(f"String length {str_len} exceeds file bounds at position {ptr}")
        obj[attr_name] = file_bytes[ptr + 3 : ptr + 3 + str_len].decode("utf-8")
        return ptr + 3 + str_len


def _read_obj_list_len(file_bytes: bytes, ptr: int) -> tuple[int, int]:
    if ptr >= len(file_bytes):
        raise ValueError("Unexpected end of file while reading object list length")

    if file_bytes[ptr] > 0x9F:
        if file_bytes[ptr] not in [0xDC, 0xDE]:
            raise MarkerNotFoundError(f"Marker 0xDC or 0xDE expected, found {hex(file_bytes[ptr])} instead")
        # Read 2 bytes for value
        length = int.from_bytes(file_bytes[ptr + 1 : ptr + 3], "big")
        if length < 0:
            raise ValueError(f"Invalid list length {length} at position {ptr}")
        return length, ptr + 3
    elif 0x80 <= file_bytes[ptr] and file_bytes[ptr] <= 0x8F:
        length = file_bytes[ptr] - 0x80
        if length < 0:
            raise ValueError(f"Invalid list length {length} at position {ptr} from value {hex(file_bytes[ptr])}")
        return length, ptr + 1
    elif 0x90 <= file_bytes[ptr] and file_bytes[ptr] <= 0x9F:
        length = file_bytes[ptr] - 0x90  # For small lists, length is stored as 0x90 + length
        if length < 0:
            raise ValueError(f"Invalid list length {length} at position {ptr} from value {hex(file_bytes[ptr])}")
        return length, ptr + 1
    else:
        raise ValueError(f"Invalid list length indicator. Expected 0x80-0x8F (or 0xDE), or 0x90-0x9F (or 0xDC), got {hex(file_bytes[ptr])}")


def _read_list_attribute(file_bytes: bytes, ptr: int, obj: dict, attr_name: str, attribute_type: str = "byte") -> int:
    # Use _read_obj_list_len to handle both small (0x90-0x9F) and large (0xDC/0xDE) list lengths
    num_items, ptr = _read_obj_list_len(file_bytes, ptr)
    obj[attr_name] = []
    for _ in range(num_items):
        if ptr >= len(file_bytes):
            raise ValueError(f"Unexpected end of file while reading list item at position {ptr}")

        temp = {}
        try:
            if attribute_type == "bool":
                ptr = _read_boolean_attribute(file_bytes, ptr, temp, "temp")
                obj[attr_name].append(temp["temp"])
            elif attribute_type == "byte":
                ptr = _read_number_attribute(file_bytes, ptr, temp, "temp")
                obj[attr_name].append(temp["temp"])
            else:
                raise ValueError(f"Unsupported attribute_type: {attribute_type}")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error reading list item: {str(e)}") from e

    return ptr


def _obj_checker(initial_ptr: int, ptr: int, obj_bytelength: int, num_attr: int, num_attr_indicated: int):
    logging.debug("Current pointer: %s, Expected end: %s", ptr, initial_ptr + obj_bytelength)
    if initial_ptr + obj_bytelength != ptr:
        raise ValueError(f"Object bytelength mismatch. Expected end at {initial_ptr + obj_bytelength}, but reached {ptr}")
    logging.debug("Number of attributes found: %d, Expected: %d", num_attr, num_attr_indicated)
    if num_attr != num_attr_indicated:
        raise ValueError(f"Attribute count mismatch. Found {num_attr} attributes, expected {num_attr_indicated}")


# Register the function to be called on program exit
import atexit
atexit.register(_write_markers_to_file)
