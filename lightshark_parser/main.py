import argparse
import logging
import os
import sys
import orjson
from pathlib import Path
from typing import Dict, Any

from .classes import Lightshow
from .parsers.section_parsers import read_patch, read_group, read_user_palette, read_cue, read_cuelist, read_playback, read_general, read_fxpalette

def print_dash_line():
    try:
        logging.info("-" * (os.get_terminal_size().columns - 5))
    except:
        logging.info("-" * 80)

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


def parse_file_bytes(file_bytes: bytes, output_file: str = None) -> Lightshow:
    fileinfo = {}
    models = {}
    patching = {} # Key: patch ID, Value: Patch object
    groups = {} # Key: group ID, Value: Group object
    user_palettes = {}
    cues = {}
    cuelists = {}
    playbacks = {}
    general = {}
    fxpalettes = {}
    # other sections. i dont fully understand these yet so not parsing them for now
    schedules = {}
    osc_targets = {}



    # Initial search for #patching# section
    # NOTE THAT THIS IS TEMPORARY AND WILL BE REMOVED ONCE FILEINFO + MODEL ARE ADDED. #patching# assert will be kept.
    ptr = file_bytes.find(b'\xAA#patching#')
    assert ptr != -1, "Could not find #patching# in file"
    logging.debug(f"Found #patching# at index {ptr}")
    ptr += 11
    logging.debug(file_bytes[ptr:ptr+10])

    ## PATCHES ##
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5patch':
        ptr += 10
        patch, ptr = read_patch(file_bytes, ptr)
        patching[patch.id] = patch
        logging.info("FOUND PATCH: %s", patch.__dict__)
        print_dash_line()
    if not patching:
        logging.warning("No patches found in file. This warning is only a concern if there are patches in your show but none were detected.")

    ## GROUPS ##
    logging.info("Finished reading patches. Moving onto groups...")
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5group':
        ptr += 10
        group, ptr = read_group(file_bytes, ptr)
        groups[group.group_id] = group
        logging.info("FOUND GROUP: %s", group.__dict__)
        print_dash_line()
    if not groups:
        logging.warning("No groups found in file. This warning is only a concern if there are groups in your show but none were detected.")


    ## USER PALETTES ##
    logging.info("Finished reading groups. Moving onto user palettes...")
    # logging.debug(file_bytes[ptr:ptr+20])
    assert file_bytes[ptr:ptr+20] == b'\x00\x00\x00\x10\xaf#user_palettes#', "Could not find #user_palettes# in file"
    ptr += 20
    deleted_flag = False
    while file_bytes[ptr:ptr+17] == b'\x00\x00\x00\x0d\xacuser_palette' or (deleted_flag and file_bytes[ptr:ptr+16] == b'\x00\x00\x0d\xacuser_palette'):
        ptr += 17 if not deleted_flag else 16
        # For logging a unique case wherein a user_palette was deleted. Not sure if this is just an issue with a show, more testing required.
        if file_bytes[ptr:ptr+16] == b'\x00\x00\x0d\xacuser_palette':
            logging.warning("Marker not found at expected position. This may be a case wherein a user_palette was deleted and is thus ignored. It is recommended to check for missing user_palette_ids")
            deleted_flag = True
        else:
            deleted_flag = False
            palette, ptr = read_user_palette(file_bytes, ptr)
            user_palettes[palette.user_palette_id] = palette
            logging.info("FOUND PALETTE: %s", palette.__dict__)
            print_dash_line()
    if not user_palettes:
        logging.warning("No user palettes found in file. This warning is only a concern if there are user palettes in your show but none were detected.")
    
    ## CUES ##
    logging.info("Finished reading groups. Moving onto cues...")
    assert file_bytes[ptr:ptr+11] == b'\x00\x00\x00\x07\xa6#cues#', "Could not find #cues# in file"
    ptr += 11
    while file_bytes[ptr:ptr+8] == b'\x00\x00\x00\x04\xa3cue':
        ptr += 8
        cue, ptr = read_cue(file_bytes, ptr)
        cues[cue.cue_id] = cue
        logging.info("FOUND CUE: %s", cue.__dict__)
        print_dash_line()
    if not cues:
        logging.warning("No cues found in file. This warning is only a concern if there are cues in your show but none were detected.")

    ## CUELISTS ##
    logging.info("Finished reading cues. Moving onto cuelists...")
    assert file_bytes[ptr:ptr+15] == b'\x00\x00\x00\x0b\xaa#cuelists#', "Could not find #cuelists# in file"
    ptr += 15
    while file_bytes[ptr:ptr+12] == b'\x00\x00\x00\x08\xa7cuelist':
        ptr += 12
        cuelist, ptr = read_cuelist(file_bytes, ptr)
        cuelists[cuelist.cuelist_id] = cuelist
        logging.info("FOUND CUELIST: %s", cuelist.__dict__)
        print_dash_line()
    if not cuelists:
        logging.warning("No cuelists found in file. This warning is only a concern if there are cuelists in your show but none were detected.")

    ## PLAYBACKS ##
    logging.info("Finished reading cuelists. Moving onto playbacks...")
    assert file_bytes[ptr:ptr+16] == b'\x00\x00\x00\x0c\xab#playbacks#', "Could not find #playbacks# in file"
    ptr += 16
    while file_bytes[ptr:ptr+13] == b'\x00\x00\x00\x09\xa8playback':
        ptr += 13
        playback, ptr = read_playback(file_bytes, ptr)
        playbacks[playback.combined_id] = playback
        logging.info("FOUND PLAYBACK (ID: %s): %s", playback.combined_id, playback.__dict__)
        print_dash_line()
    if not playbacks:
        logging.warning("No playbacks found in file. This warning is only a concern if there are playback faders assigned in your show but none were detected.")
    
    ## GENERAL ##
    logging.info("Finished reading playbacks. Moving onto general...")
    assert file_bytes[ptr:ptr+14] == b'\x00\x00\x00\x0a\xa9#general#', "Could not find #general# in file"
    ptr += 14
    general, ptr = read_general(file_bytes, ptr)
    logging.info("FOUND GENERAL: %s", general.__dict__)
    for obj in general.__dict__.values():
        logging.info("Found object: %s", obj.__dict__)
    print_dash_line()
    if not general:
        logging.warning("No general found in file. This warning is only a concern if there is general in your show but none were detected.")



    ## FX PALETTES ##
    logging.info("Finished reading general. Moving onto FX palettes...")
    assert file_bytes[ptr:ptr+17] == b'\x00\x00\x00\x0d\xac#fxpalettes#', "Could not find #fxpalettes# in file"
    ptr += 17
    while file_bytes[ptr:ptr+14] == b'\x00\x00\x00\x0a\xa9fxpalette':
        ptr += 14
        fxpalette, ptr = read_fxpalette(file_bytes, ptr)
        fxpalettes[fxpalette.fx_palette] = fxpalette
        logging.info("FOUND FX PALETTE: %s", fxpalette.__dict__)
        print_dash_line()
    if not fxpalettes:
        logging.warning("No fx palettes found in file. This warning is only a concern if there are fx palettes in your show but none were detected.")


    # Create Lightshow object
    lightshow = Lightshow(
        fileinfo=fileinfo,
        models=models,
        patches=patching,
        groups=groups,
        user_palettes=user_palettes,
        cues=cues,
        cuelists=cuelists,
        playbacks=playbacks,
        fxpalettes=fxpalettes,
        general=general
    )
    
    # Run all analysis functions if available (testing only)
    try:
        from .testing_utils.analyze_show import analyze_universe_patches
        analyze_universe_patches(patching, user_palettes)
    except (ImportError, AttributeError) as e:
        logging.debug("Skipping analysis (testing_utils/analyze_show.py not found or error in analysis): %s", e)


    # Handle output file writing if specified
    if output_file:
        try:
            # Get the dictionary representation
            data = lightshow.to_dict()
            
            # Debug: Print the structure of the data
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Data structure type: %s", type(data).__name__)
                if isinstance(data, dict):
                    logging.debug("Top-level keys: %s", list(data.keys()))
                    if 'cues' in data:
                        logging.debug("Number of cues: %d", len(data['cues']))
                        if data['cues']:
                            first_cue = next(iter(data['cues'].values()))
                            logging.debug("First cue keys: %s", list(first_cue.keys()) if hasattr(first_cue, 'keys') else 'N/A')
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                json_bytes = orjson.dumps(
                    data,
                    option=(
                        orjson.OPT_INDENT_2 | 
                        orjson.OPT_NON_STR_KEYS |
                        orjson.OPT_SERIALIZE_NUMPY
                    )
                )

                with open(output_path, 'wb') as f:
                    f.write(json_bytes)

                print(f"Successfully saved to {output_path}")
                
            except TypeError as e:
                logging.error("TypeError during JSON serialization: %s", e)
                if isinstance(data, dict):
                    logging.debug("Attempting to find non-serializable object...")
                    _debug_serialization(data)
                raise
        except Exception as e:
            logging.error("Error saving to %s: %s", output_file, e, exc_info=True)
            print(f"Error saving to {output_file}. Check logs for details.", file=sys.stderr)
            raise
    
    return lightshow




def _debug_serialization(obj, path=''):
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
                logging.error("Found non-serializable object at path: %s", current_path)
                logging.error("Type: %s, Value: %s", type(v).__name__, repr(v))
                logging.error("Error: %s", str(e))
                if hasattr(v, '__dict__'):
                    logging.error("Object attributes: %s", v.__dict__.keys())
            if isinstance(v, (dict, list)):
                _debug_serialization(v, current_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            current_path = f"{path}[{i}]"
            try:
                orjson.dumps([v])
            except TypeError as e:
                logging.error("Found non-serializable object in list at path: %s", current_path)
                logging.error("Type: %s, Value: %s", type(v).__name__, repr(v))
                logging.error("Error: %s", str(e))
                if hasattr(v, '__dict__'):
                    logging.error("Object attributes: %s", v.__dict__.keys())
            if isinstance(v, (dict, list)):
                _debug_serialization(v, current_path)

def setup_logging(verbosity=0):
    """Setup logging with different verbosity levels.
    
    Args:
        verbosity (int): 0=WARNING, 1=INFO (object found), 2=DEBUG (attributes)
    """
    log_level = logging.WARNING
    if verbosity == 1:
        log_level = logging.INFO
    elif verbosity >= 2:
        log_level = logging.DEBUG
    
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s:%(message)s',
        stream=sys.stderr
    )


def main() -> None:
    parser = argparse.ArgumentParser(description='Read and parse .lshw files')
    parser.add_argument('file', nargs='?', help='Path to the .lshw file to be parsed')
    parser.add_argument('-v', '--verbose', action='count', default=0, 
                       help='Increase verbosity (use -v for basic info, -vv for detailed debug)')
    parser.add_argument('-o', '--output', metavar='FILE', help='Output JSON file to save the parsed data')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.verbose)
    
    file_bytes = read_file_bytes(args.file)
    file_size_mb = len(file_bytes) / (1024 * 1024)
    logging.info("Successfully read %.2f MB from %s", file_size_mb, args.file)

    if args.verbose >= 2:
        logging.debug("File size: %d bytes", len(file_bytes))

    lightshow = parse_file_bytes(file_bytes, args.output)

    if not args.output:
        print(lightshow.to_dict())
        print_dash_line()

    print("Successfully parsed file!")
        