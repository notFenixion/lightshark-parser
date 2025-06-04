import argparse
import logging
import sys

class Lightshow:
    def __init__(self):
        self._fileinfo = {}
        self._models = {}
        self._patches = {}
        self._groups = {}
        self._user_palettes = {}
        self._cues = {}

    def add_model(self, model):
        self._models[model.id] = model
    
    def add_patch(self, patch):
        self._patches[patch.id] = patch

    def add_group(self, group):
        self._groups[group.id] = group

    def add_palette(self, palette):
        self._user_palettes[palette.id] = palette

    def add_cue(self, cue):
        self._cues[cue.id] = cue

    def parse_bytes(self):
        pass

    def update_bytes(self):
        pass


class Model:
    def __init__(self, model_id):
        self.model_id = model_id
        self.palettes = []

class Patch:
    def __init__(self, model_id, inverse_tilt, name, channels_ftype, index, universe, description, inverse_pan, visual_id, parked, color_mark, dimmer, swap_pan_tilt, virtual_dimmer, id, size):
        self.model_id = model_id
        self.inverse_tilt = inverse_tilt
        self.name = name
        self.channels_ftype = channels_ftype
        self.index = index
        self.universe = universe
        self.description = description
        self.inverse_pan = inverse_pan
        self.visual_id = visual_id
        self.parked = parked
        self.color_mark = color_mark
        self.dimmer = dimmer
        self.swap_pan_tilt = swap_pan_tilt
        self.virtual_dimmer = virtual_dimmer
        self.id = id
        self.size = size
       



class Group:

    def __init__(self):
        self.description = None
        self.color_mark = None
        self.visual_id = None
        self.patched_elements_ids = []
        self.grid = {}
        self.steps = {}
        self.automatic = None
        self.group_id = None

# class UserPalette:

#     def __init__(self):
#         self.section =
#         self.user_palette_id = 
#         self.name = 
#         self.orders = 

# class OrderPalette:

#     def __init__(self):
#         self.palete_id =
#         self.universe = 
#         self.section = 
#         self.receptor_type = 
#         self.patch_id = 
#         self.ftype = 
#         self.value = 
#         self.channel = 


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


def read_patching(file_bytes):
    
    pointer = file_bytes.find('\xAA#patching#')
    print(pointer)


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
    user_palettes = {} #store user_palette_id as index
    
    





    return Lightshow()


def argparse():
    parser = argparse.ArgumentParser(description='Read and parse .lshw files')
    parser.add_argument('file', help='Path to the .lshw file to be parsed')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()



def main():
    args = argparse()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    file_bytes = read_file_bytes(args.file)
    print(f"Successfully read {len(file_bytes)} bytes from {args.file}")
    print(file_bytes[:32].hex())

    lightshow = Lightshow()
    lightshow.parse_bytes(file_bytes)





if __name__ == "__main__":
    main()