import logging
from .attribute_parsers import (
    _read_byte_attribute, _read_boolean_attribute, _read_string_attribute,
    _read_list_attribute, _obj_bytelength_check, _read_attribute_name
)
from ..classes import Order


def _init_object_reading(file_bytes: bytes, ptr: int, expected_marker: bytes) -> tuple[int, int, int, int]:
    byte_length = int.from_bytes(file_bytes[ptr:ptr+4], 'big')
    initial_ptr = ptr + 4
    logging.debug(file_bytes[initial_ptr-50:initial_ptr+len(expected_marker)+50])

    assert file_bytes[initial_ptr:initial_ptr+len(expected_marker)] == expected_marker, f"Marker {expected_marker!r} not found at expected position"
    num_attr_indicated = file_bytes[initial_ptr+len(expected_marker)-1]
    # Subtract 0x80 is the usual. Only for patches is the num_attr value 0x10 for god knows what reason
    if num_attr_indicated > 0x80: num_attr_indicated -= 0x80 
    ptr = initial_ptr + len(expected_marker)
    # logging.debug(f"Number of attributes indicated: {num_attr_indicated}")

    return byte_length, initial_ptr, num_attr_indicated, ptr
    


def read_patch(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    patch = {}
    patch_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr, b'\xde\x00\x10')

    # Start reading attributes
    attributes = ['model_id', 'inverse_tilt', 'name', 'channels_ftype', 'index', 'universe', 'description', 'inverse_pan', 'visual_id', 'parked', 'color_mark', 'dimmer', 'swap_pan_tilt', 'virtual_dimmer', 'id', 'size']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'patch')

        
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
    group_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr, b'\x88')

    attributes = ['description', 'color_mark', 'visual_id', 'patched_elements_ids', 'grid', 'steps', 'automatico', 'group_id']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'group')

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


def read_order(file_bytes: bytes, ptr: int) -> tuple[Order, int]:
    order = {}
    logging.debug(hex(file_bytes[ptr]))
    assert file_bytes[ptr] == 0x88, "Error: Incorrect num. of attributes specified for order in palette"
    ptr += 1
    attributes = ['palette_id', 'universe', 'section', 'receptor_type', 'patch_id', 'ftype', 'value', 'channel']
    num_attr = 0
    while file_bytes[ptr] != 0x88 and num_attr < 8:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'order')

        if attr_name in ['palette_id', 'universe', 'section', 'receptor_type', 'patch_id', 'channel']:
            ptr = _read_byte_attribute(file_bytes, ptr, order, attr_name)
        elif attr_name in ['ftype']:
            ftype_len = 0 if (file_bytes[ptr] == 0xCB or file_bytes[ptr] == 0x00) else 2**(file_bytes[ptr] - 0xCC)
            order[attr_name] = file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8')
            ptr += ftype_len + 1
        elif attr_name in ['value']:
            # If value is >= \xCC, it could be a length indicator for a value that is >255
            # NOTE: Might have edge cases that could cause this to break
            if file_bytes[ptr] <= 0xCB:
                ptr = _read_byte_attribute(file_bytes, ptr, order, attr_name)
            else:
                value_length = 2**(file_bytes[ptr] - 0xCC)
                # First byte is in fact a length byte
                if file_bytes[ptr+1+value_length:ptr+1+value_length+8] == b'\xa7channel':
                    order[attr_name] = int.from_bytes(file_bytes[ptr+1:ptr+1+value_length], 'big')
                    ptr += value_length + 1

                # First byte is just the value and happens to be >= \xCC
                else:
                    #Check for \xA7channel to verify
                    assert file_bytes[ptr+1+value_length:ptr+1+value_length+8] == b'\xa7channel', "Error: Either the channel attribute has been written incorrectly, or something is very wrong... (order -> value)"
                    ptr = _read_byte_attribute(file_bytes, ptr, order, attr_name)       
        else:
            assert False, f"Error: This error shouldnt occur... (order)"
        logging.debug(f"Found attribute {attr_name} with value = {order[attr_name]}")
        num_attr += 1
    missing = [attr for attr in attributes if attr not in order]
    assert not missing, f"Error: Missing or None values for attributes: {missing}"
    order_obj = Order(**order)
    logging.debug("ORDER found: " + str(order_obj.__dict__))
    return order_obj, ptr


def read_user_palette(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    palette = {}
    palette_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr, b'\x84')

    attributes = ['section', 'user_palette_id', 'name', 'orders']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'user_palette')

        if attr_name in ['section', 'user_palette_id']:
            ptr = _read_byte_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name in ['name']:
            ptr = _read_string_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name == 'orders':
            if file_bytes[ptr] > 0x9f:
                assert file_bytes[ptr] == 0xDC, "Error: There is a problem with the indicator for num. of orders in the user_palette."
                num_orders = int.from_bytes(file_bytes[ptr+1:ptr+3], 'big')
                ptr += 3
            else:
                num_orders = file_bytes[ptr] - 0x90
                ptr += 1
            palette[attr_name] = []
            for i in range(num_orders):
                order, ptr = read_order(file_bytes, ptr)
                palette[attr_name].append(order)            
        else:
            assert False, f"Error: This error shouldnt occur... (user_palette)"
        logging.debug(f"Found attribute {attr_name} with value = {palette[attr_name]}")
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, palette_bytelength, num_attr, num_attr_indicated)
    return palette, ptr

    



    