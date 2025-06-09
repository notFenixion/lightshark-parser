import logging
import sys
from .classes import Lightshow, Patch, Group
from .utils.json_encoder import CompactJSONEncoder



def read_file_bytes(file_path):
    if not file_path.lower().endswith('.lshw'):
        print("Error: File must have be of extension .lshw", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when accessing '{file_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

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


def read_patch(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    patch = {}
    patch_bytelength = int.from_bytes(file_bytes[ptr+10:ptr+14], 'big')
    initial_ptr = ptr+14
    assert file_bytes[ptr+14:ptr+17] == b'\xde\x00\x10', "xDE0010 not spotted at the right location of patch :("
    num_attr_indicated = file_bytes[ptr+16]
    ptr += 17

    # Start reading attributes
    logging.debug(file_bytes[ptr:ptr+1])
    attributes = ['model_id', 'inverse_tilt', 'name', 'channels_ftype', 'index', 'universe', 'description', 'inverse_pan', 'visual_id', 'parked', 'color_mark', 'dimmer', 'swap_pan_tilt', 'virtual_dimmer', 'id', 'size']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name_len = file_bytes[ptr] - 0xA0
        attr_name = file_bytes[ptr+1:ptr+attr_name_len+1].decode('utf-8')
        assert attr_name in attributes, f"Error: Attribute {attr_name} is not a patch attribute / Attribute length byte ({attr_name_len}) is incorrect"
        ptr += attr_name_len + 1

        
        if attr_name in ['model_id', 'index', 'universe', 'visual_id', 'color_mark', 'id', 'size']:
            ptr = _read_byte_attribute(file_bytes, ptr, patch, attr_name)
        elif attr_name in ['inverse_tilt', 'inverse_pan', 'parked', 'swap_pan_tilt']:
            ptr = _read_boolean_attribute(file_bytes, ptr, patch, attr_name)
        elif attr_name in ['name', 'description']:
            ptr = _read_string_attribute(file_bytes, ptr, patch, attr_name)
        #Unique cases
        elif attr_name == 'channels_ftype':
            num_channels = file_bytes[ptr] - 0x90
            patch[attr_name] = []
            ptr += 1
            for i in range(num_channels):
                # NOTE: this 2^ thing could be wrong
                ftype_len = 0 if file_bytes[ptr] == 0xCB else 2**(file_bytes[ptr] - 0xCC)
                patch[attr_name].append(file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8'))
                ptr += ftype_len + 1
        elif attr_name == 'dimmer':
            #genuinely i have no idea how this one is meant to work
            assert file_bytes[ptr] == 0xCB, "Well this is an unique case i've never seen in patch -> dimmer"
            patch[attr_name] = []
            ptr += 1
            for i in range(8):
                patch[attr_name].append(file_bytes[ptr])
                ptr += 1
        elif attr_name == 'virtual_dimmer':
            ptr = _read_list_attribute(file_bytes, ptr, patch, attr_name)
        else:
            assert False, f"Error: this error shouldnt occur... (patch)"
        logging.debug(f"Found attribute {attr_name} with value = {patch[attr_name]}")
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, patch_bytelength, num_attr, num_attr_indicated)
    return patch, ptr

def read_group(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    group = {}
    group_bytelength = int.from_bytes(file_bytes[ptr+10:ptr+14], 'big')
    initial_ptr = ptr+14
    assert file_bytes[ptr+14] == 0x88, "x88 not spotted at the right location of group :("
    num_attr_indicated = file_bytes[ptr+14] - 0x80
    ptr += 15

    attributes = ['description', 'color_mark', 'visual_id', 'patched_elements_ids', 'grid', 'steps', 'automatico', 'group_id']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name_len = file_bytes[ptr] - 0xA0
        attr_name = file_bytes[ptr+1:ptr+attr_name_len+1].decode('utf-8')
        # logging.debug(f"Attribute name bytes: {file_bytes[ptr+1:ptr+1+attr_name_len].hex()}, length byte: 0x{file_bytes[ptr]:02x}, calculated length: {attr_name_len}")
        assert attr_name in attributes, f"Error: Attribute {attr_name} is not a group attribute / Attribute length byte ({attr_name_len}) is incorrect"
        ptr += attr_name_len + 1

        if attr_name in ['color_mark', 'visual_id', 'group_id']:
            ptr = _read_byte_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name in ['description']:
            ptr = _read_string_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name in ['automatico']:
            ptr = _read_boolean_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name == 'patched_elements_ids':
            ptr = _read_list_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name == 'grid':
            grid = {}
            num_fixtures = file_bytes[ptr] - 0x80
            ptr += 1
            for i in range(num_fixtures):
                fixture_id = file_bytes[ptr]
                assert file_bytes[ptr+1] == 0x92, "Error: This error shouldnt occur... (group -> grid)"
                fixture_x = file_bytes[ptr+2]
                fixture_y = file_bytes[ptr+3]
                grid[fixture_id] = (fixture_x, fixture_y)
                ptr += 4
            group[attr_name] = grid
        elif attr_name == 'steps':
            steps = {}
            num_steps = file_bytes[ptr] - 0x80
            ptr += 1
            for i in range(num_steps):
                fixture_id = file_bytes[ptr]
                step = file_bytes[ptr+1]
                steps[fixture_id] = step
                ptr += 2
            group[attr_name] = steps
        else:
            assert False, f"Error: This error shouldnt occur... (group)"
        logging.debug(f"Found attribute {attr_name} with value = {group[attr_name]}")
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, group_bytelength, num_attr, num_attr_indicated)
    return group, ptr


def parse_file_bytes(file_bytes):
    '''
    TODO For user palettes:
    1. Find xAF #user_palettes#
    2. For each palette:
        2a. Find instance of x00 00 00 0D AC user_palette to start with. (same 4 bytes in 2d btw)
        2b. Read the next (4 bytes' value) bytes worth, feed into parse_user_palette
        2c. create OrderPalettes and feed them into UserPalette as well
        2d. Read next 4 bytes. if ends with x07 instead of x0D, signifies end of user_palettes. else signifies start of next user_palette
    3. yay done, now store into Lightshow via add_user_palette
    4. repeat for all user palettes 

    NOTE: add a bunch of asserts inbetween to ensure that the x98 88 and whatnot are working fine
    2nd NOTE: i think u can kinda do this for the rest of the main sections tbh
    '''
    # Find all instances of xCD + 2 bytes + xCC pattern
    # cd_cc_pattern = re.compile(b'\xCD..\xCC')
    # cd_cc_matches = [match.start() for match in cd_cc_pattern.finditer(file_bytes)]
    # if cd_cc_matches:
    #     print(f"Found {len(cd_cc_matches)} instances of xCD + 2 bytes + xCC at positions: {cd_cc_matches}")
    #     # Display the bytes in both hex and ASCII
    #     bytes_to_show = file_bytes[cd_cc_matches[-1]-50:cd_cc_matches[-1]+50]
    #     hex_str = ' '.join(f'{b:02x}' for b in bytes_to_show)
    #     # Create ASCII representation, replacing non-printable chars with '.'
    #     ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes_to_show)
    #     print("Hex:", hex_str)
    #     print("ASCII:", ascii_str)
    # else:
    #     print("No instances of xCD + 2 bytes + xCC found")
    patching = {} # Key: patch ID, Value: Patch object
    groups = {} # Key: group ID, Value: Group object
    user_palettes = {}


    # Initial search for #patching# section
    # NOTE THAT THIS IS TEMPORARY AND WILL BE REMOVED ONCE FILEINFO + MODEL ARE ADDED. #patching# assert will be kept.
    ptr = file_bytes.find(b'\xAA#patching#')
    assert ptr != -1, "Could not find #patching# in file"
    logging.debug(f"Found #patching# at index {ptr}")
    ptr += 11
    logging.debug(file_bytes[ptr:ptr+10])

    ## PATCHES ##
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5patch':
        patch, ptr = read_patch(file_bytes, ptr)
        patch_obj = Patch(**patch)
        patching[patch_obj.id] = patch_obj  # Use id as dictionary key
        logging.debug("FOUND PATCH: " + str(patch_obj.__dict__) + "\n" + "-" * 80)
    if not patching:  # Check if dictionary is empty
        logging.warning("No patches found in file. This warning is only a concern if there are patches in your show but none were detected.")

    ## GROUPS ##
    logging.debug("Finished reading patches. Moving onto groups...")
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5group':
        group, ptr = read_group(file_bytes, ptr)
        group_obj = Group(**group)
        groups[group_obj.group_id] = group_obj  # Use group_id as dictionary key
        logging.debug("FOUND GROUP: " + str(group_obj.__dict__) + "\n" + "-" * 80)
    if not groups:  # Check if dictionary is empty
        logging.warning("No groups found in file. This warning is only a concern if there are groups in your show but none were detected.")

    return Lightshow(
        patches=patching,
        groups=groups,
    )




