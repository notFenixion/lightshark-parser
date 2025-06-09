
class Lightshow:
    def __init__(self):
        self._fileinfo = {}
        self._models = {}
        self._patches = {}
        self._groups = {}
        self._user_palettes = {}
        self._cues = {}

    def __init__(self, fileinfo={}, models={}, patches={}, groups={}, user_palettes={}, cues={}):
        self._fileinfo = fileinfo
        self._models = models
        self._patches = patches
        self._groups = groups
        self._user_palettes = user_palettes
        self._cues = cues

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

    def parse_to_bytes(self):
        pass

    def to_dict(self):
        """Convert the Lightshow object to a dictionary for JSON serialization."""
        return {
            'fileinfo': self._fileinfo,
            'models': [model.__dict__ for model in self._models.values()] if self._models else [],
            'patches': [patch.__dict__ for patch in self._patches.values()] if self._patches else [],
            'groups': [group.__dict__ for group in self._groups.values()] if self._groups else [],
            'user_palettes': self._user_palettes or {},
            'cues': self._cues or {}
        }



class Model:
    def __init__(self, model_id):
        self.model_id = model_id
        self.palettes = []

class Patch:

    def __init__(self):
        self.model_id = None
        self.inverse_tilt = None
        self.name = None
        self.channels_ftype = []
        self.index = None
        self.universe = None
        self.description = None
        self.inverse_pan = None
        self.visual_id = None
        self.parked = None
        self.color_mark = None
        self.dimmer = []
        self.swap_pan_tilt = None
        self.virtual_dimmer = []
        self.id = None
        self.size = None

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
        self.automatico = None
        self.group_id = None

    def __init__(self, description, color_mark, visual_id, patched_elements_ids, grid, steps, automatico, group_id):
        self.description = description
        self.color_mark = color_mark
        self.visual_id = visual_id
        self.patched_elements_ids = patched_elements_ids
        self.grid = grid
        self.steps = steps
        self.automatico = automatico
        self.group_id = group_id

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