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


def read_patching_and_groups(file_bytes):
    '''
    We do both patches and groups in the same function because both are under the "#patching#" section in the .lshw file
    I'm reading attributes the complicated way to see if my theory works (also to match how lightshark reads the file kinda?)
    '''
    
    patching = []
    groups = []

    ptr = file_bytes.find(b'\xAA#patching#')
    assert ptr != -1, "Could not find #patching# in file"
    logging.debug(f"Found #patching# at index {ptr}")

    ptr += 11
    logging.debug(file_bytes[ptr:ptr+10])

    ## PATCHES ##
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5patch':
        patch = {}
        patch_bytelength = int.from_bytes(file_bytes[ptr+10:ptr+14], 'big')
        initial_ptr = ptr+14
        assert file_bytes[ptr+14:ptr+17] == b'\xde\x00\x10', "xDE0010 not spotted at the right location of patch :("
        ptr += 17

        # Start reading attributes
        logging.debug(file_bytes[ptr:ptr+1])
        attributes = ['model_id', 'inverse_tilt', 'name', 'channels_ftype', 'index', 'universe', 'description', 'inverse_pan', 'visual_id', 'parked', 'color_mark', 'dimmer', 'swap_pan_tilt', 'virtual_dimmer', 'id', 'size']
        while file_bytes[ptr] != 0x00:
            attr_name_len = file_bytes[ptr] - 0xA0
            attr_name = file_bytes[ptr+1:ptr+attr_name_len+1].decode('utf-8')
            # logging.debug(f"Found attribute \"{attr_name}\" of length {attr_name_len} bytes")
            assert attr_name in attributes, f"Error: Attribute {attr_name} is not a patch attribute / Attribute length byte is incorrect"

            ptr += attr_name_len + 1
            # 1 byte attributes. i dont think these go beyond 255 in normal circumstances
            if attr_name in ['model_id', 'index', 'universe', 'visual_id', 'color_mark', 'id', 'size']:
                patch[attr_name] = file_bytes[ptr]
                ptr += 1
            # boolean attributes
            elif attr_name in ['inverse_tilt', 'inverse_pan', 'parked', 'swap_pan_tilt']:
                # Compare with integers instead of bytes
                assert file_bytes[ptr] in [0xC2, 0xC3], "Error: Attribute value is not a boolean (0xC2 or 0xC3)"
                patch[attr_name] = file_bytes[ptr] == 0xC3  # True if 0xC3, False if 0xC2
                ptr += 1
            elif attr_name in ['name', 'description']:
                name_len = file_bytes[ptr] - 0xA0
                patch[attr_name] = file_bytes[ptr+1:ptr+name_len+1].decode('utf-8')
                ptr += name_len + 1
            elif attr_name == 'channels_ftype':
                num_channels = file_bytes[ptr] - 0x90
                patch[attr_name] = []
                ptr += 1
                for i in range(num_channels):
                    ftype_len = file_bytes[ptr] - 0xCB
                    patch[attr_name].append(file_bytes[ptr+1:ptr+ftype_len+1].decode('utf-8'))
                    ptr += ftype_len + 1
            elif attr_name == 'dimmer':
                #genuinely i have no idea how this one is meant to work
                assert file_bytes[ptr] == 0xCB, "Well this is an unique case i've never seen"
                patch[attr_name] = []
                ptr += 1
                for i in range(8):
                    patch[attr_name].append(file_bytes[ptr])
                    ptr += 1
            elif attr_name == 'virtual_dimmer':
                num_dimmers = file_bytes[ptr] - 0x90
                patch[attr_name] = []
                ptr += 1
                for i in range(num_dimmers):
                    patch[attr_name].append(file_bytes[ptr])
                    ptr += 1
            else:
                assert False, f"Error: this error shouldnt occur..."
            logging.debug(f"Found attribute {attr_name} with value = {patch[attr_name]}")

        logging.debug("Current ptr: %s, Initial+indicated: %s", ptr, initial_ptr + patch_bytelength)
        # logging.debug(file_bytes[ptr])
        # logging.debug(file_bytes[initial_ptr + patch_bytelength:initial_ptr + patch_bytelength + 4])
        assert initial_ptr + patch_bytelength == ptr, "Error: patch bytelength indicated does not match actual patch bytelength"

        patching.append(Patch(**patch))
        logging.debug("FOUND PATCH: " + str(patching[-1].__dict__)+"\n"+"-"*80)


    ## GROUPS ##
    while file_bytes[ptr:ptr+10] == b'\x00\x00\x00\x06\xa5group':

        group = {}
        
        #TODO: implement!#

                    
        groups.append(Groups(**group))            
                
                

        





    return patching, groups


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


def main():
    parser = argparse.ArgumentParser(description='Read and parse .lshw files')
    parser.add_argument('file', nargs='?', help='Path to the .lshw file to be parsed')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    file_bytes = read_file_bytes(args.file)
    logging.debug(f"Successfully read {len(file_bytes)} bytes from {args.file}")
    logging.debug("Sample bytes:" + file_bytes[:32].hex())

    read_patching(file_bytes)


    lightshow = Lightshow()





if __name__ == "__main__":
    main()