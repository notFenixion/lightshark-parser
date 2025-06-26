from __future__ import annotations
import logging
from lightshark_parser.parsers.attribute_parsers import (
    _read_boolean_attribute,
    _read_string_attribute,
    _read_list_attribute,
    _obj_checker,
    _read_attribute_name,
    _read_obj_list_len,
    _read_number_attribute,
    _read_number
)
from lightshark_parser.utils.custom_errors import MarkerNotFoundError
from lightshark_parser.classes import (
    FileInfo, Model, ModelPalette, ModelHardware, ModelValue, ModelValueStep, Macro, MacroStep, Patch, Group, UserPalette, Cue, Order, FX, FXLayer, FXLayerStep, FXPalette,
    Cuelist, CuelistElement, Playback, General, Action
)


def _init_object_reading(file_bytes: bytes, ptr: int) -> tuple[int, int, int, int]:
    if ptr + 4 > len(file_bytes):
        raise ValueError(f"Unexpected end of file while reading object header at position {ptr}")

    byte_length = int.from_bytes(file_bytes[ptr : ptr + 4], "big")
    if byte_length <= 0:
        raise ValueError(f"Invalid object length {byte_length} at position {ptr}")

    initial_ptr = ptr + 4
    if file_bytes[initial_ptr] == 0xDE:
        num_attr_indicated = int.from_bytes(file_bytes[initial_ptr + 1 : initial_ptr + 3], "big")
        ptr = initial_ptr + 3
    else:
        num_attr_indicated = file_bytes[initial_ptr] - 0x80
        ptr = initial_ptr + 1

    return byte_length, initial_ptr, num_attr_indicated, ptr


#### FILEINFO ####

def read_version(file_bytes: bytes, ptr: int) -> tuple[FileInfo.Version, int]:
    version = {}
    if file_bytes[ptr : ptr + 12] != b"\x00\x00\x00\x08\xa7version":
        raise MarkerNotFoundError("Could not find version marker in file")
    ptr += 12
    version_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = [
        "subversion",
        "version",
        "autoload",
        "software",
    ]

    num_attr = 0
    while num_attr < num_attr_indicated and file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "version", version)
        
        if attr_name in ["subversion", "version",]:
            ptr = _read_number_attribute(file_bytes, ptr, version, attr_name)
        elif attr_name in ["autoload"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, version, attr_name)
        elif attr_name in ["software"]:
            ptr = _read_string_attribute(file_bytes, ptr, version, attr_name)
        else:
            raise AttributeError("Unexpected error occurred while processing version")

        logging.debug("Found attribute %s with value = %s", attr_name, version[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, version_bytelength, num_attr, num_attr_indicated)
    return FileInfo.Version(**version), ptr


def read_fileinfo(file_bytes: bytes, ptr: int) -> tuple[FileInfo, int]:
    # Will add more attributes if I find more
    fileinfo = {}
    version, ptr = read_version(file_bytes, ptr)
    fileinfo["version"] = version
    return FileInfo(**fileinfo), ptr


#### MODELS ####

def read_model_palette(file_bytes: bytes, ptr: int) -> tuple[ModelPalette, int]:
    model_palette = {}
    num_attr_indicated, ptr = _read_obj_list_len(file_bytes, ptr)
    num_attr = 0

    attributes = [
        "color",
        "icon",
        "values",
        "name",
        "type_id"
    ]
    while num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "ModelPalette", model_palette)
        if attr_name in ["color", "icon", "name", "type_id"]:
            ptr = _read_string_attribute(file_bytes, ptr, model_palette, attr_name)
        elif attr_name == "values":
            values = {}
            num_values, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_values):
                if file_bytes[ptr] != 0x92:
                    raise ValueError(f"Marker \\x92 expected but {hex(file_bytes[ptr])} was found instead. (NOTE: there might be other values I'm not aware of. Feel free to report!)")
                ptr += 1
                ftype, ptr = _read_number(file_bytes, ptr, "model palette ftype")
                value, ptr = _read_number(file_bytes, ptr, "model palette value")
                logging.debug([hex(ftype), hex(value)])
                values[ftype] = value
            model_palette[attr_name] = values


        else:
            raise AttributeError("Unexpected error occurred while processing ModelPalette")
        logging.debug("Found attribute %s with value = %s", attr_name, model_palette[attr_name])
        num_attr += 1
    
    return ModelPalette(**model_palette), ptr

def read_model_hardware(file_bytes: bytes, ptr: int) -> tuple[ModelHardware, int]:
    hardware = {}
    # All attributes of ModelHardware are strings
    attributes = [
        "width",
        "depth",
        "max_power",
        "weight",
        "height"
    ]
    num_attr_indicated, ptr = _read_obj_list_len(file_bytes, ptr)
    num_attr = 0
    while num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "ModelHardware", hardware)
        if attr_name in ["width", "depth", "max_power", "weight", "height"]:
            ptr = _read_string_attribute(file_bytes, ptr, hardware, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute '{attr_name}' found while processing ModelHardware")
        logging.debug("Found hardware attribute %s with value = %s", attr_name, hardware[attr_name])
        num_attr += 1
    return ModelHardware(**hardware), ptr

def read_model_macro(file_bytes: bytes, ptr: int) -> tuple[Macro, int]:


    macro = {}
    attributes = ["name", "steps"]
    ptr = _read_string_attribute(file_bytes, ptr, macro, "macro_type")
    num_attr_indicated, ptr = _read_obj_list_len(file_bytes, ptr)
    num_attr = 0

    while num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "Macro", macro)
        if attr_name in ["name"]:
            ptr = _read_string_attribute(file_bytes, ptr, macro, attr_name)
        elif attr_name == "steps":
            steps = []
            num_steps, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_steps):
                step, ptr = read_model_macro_step(file_bytes, ptr)
                steps.append(step)
            macro["steps"] = steps
        else:
            raise AttributeError(f"Unexpected attribute '{attr_name}' found while processing Macro")
        num_attr += 1

    return Macro(**macro), ptr


def read_model_macro_step(file_bytes: bytes, ptr: int) -> tuple[MacroStep, int]:
    step = {}
    attributes = ["ms_wait", "values"]
    if file_bytes[ptr] != 0x82:
        raise ValueError(f"Expected step object marker 0x82, got {hex(file_bytes[ptr])}")
    num_attr_indicated, ptr = _read_obj_list_len(file_bytes, ptr)
    num_attr = 0

    while num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "MacroStep", step)
        if attr_name == "ms_wait":
            ptr = _read_number_attribute(file_bytes, ptr, step, "ms_wait")
        elif attr_name == "values":
            values = []
            num_values, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_values):
                if file_bytes[ptr] != 0x92:
                    raise ValueError(f"Expected value object marker 0x92, got {hex(file_bytes[ptr])}")
                ptr += 1
                value_obj = {}
                ptr = _read_string_attribute(file_bytes, ptr, value_obj, "name")
                ptr = _read_number_attribute(file_bytes, ptr, value_obj, "value")
                values.append(value_obj)
            step["values"] = values
        else:
            raise AttributeError(f"Unexpected attribute '{attr_name}' found while processing MacroStep")
        num_attr += 1

    return MacroStep(**step), ptr

def read_model_value(file_bytes: bytes, ptr: int) -> tuple[ModelValue, int]:
    value_obj = {}
    num_attr_indicated, ptr = _read_obj_list_len(file_bytes, ptr)
    attributes = ["index", "inverse", "instant", "description", "ftype", "steps", "htp", "size"]
    num_attr = 0
    while num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "Value", value_obj)
        if attr_name in ["index", "ftype"]:
            ptr = _read_number_attribute(file_bytes, ptr, value_obj, attr_name)
        elif attr_name in ["inverse", "instant", "htp"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, value_obj, attr_name)
        elif attr_name == "description":
            ptr = _read_string_attribute(file_bytes, ptr, value_obj, attr_name)
        elif attr_name == "steps":
            steps_dict = {}
            num_steps, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_steps):
                id, ptr = _read_number(file_bytes, ptr, "model_value steps")
                step_obj, ptr = read_model_value_step(file_bytes, ptr)
                steps_dict[id] = step_obj
            value_obj["steps"] = steps_dict
        elif attr_name == "size":
            ptr = _read_number_attribute(file_bytes, ptr, value_obj, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing Value")
        logging.debug("Found attribute %s with value = %s", attr_name, value_obj.get(attr_name))
        num_attr += 1
    
    return ModelValue(**value_obj), ptr


def read_model_value_step(file_bytes: bytes, ptr: int) -> tuple[ModelValueStep, int]:
    step = {}
    if file_bytes[ptr] != 0x95:
        logging.debug(file_bytes[ptr:ptr+10])
        raise ValueError(f"Expected ModelValueStep marker 0x95, got {hex(file_bytes[ptr])} (NOTE: marker is not confirmed to be 0x95 only)")
    ptr += 1
    ptr = _read_string_attribute(file_bytes, ptr, step, "step_name")
    ptr = _read_number_attribute(file_bytes, ptr, step, "step_value")
    ptr = _read_string_attribute(file_bytes, ptr, step, "min_str")
    ptr = _read_string_attribute(file_bytes, ptr, step, "max_str")
    ptr = _read_string_attribute(file_bytes, ptr, step, "symbol")
    return ModelValueStep(**step), ptr

def read_model(file_bytes: bytes, ptr: int) -> tuple[Model, int]:
    """
    model_id,
    palette: {color, icon, values, name, type_id},
    name, short_name, default_inverted_pan, brand,
    hardware: {width, depth, max_power, weight, height},
    macros: {
        [macro_name],
        steps: {ms_wait, values},
        name
    },
    use_virtual_dimmer, default_inverted_tilt,
    values: {
        index, inverse, instant, description, ftype,
        steps: {values or smth idk}
        htp, size
    }
    mode_name, virtual_dimmer_channels, size
    """
    model = {}
    model_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)

    attributes = [
        "model_id",
        "palette",
        "name",
        "short_name",
        "default_inverted_pan",
        "brand",
        "hardware",
        "macros",
        "use_virtual_dimmer",
        "default_inverted_tilt",
        "values",
        "mode_name",
        "virtual_dimmer_channels",
        "size"
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "model", model)

        if attr_name in ["model_id", "type_id", "size"]:
            ptr = _read_number_attribute(file_bytes, ptr, model, attr_name)
        elif attr_name in ["default_inverted_pan", "use_virtual_dimmer", "default_inverted_tilt"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, model, attr_name)
        elif attr_name in ["name", "short_name", "brand", "mode_name"]:
            ptr = _read_string_attribute(file_bytes, ptr, model, attr_name)
        elif attr_name == "virtual_dimmer_channels":
            ptr = _read_list_attribute(file_bytes, ptr, model, attr_name)
        elif attr_name == "palette":
            palettes_dict = {}
            num_palettes, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_palettes):
                id, ptr = _read_number(file_bytes, ptr, "model palette id")
                palettes_dict[id], ptr = read_model_palette(file_bytes, ptr)
            model["palette"] = palettes_dict

        elif attr_name == "hardware":
            model["hardware"], ptr = read_model_hardware(file_bytes, ptr)

        elif attr_name == "macros":
            num_macros, ptr = _read_obj_list_len(file_bytes, ptr)
            macros = {}
            for _ in range(num_macros):
                macro, ptr = read_model_macro(file_bytes, ptr)
                macros[macro.macro_type] = macro
            model["macros"] = macros
        elif attr_name == "values":
            num_values, ptr = _read_obj_list_len(file_bytes, ptr)
            values = []
            for _ in range(num_values):
                value_obj, ptr = read_model_value(file_bytes, ptr)
                values.append(value_obj)
            model["values"] = values
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing model")
        logging.debug("Found attribute %s with value = %s", attr_name, model.get(attr_name))
        num_attr += 1

    # Add virtual intensity (ftype 516) if not already present
    if "values" in model:
        has_intensity = any(getattr(value, 'ftype', None) == 516 for value in model["values"])
        if not has_intensity:
            virtual_intensity = ModelValue(
                description="Intensity (Virtual)",
                ftype=516,
                index=len(model["values"]),  # Next available index
                size=1,
                htp=False,
                instant=False,
                inverse=False
            )
            model["values"].append(virtual_intensity)
            logging.debug("Added virtual dimmer Intensity (ftype 516) to model")

    _obj_checker(initial_ptr, ptr, model_bytelength, num_attr, num_attr_indicated)
    return Model(**model), ptr



### PATCHES ###

def read_patch(file_bytes: bytes, ptr: int) -> tuple[Patch, int]:
    patch = {}
    patch_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)

    # Start reading attributes
    attributes = [
        "model_id",
        "inverse_tilt",
        "name",
        "channels_ftype",
        "index",
        "universe",
        "description",
        "inverse_pan",
        "visual_id",
        "parked",
        "color_mark",
        "dimmer",
        "swap_pan_tilt",
        "virtual_dimmer",
        "id",
        "size",
        "frozen",
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "patch", patch)

        if attr_name in ["model_id", "index", "universe", "visual_id", "color_mark", "id", "size", "frozen"]:
            ptr = _read_number_attribute(file_bytes, ptr, patch, attr_name)
        elif attr_name in ["inverse_tilt", "inverse_pan", "parked", "swap_pan_tilt"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, patch, attr_name)
        elif attr_name in ["name", "description"]:
            ptr = _read_string_attribute(file_bytes, ptr, patch, attr_name)
        # Complex attributes
        elif attr_name == "channels_ftype":
            ptr = _read_list_attribute(file_bytes, ptr, patch, attr_name)
        elif attr_name == "dimmer":
            # genuinely i have no idea how this one is meant to work
            if file_bytes[ptr] != 0xCB:
                raise ValueError(
                    f"Unexpected value in patch -> dimmer. Expected 0xCB, got {hex(file_bytes[ptr])}. Note that 0xCB may not be the only valid representation. Feel free to report if this happens!"
                )
            patch[attr_name] = []
            ptr += 1
            for _ in range(8):
                patch[attr_name].append(file_bytes[ptr])
                ptr += 1
        elif attr_name == "virtual_dimmer":
            ptr = _read_list_attribute(file_bytes, ptr, patch, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing patch")
        logging.debug("Found attribute %s with value = %s", attr_name, patch[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, patch_bytelength, num_attr, num_attr_indicated)
    return Patch(**patch), ptr


def read_group(file_bytes: bytes, ptr: int) -> tuple[Group, int]:
    group = {}
    group_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)

    attributes = [
        "description",
        "color_mark",
        "visual_id",
        "patched_elements_ids",
        "grid",
        "steps",
        "automatico",
        "group_id",
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "group", group)

        if attr_name in ["color_mark", "visual_id", "group_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name in ["description"]:
            ptr = _read_string_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name in ["automatico"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name == "patched_elements_ids":
            ptr = _read_list_attribute(file_bytes, ptr, group, attr_name)
        elif attr_name == "grid":
            grid = {}
            num_fixtures, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_fixtures):
                fixture_id, ptr = _read_number(file_bytes, ptr, "group grid fixture_id")
                if file_bytes[ptr] != 0x92:
                    raise ValueError(f"Error found in grid. Expected marker 0x92, found {hex(file_bytes[ptr])} instead")
                ptr += 1
                fixture_x, ptr = _read_number(file_bytes, ptr, "group fixture_x")
                fixture_y, ptr = _read_number(file_bytes, ptr, "group fixture_y")
                grid[fixture_id] = [fixture_x, fixture_y]
            group[attr_name] = grid
        elif attr_name == "steps":
            steps = {}
            num_steps, ptr = _read_obj_list_len(file_bytes, ptr)
            for _ in range(num_steps):
                fixture_id, ptr = _read_number(file_bytes, ptr, "group steps fixture_id")
                step, ptr = _read_number(file_bytes, ptr, "group step")
                steps[fixture_id] = step
            group[attr_name] = steps
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing group")
        logging.debug("Found attribute %s with value = %s", attr_name, group[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, group_bytelength, num_attr, num_attr_indicated)
    return Group(**group), ptr


def read_order(file_bytes: bytes, ptr: int) -> tuple[Order, int]:
    order = {}
    if file_bytes[ptr] != 0x88:
        raise ValueError(f"Incorrect number of attributes specified for order in palette. Expected 0x88, got {hex(file_bytes[ptr])}")
    ptr += 1
    attributes = ["palette_id", "universe", "section", "receptor_type", "patch_id", "ftype", "value", "channel"]
    num_attr_indicated = 8
    num_attr = 0
    while file_bytes[ptr] != 0x88 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "order", order)

        if attr_name in ["palette_id", "universe", "section", "receptor_type", "patch_id", "channel", "ftype"]:
            ptr = _read_number_attribute(file_bytes, ptr, order, attr_name)
        # seperated this originally before _read_number_attribute was updated to handle multibyte values
        # keeping it here because of the channel marker check
        elif attr_name in ["value"]:
            ptr = _read_number_attribute(file_bytes, ptr, order, attr_name, b"\xa7channel")
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing order")
        logging.debug("Found attribute %s with value = %s", attr_name, order[attr_name])
        num_attr += 1

    if num_attr != num_attr_indicated:
        raise ValueError(f"Attribute count mismatch in order. Found {num_attr}, expected {num_attr_indicated}")
    # set to debug instead of info because there's a lot
    logging.debug("ORDER FOUND: %s", order)
    return order, ptr


def read_user_palette(file_bytes: bytes, ptr: int, all_palette_orders: dict) -> tuple[UserPalette, int]:
    palette = {}
    palette_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)

    attributes = ["section", "user_palette_id", "name", "icon", "orders"]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "user_palette", palette)

        if attr_name in ["section", "user_palette_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name in ["name", "icon"]:
            ptr = _read_string_attribute(file_bytes, ptr, palette, attr_name)
        elif attr_name == "orders":
            num_orders, ptr = _read_obj_list_len(file_bytes, ptr)
            palette[attr_name] = []
            for _ in range(num_orders):
                order, ptr = read_order(file_bytes, ptr)
                palette[attr_name].append(Order(**order))
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing user_palette")
        logging.debug("Found attribute %s with value = %s", attr_name, palette[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, palette_bytelength, num_attr, num_attr_indicated)

    if "orders" in palette:
        all_palette_orders[palette["user_palette_id"]] = palette["orders"]
    return UserPalette(**palette), ptr


def read_fx_layer_steps(file_bytes: bytes, ptr: int) -> tuple[FXLayerStep, int]:
    logging.debug("-" * 40 + " Parsing FX Layer Step " + "-" * 40)
    if file_bytes[ptr] != 0x8C:
        raise ValueError(f"Incorrect number of attributes specified for step in FX layer. Expected 0x8C, got {hex(file_bytes[ptr])}")
    ptr += 1
    num_attr_indicated = 12
    num_attr = 0
    step = {}
    attributes = [
        "start_limit",
        "palette_type",
        "name",
        "ancho",
        "curve_in",
        "curve_out",
        "strength",
        "curve_type",
        "palette_value",
        "inicio",
        "end_limit",
        "jumps",
    ]

    while file_bytes[ptr] != 0x8C and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "step", step)

        if attr_name in ["palette_type", "curve_type", "palette_value", "jumps"]:
            ptr = _read_number_attribute(file_bytes, ptr, step, attr_name)
        elif attr_name in [
            "start_limit",
            "strength",
            "ancho",
            "curve_in",
            "curve_out",
            "strength",
            "inicio",
            "end_limit",
        ]:
            ptr = _read_number_attribute(file_bytes, ptr, step, attr_name)
        elif attr_name in ["name"]:
            ptr = _read_string_attribute(file_bytes, ptr, step, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing step")
        logging.debug("Found attribute %s with value = %s", attr_name, step[attr_name])
        num_attr += 1

    if num_attr != num_attr_indicated:
        raise ValueError(f"Attribute count mismatch in step. Found {num_attr}, expected {num_attr_indicated}")
    logging.debug("-" * 40 + " End FX Layer Step " + "-" * 43)
    return FXLayerStep(**step), ptr


def read_fx_layer(file_bytes: bytes, ptr: int) -> tuple[FXLayer, int]:
    logging.debug("=" * 45 + " Parsing FX Layer " + "=" * 45)
    if file_bytes[ptr] != 0x88:
        raise ValueError(f"Incorrect number of attributes specified for layer in FX. Expected 0x88, got {hex(file_bytes[ptr])}")
    ptr += 1
    num_attr_indicated = 8
    num_attr = 0
    layer = {}
    attributes = ["blind", "phase_offset", "section", "curve", "steps", "ftypes", "id", "size"]

    while file_bytes[ptr] != 0x88 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "layer", layer)

        if attr_name in ["section", "id", "phase_offset", "curve", "size"]:
            ptr = _read_number_attribute(file_bytes, ptr, layer, attr_name)
        elif attr_name in ["blind"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, layer, attr_name)
        elif attr_name == "ftypes":
            ptr = _read_list_attribute(file_bytes, ptr, layer, attr_name)
        # Complex attributes
        elif attr_name == "steps":
            num_steps, ptr = _read_obj_list_len(file_bytes, ptr)
            layer[attr_name] = []
            for _ in range(num_steps):
                step, ptr = read_fx_layer_steps(file_bytes, ptr)
                layer[attr_name].append(step)

        
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing layer")
        logging.debug("Found attribute %s with value = %s", attr_name, layer[attr_name])
        num_attr += 1

    if num_attr != num_attr_indicated:
        raise ValueError(f"Attribute count mismatch in layer. Found {num_attr}, expected {num_attr_indicated}")
    logging.debug("=" * 45 + " End FX Layer " + "=" * 48)
    return FXLayer(**layer), ptr


def read_fx(file_bytes: bytes, ptr: int) -> tuple[FX, int]:
    fx = {}
    # NOTE: different from the usual init_object_reading
    expected_marker = b"\xde\x00\x18"
    if file_bytes[ptr : ptr + 3] != expected_marker:
        raise MarkerNotFoundError(f"Expected marker {expected_marker!r} not found for FX. Found {file_bytes[ptr : ptr + 3]!r} instead")
    num_attr_indicated = int.from_bytes(file_bytes[ptr + 1 : ptr + 3], "big")
    ptr += 3
    attributes = [
        "cyclos",
        "direction",
        "speed",
        "group_steps",
        "size",
        "layers",
        "patches",
        "speed_in_bpm",
        "width",
        "spread",
        "basic",
        "gfxid",
        "internal_speed",
        "fx_ref",
        "splits",
        "groups",
        "rect_width",
        "name",
        "phase_offset",
        "bpm",
        "render_id",
        "mode",
        "repeats",
        "rect_height",
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00 and num_attr < num_attr_indicated:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "fx", fx)

        if attr_name in [
            "cyclos",
            "direction",
            "group_steps",
            "gfxid",
            "splits",
            "rect_width",
            "render_id",
            "mode",
            "repeats",
            "rect_height",
        ]:
            ptr = _read_number_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ["speed", "size", "width", "spread", "internal_speed", "fx_ref", "phase_offset", "bpm"]:
            ptr = _read_number_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name == "name":
            ptr = _read_string_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ["speed_in_bpm", "basic"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, fx, attr_name)
        elif attr_name in ["patches", "groups"]:
            ptr = _read_list_attribute(file_bytes, ptr, fx, attr_name)

        # Complex attributes
        elif attr_name == "layers":
            num_layers, ptr = _read_obj_list_len(file_bytes, ptr)
            fx[attr_name] = []
            for _ in range(num_layers):
                layer, ptr = read_fx_layer(file_bytes, ptr)
                fx[attr_name].append(layer)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing fx")
        logging.debug("Found attribute %s with value = %s", attr_name, fx[attr_name])
        num_attr += 1

    if num_attr != num_attr_indicated:
        raise ValueError(f"Attribute count mismatch in FX. Found {num_attr}, expected {num_attr_indicated}")
    return FX(**fx), ptr


def read_cue(file_bytes: bytes, ptr: int, all_palette_orders: dict[int, list["Order"]]) -> tuple[Cue, int]:
    cue = {}
    cue_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = ["fx_palette", "cue_id", "description", "visual_id", "fxs", "actions", "fxs_channels", "orders", "name"]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "cue", cue)

        if attr_name in ["fx_palette"]:
            if file_bytes[ptr] == 0xFF:
                cue[attr_name] = "N/A"
                ptr += 1
            else:
                ptr = _read_number_attribute(file_bytes, ptr, cue, attr_name)
        elif attr_name in ["cue_id", "visual_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, cue, attr_name)
        elif attr_name in ["description", "name"]:
            ptr = _read_string_attribute(file_bytes, ptr, cue, attr_name)

        elif attr_name == "fxs":
            num_fxs, ptr = _read_obj_list_len(file_bytes, ptr)
            cue[attr_name] = []
            for _ in range(num_fxs):
                fx, ptr = read_fx(file_bytes, ptr)
                cue[attr_name].append(fx)

        elif attr_name == "actions":
            num_actions, ptr = _read_obj_list_len(file_bytes, ptr)
            if num_actions != 0:
                raise ValueError(f"Found {num_actions} actions. NOTE: Actions are not supported yet. Sorry!")
            cue[attr_name] = None

        elif attr_name == "fxs_channels":
            num_channels, ptr = _read_obj_list_len(file_bytes, ptr)
            # logging.info("Channel length: %d", num_channels)
            cue[attr_name] = []
            for _ in range(num_channels):
                channel_len, ptr = _read_obj_list_len(file_bytes, ptr)
                # logging.info("Channel length: %d", channel_len)
                channel = []
                i = 0
                # NOTE: some of the channel instances have:
                # \xD1 ?? and it doesn't count towards the channel_len for some reason?
                # \xCD multibyte values (these count towards channel_len)
                # will fix once I figure this out
                while i < channel_len:
                    # probably deleted? idk
                    if file_bytes[ptr] == 0xD1:
                        channel.append(file_bytes[ptr : ptr + 2].hex())
                        ptr += 2
                    else:
                        temp = {}
                        ptr = _read_number_attribute(file_bytes, ptr, temp, "channel")
                        channel.append(temp["channel"])
                        i += 1
                cue[attr_name].append(channel)
                logging.debug("Found channel with value = %s", channel)

        elif attr_name == "orders":
            num_orders, ptr = _read_obj_list_len(file_bytes, ptr)
            logging.debug("Number of orders: %d", num_orders)
            cue[attr_name] = []
            for _ in range(num_orders):
                order_dict, ptr = read_order(file_bytes, ptr)
                palette_id = order_dict["palette_id"]
                # checks if current order found exists as a palette's order already
                # if so, then replace the order with the palette's order object so they share the same Order
                if palette_id in all_palette_orders:
                    for palette_order in all_palette_orders[palette_id]:
                        if palette_order.to_dict() == order_dict:
                            order_obj = palette_order
                            break
                else:
                    order_obj = Order(**order_dict)

                cue[attr_name].append(order_obj)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing cue")
        logging.debug("Found attribute %s with value = %s", attr_name, cue[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, cue_bytelength, num_attr, num_attr_indicated)
    return Cue(**cue), ptr


def read_cuelist_element(file_bytes: bytes, ptr: int) -> tuple[CuelistElement, int]:
    element = {}
    if file_bytes[ptr] != 0x89:
        raise ValueError(f"Incorrect number of attributes specified for cuelist element. Expected 0x89, got {hex(file_bytes[ptr])}")
    ptr += 1
    attributes = [
        "ms_fadeout",
        "cue_id",
        "ms_delay",
        "next",
        "dotted_id",
        "ms_fadein",
        "ms_crossfade",
        "ms_duration",
        "halt",
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x89 and num_attr < 9:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "cuelist_element", element)

        if attr_name == "next":
            if file_bytes[ptr] == 0xFF:
                element[attr_name] = "N/A"
                ptr += 1
            else:
                ptr = _read_number_attribute(file_bytes, ptr, element, attr_name)
        elif attr_name in ["cue_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, element, attr_name)
        elif attr_name in ["halt"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, element, attr_name)
        elif attr_name in ["ms_fadeout", "ms_delay", "dotted_id", "ms_fadein", "ms_crossfade", "ms_duration"]:
            ptr = _read_number_attribute(file_bytes, ptr, element, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing cuelist_element")
        logging.debug("Found attribute %s with value = %s", attr_name, element[attr_name])
        num_attr += 1

    if num_attr != 9:
        raise ValueError(f"Incorrect number of attributes for cuelist element. Found {num_attr}, expected 9")

    return CuelistElement(**element), ptr


def read_cuelist(file_bytes: bytes, ptr: int) -> tuple[Cuelist, int]:
    cuelist = {}
    """
    byte: loops, visual_id, flash_mode, cuelist_id, 
    multibyte: ms_flash_attack, ms_chase_time, bpm_chase, ms_flash_decay, pcrossfade, ms_fadeout, ms_fadein, ms_crossfade, ms_flash_hold, ms_stop_time
    string: name
    boolean: autoreset, at_end_pause, chase, at_end_stop, no_first_fade, block_fx, 
    list:

    others: cuelist_elements: {ms_fadeout, cue_id, ms_delay, next, dotted_id, ms_fadein, ms_crossfade, ms_duration, halt},

    ms_flash_attack, autoreset, at_end_pause, loops, chase, ms_chase_time, visual_id, bpm_chase, ms_flash_decay, pcrossfade, ms_fadeout, direction, at_end_stop, flash_mode, cuelist_id, ms_fadein, ms_crossfade, no_first_fade, name, block_fx,
    cuelist_elements: {ms_fadeout, cue_id, ms_delay, next, dotted_id, ms_fadein, ms_crossfade, ms_duration, halt},
    ms_flash_hold, ms_stop_time
    """

    cuelist_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = [
        "ms_flash_attack",
        "autoreset",
        "at_end_pause",
        "loops",
        "chase",
        "ms_chase_time",
        "visual_id",
        "bpm_chase",
        "ms_flash_decay",
        "pcrossfade",
        "ms_fadeout",
        "direction",
        "at_end_stop",
        "flash_mode",
        "cuelist_id",
        "ms_fadein",
        "ms_crossfade",
        "no_first_fade",
        "name",
        "block_fx",
        "cuelist_elements",
        "ms_flash_hold",
        "ms_stop_time",
    ]

    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "cuelist", cuelist)

        # Handle different attribute types
        if attr_name in ["loops", "visual_id", "flash_mode", "cuelist_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, cuelist, attr_name)
        elif attr_name in ["autoreset", "at_end_pause", "chase", "at_end_stop", "no_first_fade", "block_fx"]:
            ptr = _read_boolean_attribute(file_bytes, ptr, cuelist, attr_name)
        elif attr_name == "name":
            ptr = _read_string_attribute(file_bytes, ptr, cuelist, attr_name)
        elif attr_name in [
            "ms_flash_attack",
            "ms_chase_time",
            "bpm_chase",
            "ms_flash_decay",
            "pcrossfade",
            "ms_fadeout",
            "ms_fadein",
            "ms_crossfade",
            "ms_flash_hold",
            "ms_stop_time",
            "direction",
        ]:
            ptr = _read_number_attribute(file_bytes, ptr, cuelist, attr_name)
        elif attr_name == "cuelist_elements":
            num_elements, ptr = _read_obj_list_len(file_bytes, ptr)
            cuelist[attr_name] = []
            for _ in range(num_elements):
                element, ptr = read_cuelist_element(file_bytes, ptr)
                cuelist[attr_name].append(element)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing cuelist")
        logging.debug("Found attribute %s with value = %s", attr_name, cuelist[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, cuelist_bytelength, num_attr, num_attr_indicated)
    return Cuelist(**cuelist), ptr


def read_playback(file_bytes: bytes, ptr: int) -> tuple[Playback, int]:
    """
    byte: fader_value, index, priority, trigger_level, page, cuelist
    multibyte: fader_mode, ms_chase_time, bpm_chase, pcrossfade, ms_fadeout, ms_fadein, ms_crossfade,
    string:
    boolean: on_load_play, chase, fader_up_play, on_page_stop, is_executor, fader_down_stop, on_page_play, docked, ignore_grand_master
    list: xct_color, xct_push_mode, xct_cuelist,

    fader_value, on_load_play, fader_mode, chase, index, ms_chase_time, fader_up_play, priority, bpm_chase, on_page_stop, trigger_level, is_executor, pcrossfade, ms_fadeout, fader_down_stop, ms_fadein, ms_crossfade, on_page_play, xct_color, cuelist, xct_push_mode,  docked, xct_cuelist, page
    """

    playback = {}
    playback_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = [
        "fader_value",
        "on_load_play",
        "fader_mode",
        "chase",
        "index",
        "ms_chase_time",
        "fader_up_play",
        "priority",
        "bpm_chase",
        "on_page_stop",
        "trigger_level",
        "is_executor",
        "pcrossfade",
        "ms_fadeout",
        "fader_down_stop",
        "ignore_swap",
        "swap_always",
        "ms_fadein",
        "ms_crossfade",
        "on_page_play",
        "xct_color",
        "cuelist",
        "xct_push_mode",
        "docked",
        "used_in_alarm",
        "xct_cuelist",
        "page",
        "ignore_grand_master",
        "xct_swap",
    ]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "playback", playback)

        # Handle different attribute types
        if attr_name in ["fader_value", "index", "priority", "trigger_level", "cuelist", "page"]:
            ptr = _read_number_attribute(file_bytes, ptr, playback, attr_name)
        elif attr_name in [
            "fader_mode",
            "ms_chase_time",
            "bpm_chase",
            "pcrossfade",
            "ms_fadeout",
            "ms_fadein",
            "ms_crossfade",
        ]:
            ptr = _read_number_attribute(file_bytes, ptr, playback, attr_name)
        elif attr_name in [
            "on_load_play",
            "chase",
            "fader_up_play",
            "on_page_stop",
            "is_executor",
            "fader_down_stop",
            "ignore_swap",
            "swap_always",
            "on_page_play",
            "docked",
            "ignore_grand_master",
            "used_in_alarm",
        ]:
            ptr = _read_boolean_attribute(file_bytes, ptr, playback, attr_name)
        elif attr_name in ["xct_push_mode", "xct_swap"]:
            ptr = _read_list_attribute(file_bytes, ptr, playback, attr_name, attribute_type="bool")
        elif attr_name in ["xct_color", "xct_cuelist"]:
            ptr = _read_list_attribute(file_bytes, ptr, playback, attr_name)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing playback")

        logging.debug("Found attribute %s with value = %s", attr_name, playback[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, playback_bytelength, num_attr, num_attr_indicated)
    return Playback(**playback), ptr


def read_config(file_bytes: bytes, ptr: int) -> tuple[General.Config, int]:
    config = {}
    if file_bytes[ptr : ptr + 11] != b"\x00\x00\x00\x07\xa6config":
        raise MarkerNotFoundError("Could not find config marker in file")
    ptr += 11
    config_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = [
        "update_mode",
        "executors_exclusive_mode",
        "remove_non_empty_cuelist",
        "clear_ltp",
        "bpm_mode",
        "show_password",
        "show_password_enabled",
    ]

    num_attr = 0
    while num_attr < num_attr_indicated and file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "config", config)

        if attr_name in ["update_mode"]:
            ptr = _read_number_attribute(file_bytes, ptr, config, attr_name)
        elif attr_name in [
            "executors_exclusive_mode",
            "remove_non_empty_cuelist",
            "clear_ltp",
            "bpm_mode",
            "show_password_enabled",
        ]:
            ptr = _read_boolean_attribute(file_bytes, ptr, config, attr_name)
        elif attr_name in ["show_password"]:
            ptr = _read_string_attribute(file_bytes, ptr, config, attr_name)
        else:
            raise AttributeError("Unexpected error occurred while processing config")

        logging.debug("Found attribute %s with value = %s", attr_name, config[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, config_bytelength, num_attr, num_attr_indicated)
    return General.Config(**config), ptr


def read_general(file_bytes: bytes, ptr: int) -> tuple[General, int]:
    # Will add more attributes if I find more
    general = {}
    config, ptr = read_config(file_bytes, ptr)
    general["config"] = config
    return General(**general), ptr


def read_fxpalette(file_bytes: bytes, ptr: int) -> tuple[dict, int]:
    fxpalette = {}
    fxpalette_bytelength, initial_ptr, num_attr_indicated, ptr = _init_object_reading(file_bytes, ptr)
    attributes = ["fx_palette", "cue_id", "visual_id", "fxs", "fxs_channels", "orders", "name"]
    num_attr = 0
    while file_bytes[ptr] != 0x00:
        attr_name, ptr = _read_attribute_name(file_bytes, ptr, attributes, "fxpalette", fxpalette)

        if attr_name in ["fx_palette", "cue_id", "visualid"]:
            ptr = _read_number_attribute(file_bytes, ptr, fxpalette, attr_name)
        elif attr_name in ["visual_id"]:
            ptr = _read_number_attribute(file_bytes, ptr, fxpalette, attr_name)
        elif attr_name in ["name"]:
            ptr = _read_string_attribute(file_bytes, ptr, fxpalette, attr_name)

        elif attr_name == "fxs":
            num_fxs, ptr = _read_obj_list_len(file_bytes, ptr)
            fxpalette[attr_name] = []
            for _ in range(num_fxs):
                fx, ptr = read_fx(file_bytes, ptr)
                fxpalette[attr_name].append(fx)

        elif attr_name == "fxs_channels":
            num_channels, ptr = _read_obj_list_len(file_bytes, ptr)
            fxpalette[attr_name] = []
            for _ in range(num_channels):
                channel_len, ptr = _read_obj_list_len(file_bytes, ptr)
                channel = []
                i = 0
                # NOTE: some of the channel instances have:
                # \xD1 ?? and it doesn't count towards the channel_len.
                # I'm assuming these are deleted values, but will fix once I actually figure this out

                while i < channel_len:
                    if file_bytes[ptr] == 0xD1:
                        channel.append(file_bytes[ptr : ptr + 2].hex())
                        ptr += 2
                    else:
                        temp = {}
                        ptr = _read_number_attribute(file_bytes, ptr, temp, "channel")
                        channel.append(temp["channel"])
                        i += 1
                fxpalette[attr_name].append(channel)
                logging.debug("Found channel with value = %s", channel)

        elif attr_name == "orders":
            num_orders, ptr = _read_obj_list_len(file_bytes, ptr)
            logging.debug("Number of orders: %d", num_orders)
            fxpalette[attr_name] = []
            for _ in range(num_orders):
                order_obj, ptr = read_order(file_bytes, ptr)
                fxpalette[attr_name].append(order_obj)
        else:
            raise AttributeError(f"Unexpected attribute {attr_name} found while processing fxpalette")
        logging.debug("Found attribute %s with value = %s", attr_name, fxpalette[attr_name])
        num_attr += 1

    _obj_checker(initial_ptr, ptr, fxpalette_bytelength, num_attr, num_attr_indicated)
    return FXPalette(**fxpalette), ptr
