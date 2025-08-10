import os
import sys
import orjson
from pathlib import Path

from lightshark_parser.classes import Lightshow
from lightshark_parser.parsers.section_parsers import *
from lightshark_parser.utils.custom_errors import MarkerNotFoundError
from lightshark_parser.utils.logger import logger

def print_dash_line():
    try:
        logger.info("-" * (os.get_terminal_size().columns - 5))
    except:
        logger.info("-" * 80)


def parse_lshw(filepath: str, output_file: str = None) -> Lightshow:
    """
    Parse a LightShark .lshw file from a file path.
    Args:
        filepath: The path to the .lshw file.
        output_file: Optional, path to save parsed JSON.
    Returns:
        Lightshow object.
    """
    if not filepath.lower().endswith(".lshw"):
        print("Error: File must have be of extension .lshw", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    return parse_file_bytes(file_bytes, output_file=output_file, filepath=filepath)

def parse_file_bytes(file_bytes: bytes, output_file: str = None,  filepath: str = None) -> Lightshow:
    """
    Parse a LightShark .lshw file from bytes.
    Args:
        file_bytes: The bytes of the .lshw file.
        filepath: Optional, for logging/metadata only.
        output_file: Optional, path to save parsed JSON.
    Returns:
        Lightshow object.
    """
    if filepath and not filepath.lower().endswith(".lshw"):
        print("Error: File must have be of extension .lshw", file=sys.stderr)
        sys.exit(1)

    fileinfo = None
    models = None
    patching = None
    groups = None
    user_palettes = None
    cues = None
    cuelists = None
    playbacks = None
    general = None
    fxpalettes = None
    # other sections. i dont fully understand these yet so not parsing them for now
    schedules = None
    osc_targets = None

    ptr = 0
    all_palette_orders = {}

    # num_checked = 0
    # section_headers = [
    #     b"\x00\x00\x00\x0b\xaa#fileinfo#",
    #     b"\x00\x00\x00\x09\xa8#models#",
    #     b"\x00\x00\x00\x0b\xaa#patching#",
    #     b"\x00\x00\x00\x10\xaf#user_palettes#",
    #     b"\x00\x00\x00\x07\xa6#cues#",
    #     b"\x00\x00\x00\x0b\xaa#cuelists#",
    #     b"\x00\x00\x00\x0c\xab#playbacks#",
    #     b"\x00\x00\x00\x0a\xa9#general#",
    #     b"\x00\x00\x00\x0d\xac#fxpalettes#"
    # ]




    print("Starting parsing...")
    ## FILEINFO ##
    if file_bytes[ptr : ptr + 15] != b"\x00\x00\x00\x0b\xaa#fileinfo#":
        logger.warning("Could not find #fileinfo# in file. If your file contains a fileinfo section, please fix it.")
    else:
        ptr += 15
        fileinfo, ptr = read_fileinfo(file_bytes, ptr)
        logger.info("FOUND FILEINFO: %s", fileinfo.__dict__)
        for obj in fileinfo.__dict__.values():
            logger.info("Found object: %s", obj.__dict__)
        print_dash_line()

    ## MODELS ##
    print("Finished reading fileinfo. Moving onto models...")
    if file_bytes[ptr : ptr + 13] != b"\x00\x00\x00\x09\xa8#models#":
        raise MarkerNotFoundError("Could not find #models# in file")
    models = {}
    ptr += 13
    while file_bytes[ptr : ptr + 10] == b"\x00\x00\x00\x06\xa5model":
        ptr += 10
        model, ptr = read_model(file_bytes, ptr)
        if model.model_id in models:
            raise ValueError(f"Duplicate model ID found: {model.model_id}")
        models[model.model_id] = model
        logger.info("FOUND MODEL: %s", model.__dict__)
        print_dash_line()
    if not models:
        logger.warning("No models found in file. Did you configure models and patches yet?")

    ## PATCHES ##
    logger.info("Finished reading models. Moving onto patches...")
    if file_bytes[ptr : ptr + 15] != b"\x00\x00\x00\x0b\xaa#patching#":
        raise MarkerNotFoundError("Could not find #patching# in file")
    patching = {}
    ptr += 15
    while file_bytes[ptr : ptr + 10] == b"\x00\x00\x00\x06\xa5patch":
        ptr += 10
        patch, ptr = read_patch(file_bytes, ptr)
        if patch.id in patching:
            raise ValueError(f"Duplicate patch ID found: {patch.id}")
        patching[patch.id] = patch
        logger.info("FOUND PATCH: %s", patch.__dict__)
        print_dash_line()
    if not patching:
        logger.warning(
            "No patches found in file. This warning is only a concern if there are patches in your show but none were detected."
        )

    ## GROUPS ##
    print("Finished reading patches. Moving onto groups...")
    # initial check for if there are groups at all
    if file_bytes[ptr : ptr + 10] == b"\x00\x00\x00\x06\xa5group":
        groups = {}
    while file_bytes[ptr : ptr + 10] == b"\x00\x00\x00\x06\xa5group":
        ptr += 10
        group, ptr = read_group(file_bytes, ptr)
        if group.group_id in groups:
            raise ValueError(f"Duplicate group ID found: {group.group_id}")
        groups[group.group_id] = group
        logger.info("FOUND GROUP: %s", group.__dict__)
        print_dash_line()
    if not groups:
        logger.warning("No groups found in file. This warning is only a concern if there are groups in your show but none were detected.")

    ## USER PALETTES ##
    print("Finished reading groups. Moving onto user palettes...")
    # logger.debug(file_bytes[ptr:ptr+20])
    if file_bytes[ptr : ptr + 20] != b"\x00\x00\x00\x10\xaf#user_palettes#":
        raise MarkerNotFoundError("Could not find #user_palettes# in file")
    user_palettes = {}
    ptr += 20
    deleted_flag = False
    while file_bytes[ptr : ptr + 17] == b"\x00\x00\x00\x0d\xacuser_palette" or (
        deleted_flag and file_bytes[ptr : ptr + 16] == b"\x00\x00\x0d\xacuser_palette"
    ):
        ptr += (17 if not deleted_flag else 16)
        # For logging a unique case wherein a user_palette was deleted. Not sure if this is just an issue with a show, more testing required.
        if file_bytes[ptr : ptr + 16] == b"\x00\x00\x0d\xacuser_palette":
            logger.warning(
                "user_palette marker '\\x00\\x00\\x0d\\xacuser_palette' was found at position %d instead of expected '\\x00\\x00\\x00\\x0d\\xacuser_palette'. This may be a case wherein a user_palette was deleted and is thus ignored. It is recommended to check for missing user_palette_ids",
                ptr
            )
            print("Potential deleted palette found. Recommended to check for any missing 'user_palette_id' values.")
            deleted_flag = True
        else:
            deleted_flag = False
            palette, ptr = read_user_palette(file_bytes, ptr, all_palette_orders)
            if palette.user_palette_id in user_palettes:
                raise ValueError(f"Duplicate user palette ID found: {palette.user_palette_id}")
            user_palettes[palette.user_palette_id] = palette
            logger.info("FOUND PALETTE: %s", palette.__dict__)
            print_dash_line()
    if not user_palettes:
        logger.warning(
            "No user palettes found in file. This warning is only a concern if there are user palettes in your show but none were detected."
        )

    ## CUES ##
    print("Finished reading user palettes. Moving onto cues...")
    if file_bytes[ptr : ptr + 11] != b"\x00\x00\x00\x07\xa6#cues#":
        raise MarkerNotFoundError("Could not find #cues# in file")
    cues = {}
    ptr += 11
    while file_bytes[ptr : ptr + 8] == b"\x00\x00\x00\x04\xa3cue":
        ptr += 8
        cue, ptr = read_cue(file_bytes, ptr, all_palette_orders)
        if cue.cue_id in cues:
            raise ValueError(f"Duplicate cue ID found: {cue.cue_id}")
        cues[cue.cue_id] = cue
        logger.info("FOUND CUE: %s", cue.__dict__)
        print_dash_line()
    if not cues:
        logger.warning("No cues found in file. This warning is only a concern if there are cues in your show but none were detected.")

    ## CUELISTS ##
    print("Finished reading cues. Moving onto cuelists...")
    if file_bytes[ptr : ptr + 15] != b"\x00\x00\x00\x0b\xaa#cuelists#":
        raise MarkerNotFoundError("Could not find #cuelists# in file")
    cuelists = {}
    ptr += 15
    while file_bytes[ptr : ptr + 12] == b"\x00\x00\x00\x08\xa7cuelist":
        ptr += 12
        cuelist, ptr = read_cuelist(file_bytes, ptr)
        if cuelist.cuelist_id in cuelists:
            raise ValueError(f"Duplicate cuelist ID found: {cuelist.cuelist_id}")
        cuelists[cuelist.cuelist_id] = cuelist
        logger.info("FOUND CUELIST: %s", cuelist.__dict__)
        print_dash_line()
    if not cuelists:
        logger.warning(
            "No cuelists found in file. This warning is only a concern if there are cuelists in your show but none were detected."
        )

    ## PLAYBACKS ##
    print("Finished reading cuelists. Moving onto playbacks...")
    if file_bytes[ptr : ptr + 16] != b"\x00\x00\x00\x0c\xab#playbacks#":
        raise MarkerNotFoundError("Could not find #playbacks# in file")
    playbacks = {}
    ptr += 16
    while file_bytes[ptr : ptr + 13] == b"\x00\x00\x00\x09\xa8playback":
        ptr += 13
        playback, ptr = read_playback(file_bytes, ptr)
        if playback.combined_id in playbacks:
            raise ValueError(f"Duplicate playback ID found: {playback.combined_id}")
        playbacks[playback.combined_id] = playback
        logger.info("FOUND PLAYBACK (ID: %s): %s", playback.combined_id, playback.__dict__)
        print_dash_line()
    if not playbacks:
        logger.warning(
            "No playbacks found in file. This warning is only a concern if there are playback faders assigned in your show but none were detected."
        )

    ## GENERAL ##
    print("Finished reading playbacks. Moving onto general...")
    if file_bytes[ptr : ptr + 14] != b"\x00\x00\x00\x0a\xa9#general#":
        raise MarkerNotFoundError("Could not find #general# in file")
    ptr += 14
    general, ptr = read_general(file_bytes, ptr)
    logger.info("FOUND GENERAL: %s", general.__dict__)
    for obj in general.__dict__.values():
        logger.info("Found object: %s", obj.__dict__)
    print_dash_line()
    if not general:
        logger.warning("No general found in file. This warning is only a concern if there is general in your show but none were detected.")

    ## FX PALETTES ##
    print("Finished reading general. Moving onto FX palettes...")
    if file_bytes[ptr : ptr + 17] != b"\x00\x00\x00\x0d\xac#fxpalettes#":
        logger.warning("Could not find #fxpalettes# in file.")
    else:
        fxpalettes = {}
        ptr += 17
        while file_bytes[ptr : ptr + 14] == b"\x00\x00\x00\x0a\xa9fxpalette":
            ptr += 14
            fxpalette, ptr = read_fxpalette(file_bytes, ptr)
            if fxpalette.fx_palette in fxpalettes:
                raise ValueError(f"Duplicate FX palette ID found: {fxpalette.fx_palette}")
            fxpalettes[fxpalette.fx_palette] = fxpalette
            logger.info("FOUND FX PALETTE: %s", fxpalette.__dict__)
            print_dash_line()
        if not fxpalettes:
            logger.warning(
                "No fx palettes found in file. This warning is only a concern if there are fx palettes in your show but none were detected."
            )

    logger.info("Finished reading FX palettes. Parsing complete! (until schedules is done)")

    # Create Lightshow object
    lightshow = Lightshow(
        # filepath=filepath,
        fileinfo=fileinfo,
        models=models,
        patches=patching,
        groups=groups,
        user_palettes=user_palettes,
        cues=cues,
        cuelists=cuelists,
        playbacks=playbacks,
        fxpalettes=fxpalettes,
        general=general,
    )

    # Handle output file writing if specified
    if output_file:
        try:
            # Get the dictionary representation
            data = lightshow.to_dict()
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                json_bytes = orjson.dumps(data, option=(orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY))

                with open(output_path, "wb") as f:
                    f.write(json_bytes)

                logger.info(f"Successfully saved to {output_path}")

            except TypeError as e:
                logger.error("TypeError during JSON serialization: %s", e)
                if isinstance(data, dict):
                    logger.debug("Attempting to find non-serializable object...")
                    _debug_serialization(data)
                raise
        except Exception as e:
            logger.error("Error saving to %s: %s", output_file, e, exc_info=True)
            print(f"Error saving to {output_file}. Check logs for details.", file=sys.stderr)
            raise

    return lightshow



def _debug_serialization(obj, path=""):
    """
    Recursively find non-serializable objects for orjson.
    Thank you AI again for this check LOL
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            current_path = f"{path}['{k}']" if path else k
            try:
                orjson.dumps({k: v})
            except TypeError as e:
                logger.error("Found non-serializable object at path: %s", current_path)
                logger.error("Type: %s, Value: %s", type(v).__name__, repr(v))
                logger.error("Error: %s", str(e))
                if hasattr(v, "__dict__"):
                    logger.error("Object attributes: %s", v.__dict__.keys())
            if isinstance(v, (dict, list)):
                _debug_serialization(v, current_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            current_path = f"{path}[{i}]"
            try:
                orjson.dumps([v])
            except TypeError as e:
                logger.error("Found non-serializable object in list at path: %s", current_path)
                logger.error("Type: %s, Value: %s", type(v).__name__, repr(v))
                logger.error("Error: %s", str(e))
                if hasattr(v, "__dict__"):
                    logger.error("Object attributes: %s", v.__dict__.keys())
            if isinstance(v, (dict, list)):
                _debug_serialization(v, current_path)
