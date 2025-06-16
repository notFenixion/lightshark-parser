import logging
from .attribute_parsers import (
    _read_byte_attribute, _read_boolean_attribute, _read_string_attribute,
    _read_list_attribute, _obj_bytelength_check, _read_attribute_name, _read_obj_list_len, _read_multibyte_attribute
)
from ..classes import Order, FX


def _init_object_reading(file_bytes: bytes, ptr: int, expected_marker: bytes) -> tuple[int, int, int, int]:
    byte_length = int.from_bytes(file_bytes[ptr:ptr+4], 'big')
    initial_ptr = ptr + 4
    # logging.debug("Bytes around current position: %r", file_bytes[initial_ptr-50:initial_ptr+len(expected_marker)+50])

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
        # Complex attributes
        elif attr_name == 'channels_ftype':
            num_channels, ptr = _read_obj_list_len(file_bytes, ptr)
            patch[attr_name] = []
            for _ in range(num_channels):
                # NOTE: this 2^ thing could be wrong
                ftype_len = 0 if file_bytes[ptr] == 0xCB else 2**(file_bytes[ptr] - 0xCC)
                patch[attr_name].append(file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8'))
                ptr += ftype_len + 1
        elif attr_name == 'dimmer':
            #genuinely i have no idea how this one is meant to work
            assert file_bytes[ptr] == 0xCB, "Well this is an unique case i've never seen in patch -> dimmer"
            patch[attr_name] = []
            ptr += 1
            for _ in range(8):
                patch[attr_name].append(file_bytes[ptr])
                ptr += 1
        elif attr_name == 'virtual_dimmer':
            ptr = _read_list_attribute(file_bytes, ptr, patch, attr_name)
        else:
            assert False, f"Error: this error shouldnt occur... (patch)"
        logging.debug("Found attribute %s with value = %s", attr_name, patch[attr_name])
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
            for _ in range(num_fixtures):
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
            for _ in range(num_steps):
                fixture_id = file_bytes[ptr]
                step = file_bytes[ptr+1]
                steps[fixture_id] = step
                ptr += 2
            group[attr_name] = steps
        else:
            assert False, f"Error: This error shouldnt occur... (group)"
        logging.debug("Found attribute %s with value = %s", attr_name, group[attr_name])
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, group_bytelength, num_attr, num_attr_indicated)
    return group, ptr


def read_order(file_bytes: bytes, ptr: int) -> tuple[Order, int]:
    order = {}
    assert file_bytes[ptr] == 0x88, "Error: Incorrect num. of attributes specified for order in palette"
    ptr += 1
    attributes = ['palette_id', 'universe', 'section', 'receptor_type', 'patch_id', 'ftype', 'value', 'channel']
    num_attr_indicated = 8
    num_attr = 0
    while file_bytes[ptr] != 0x88 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'order')

        if attr_name in ['palette_id', 'universe', 'section', 'receptor_type', 'patch_id', 'channel']:
            ptr = _read_byte_attribute(file_bytes, ptr, order, attr_name)
        elif attr_name in ['ftype']:
            ftype_len = 0 if (file_bytes[ptr] == 0xCB or file_bytes[ptr] == 0x00) else 2**(file_bytes[ptr] - 0xCC)
            order[attr_name] = file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8')
            ptr += ftype_len + 1
        elif attr_name in ['value']:
            ptr = _read_multibyte_attribute(file_bytes, ptr, order, attr_name, b'\xa7channel')
        else:
            assert False, f"Error: This error shouldnt occur... (order)"
        logging.debug("Found attribute %s with value = %s", attr_name, order[attr_name])
        num_attr += 1

    missing = [attr for attr in attributes if attr not in order]
    assert not missing, f"Error: Missing or None values for attributes: {missing}"
    assert num_attr == num_attr_indicated, "Error: number of attributes found does not match expected number of attributes for order"
    order_obj = Order(**order)
    logging.info("ORDER FOUND: %s", order_obj.__dict__)
    return order_obj, ptr


def read_user_palette(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    palette = {}
    palette_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr, b'\x84')

    attributes = ['section', 'user_palette_id', 'name', 'orders']
    num_attr_indicated = 4
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'user_palette')

        if attr_name in ['section', 'user_palette_id']:
            ptr = _read_byte_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name in ['name']:
            ptr = _read_string_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name == 'orders':
            num_orders, ptr = _read_obj_list_len(file_bytes, ptr)
            palette[attr_name] = []
            for _ in range(num_orders):
                order, ptr = read_order(file_bytes, ptr)
                palette[attr_name].append(order)            
        else:
            assert False, f"Error: This error shouldnt occur... (user_palette)"
        logging.debug("Found attribute %s with value = %s", attr_name, palette[attr_name])
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, palette_bytelength, num_attr, num_attr_indicated)
    return palette, ptr

def read_fx_layer_steps(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    logging.debug("-" * 40 + " Parsing FX Layer Step " + "-" * 40)
    assert file_bytes[ptr] == 0x8C, "Error: Incorrect num. of attributes specified for step in FX layer"
    ptr += 1
    num_attr_indicated = 12
    num_attr = 0
    step = {}
    attributes = ['start_limit', 'palette_type', 'name', 'ancho', 'curve_in', 'curve_out', 'strength', 'curve_type', 'palette_value', 'inicio', 'end_limit', 'jumps']

    while file_bytes[ptr] != 0x8C and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'step')

        if attr_name in ['palette_type', 'curve_type', 'palette_value', 'jumps']:
            ptr = _read_byte_attribute(file_bytes, ptr, step, attr_name)
        elif attr_name in ['start_limit', 'strength', 'ancho', 'curve_in', 'curve_out', 'strength', 'inicio', 'end_limit']:
            ptr = _read_multibyte_attribute(file_bytes, ptr, step, attr_name)
        elif attr_name in ['name']:
            ptr = _read_string_attribute(file_bytes, ptr, step, attr_name)
        else:
            assert False, f"Error: This error shouldnt occur... (step)"
        logging.debug("Found attribute %s with value = %s", attr_name, step[attr_name])
        num_attr += 1

    assert num_attr == num_attr_indicated, "Error: number of attributes found does not match expected number of attributes for step"
    logging.debug("-" * 40 + " End FX Layer Step " + "-" * 43)
    return step, ptr


def read_fx_layer(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    logging.debug("=" * 45 + " Parsing FX Layer " + "=" * 45)
    assert file_bytes[ptr] == 0x88, "Error: Incorrect num. of attributes specified for layer in FX"
    ptr += 1
    num_attr_indicated = 8
    num_attr = 0
    layer = {}
    attributes = ['blind', 'phase_offset', 'section', 'curve', 'steps', 'ftypes', 'id', 'size']

    while file_bytes[ptr] != 0x88 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'layer')

        if attr_name in ['section', 'id']:
            ptr = _read_byte_attribute(file_bytes, ptr, layer, attr_name)
        elif attr_name in ['blind']:
            ptr = _read_boolean_attribute(file_bytes, ptr, layer, attr_name)
        elif attr_name in ['phase_offset', 'curve', 'size']:
            ptr = _read_multibyte_attribute(file_bytes, ptr, layer, attr_name)\
        
        # Complex attributes
        elif attr_name == 'steps':
            num_steps, ptr = _read_obj_list_len(file_bytes, ptr)
            layer[attr_name] = []
            for _ in range(num_steps):
                step, ptr = read_fx_layer_steps(file_bytes, ptr)
                step_obj = FX.FXLayerStep(**step)
                layer[attr_name].append(step_obj)

        elif attr_name == 'ftypes':
            num_ftypes, ptr = _read_obj_list_len(file_bytes, ptr)
            layer[attr_name] = []
            for _ in range(num_ftypes):
                ftype_len = 0 if file_bytes[ptr] == 0xCB else 2**(file_bytes[ptr] - 0xCC)
                layer[attr_name].append(file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8'))
                ptr += ftype_len + 1
        else:
            assert False, f"Error: This error shouldnt occur... (layer)"
        logging.debug("Found attribute %s with value = %s", attr_name, layer[attr_name])
        num_attr += 1

    assert num_attr == num_attr_indicated, "Error: number of attributes found does not match expected number of attributes for layer"
    logging.debug("=" * 45 + " End FX Layer " + "=" * 48)
    return layer, ptr

def read_fx(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    fx = {}
    #NOTE: different from the usual init_object_reading
    expected_marker = b'\xde\x00\x18'
    assert file_bytes[ptr:ptr+3] == expected_marker, f"Error: Marker {expected_marker!r} not found for FX"
    num_attr_indicated = int.from_bytes(file_bytes[ptr+1:ptr+3], 'big')
    ptr += 3
    attributes = [
        'cyclos', 'direction', 'speed', 'group_steps', 'size', 'layers', 
        'patches', 'speed_in_bpm', 'width', 'spread', 'basic', 'gfxid', 
        'internal_speed', 'fx_ref', 'splits', 'groups', 'rect_width', 
        'name', 'phase_offset', 'bpm', 'render_id', 'mode', 'repeats', 
        'rect_height'
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'fx')

        if attr_name in ['cyclos', 'direction', 'group_steps', 'gfxid', 'splits', 'rect_width', 'render_id', 'mode', 'repeats', 'rect_height']:
            ptr = _read_byte_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ['speed', 'size', 'width', 'spread', 'internal_speed', 'fx_ref', 'phase_offset', 'bpm']:
            ptr = _read_multibyte_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name == 'name':
            ptr = _read_string_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ['speed_in_bpm', 'basic']:
            ptr = _read_boolean_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ['patches', 'groups']:
            ptr = _read_list_attribute(file_bytes, ptr, fx, attr_name)
                
        # Complex attributes
        elif attr_name == 'layers':
            num_layers, ptr = _read_obj_list_len(file_bytes, ptr)
            fx[attr_name] = []
            for _ in range(num_layers):
                layer, ptr = read_fx_layer(file_bytes, ptr)
                layer_obj = FX.FXLayer(**layer)
                fx[attr_name].append(layer_obj)
        else:
            assert False, f"Error: Unhandled attribute '{attr_name}' in FX"
        logging.debug("Found attribute %s with value = %s", attr_name, fx[attr_name])
        num_attr += 1

    assert num_attr == num_attr_indicated, "Error: number of attributes does not match expected number of attributes for FX"
    return fx, ptr


def read_cue(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    cue = {}
    cue_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr, b'\x87')
    attributes = ['fx_palette', 'cue_id', 'visual_id', 'fxs', 'fxs_channels', 'orders', 'name']
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, 'cue')

        if attr_name in ['fx_palette', 'cue_id', 'visualid']:
            ptr = _read_byte_attribute(file_bytes, ptr, cue, attr_name)
        elif attr_name in ['visual_id']:
            ptr = _read_multibyte_attribute(file_bytes, ptr, cue, attr_name)
        elif attr_name in ['name']:
            ptr = _read_string_attribute(file_bytes, ptr, cue, attr_name)

        elif attr_name == 'fxs':
            num_fxs, ptr = _read_obj_list_len(file_bytes, ptr)
            cue[attr_name] = []
            for _ in range(num_fxs):
                fx, ptr = read_fx(file_bytes, ptr)
                fx_obj = FX(**fx)
                cue[attr_name].append(fx_obj)

        elif attr_name == 'fxs_channels':
            num_channels, ptr = _read_obj_list_len(file_bytes, ptr)
            cue[attr_name] = []
            for _ in range(num_channels):
                channel_len, ptr = _read_obj_list_len(file_bytes, ptr)
                channel = []
                i = 0
                # NOTE: some of the channel instances have:
                # \xD1 FF at the 11th channel's index and it doesn't count towards the channel_len for some reason?
                # \xCD multibyte values (these count towards channel_len)
                # will fix once I figure this out
                while i < channel_len:
                    # probably deleted? idk
                    if file_bytes[ptr:ptr+2] == b'\xd1\xff':
                        channel.append(file_bytes[ptr:ptr+2])
                        ptr += 2
                    else:
                        temp = {}
                        ptr = _read_multibyte_attribute(file_bytes, ptr, temp, 'channel')
                        channel.append(temp['channel'])
                        i += 1
                cue[attr_name].append(channel)

        elif attr_name == 'orders':
            num_orders, ptr = _read_obj_list_len(file_bytes, ptr)
            logging.debug("Number of orders: %d", num_orders)
            cue[attr_name] = []
            for _ in range(num_orders):
                order_obj, ptr = read_order(file_bytes, ptr)
                cue[attr_name].append(order_obj)            
        else:
            assert False, f"Error: This error shouldnt occur... (cue)"
        logging.debug("Found attribute %s with value = %s", attr_name, cue[attr_name])
        num_attr += 1

    _obj_bytelength_check(initial_ptr, ptr, cue_bytelength, num_attr, num_attr_indicated)
    return cue, ptr


def read_cuelist(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    cuelist = {}
    
def read_playback(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    playback = {}

def read_general(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    general = {}