import argparse
import logging
import os
import sys
from .utils.json_encoder import CompactJSONEncoder
from .classes import Lightshow, Patch, Group, UserPalette
from .parsers.section_parsers import read_patch, read_group, read_user_palette

def print_dash_line():
    try:
        print("-" * os.get_terminal_size().columns)
    except:
        print("-" * 80)

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
        ptr += 10
        patch, ptr = read_patch(file_bytes, ptr)
        patch_obj = Patch(**patch)
        patching[patch_obj.id] = patch_obj
        logging.debug("FOUND PATCH: " + str(patch_obj.__dict__))
        print_dash_line()
    if not patching:
        logging.warning("No patches found in file. This warning is only a concern if there are patches in your show but none were detected.")

    ## GROUPS ##
    logging.debug("Finished reading patches. Moving onto groups...")
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5group':
        ptr += 10
        group, ptr = read_group(file_bytes, ptr)
        group_obj = Group(**group)
        groups[group_obj.group_id] = group_obj
        logging.debug("FOUND GROUP: " + str(group_obj.__dict__))
        print_dash_line()
    if not groups:
        logging.warning("No groups found in file. This warning is only a concern if there are groups in your show but none were detected.")


    ## USER PALETTES ##
    logging.debug("Finished reading groups. Moving onto user palettes...")
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
            palette_obj = UserPalette(**palette)
            user_palettes[palette_obj.user_palette_id] = palette_obj
            logging.debug("FOUND PALETTE: " + str(palette_obj.__dict__))
            print_dash_line()
    





    # Create Lightshow object
    lightshow = Lightshow(
        patches=patching,
        groups=groups,
        user_palettes=user_palettes,
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
            data = lightshow.to_dict()
            json_str = CompactJSONEncoder(indent=2, ensure_ascii=False).encode(data)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            print(f"Successfully saved to {output_file}")
        except Exception as e:
            print(f"Error saving to {output_file}: {e}", file=sys.stderr)
    
    return lightshow




def main() -> None:
    parser = argparse.ArgumentParser(description='Read and parse .lshw files')
    parser.add_argument('file', nargs='?', help='Path to the .lshw file to be parsed')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-o', '--output', help='Output JSON file to save the parsed data')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    file_bytes = read_file_bytes(args.file)
    logging.debug(f"Successfully read {len(file_bytes)} bytes from {args.file}")

    lightshow = parse_file_bytes(file_bytes, args.output)

    if not args.output:
        print(lightshow.to_dict())
        print_dash_line()

    print("Successfully parsed file!")
        