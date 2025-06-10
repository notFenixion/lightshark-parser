from typing import Dict, List, Any, Optional, Tuple

class Lightshow:
    def __init__(self, fileinfo: Dict = None, models: Dict = None, patches: Dict[Any, 'Patch'] = None, groups: Dict[Any, 'Group'] = None, user_palettes: Dict = None, cues: Dict = None):
        self._fileinfo: Dict = fileinfo if fileinfo is not None else {}
        self._models: Dict[Any, Any] = models if models is not None else {}
        self._patches: Dict[Any, 'Patch'] = patches if patches is not None else {}
        self._groups: Dict[Any, 'Group'] = groups if groups is not None else {}
        self._user_palettes: Dict = user_palettes if user_palettes is not None else {}
        self._cues: Dict = cues if cues is not None else {}

    def add_model(self, model: 'Model') -> None:
        self._models[model.id] = model
    
    def add_patch(self, patch: 'Patch') -> None:
        self._patches[patch.id] = patch

    def add_group(self, group: 'Group') -> None:
        self._groups[group.id] = group

    def add_palette(self, palette: 'UserPalette') -> None:
        self._user_palettes[palette.id] = palette

    def add_cue(self, cue: 'Cue') -> None:
        self._cues[cue.id] = cue

    def parse_to_bytes(self) -> None:
        pass

    def to_dict(self) -> Dict:
        return {
            'fileinfo': self._fileinfo,
            'models': [model.__dict__ for model in self._models.values()] if self._models else [],
            'patches': [patch.__dict__ for patch in self._patches.values()] if self._patches else [],
            'groups': [group.__dict__ for group in self._groups.values()] if self._groups else [],
            'user_palettes': {k: v.to_dict() for k, v in self._user_palettes.items()},
            'cues': self._cues or {}
        }



class Model:
    def __init__(self, model_id: int) -> None:
        self.model_id: int = model_id
        self.palettes: List[Any] = []

class Patch:
    def __init__(self, model_id: Optional[int] = None, inverse_tilt: Optional[bool] = None, name: Optional[str] = None, channels_ftype: Optional[List[str]] = None, index: Optional[int] = None, universe: Optional[int] = None, description: Optional[str] = None, inverse_pan: Optional[bool] = None, visual_id: Optional[int] = None, parked: Optional[bool] = None, color_mark: Optional[int] = None, dimmer: Optional[List[int]] = None, swap_pan_tilt: Optional[bool] = None, virtual_dimmer: Optional[List[int]] = None, id: Optional[int] = None, size: Optional[int] = None) -> None:
        self.model_id: Optional[int] = model_id
        self.inverse_tilt: Optional[bool] = inverse_tilt
        self.name: Optional[str] = name
        self.channels_ftype: List[str] = channels_ftype if channels_ftype is not None else []
        self.index: Optional[int] = index
        self.universe: Optional[int] = universe
        self.description: Optional[str] = description
        self.inverse_pan: Optional[bool] = inverse_pan
        self.visual_id: Optional[int] = visual_id
        self.parked: Optional[bool] = parked
        self.color_mark: Optional[int] = color_mark
        self.dimmer: List[int] = dimmer if dimmer is not None else []
        self.swap_pan_tilt: Optional[bool] = swap_pan_tilt
        self.virtual_dimmer: List[int] = virtual_dimmer if virtual_dimmer is not None else []
        self.id: Optional[int] = id
        self.size: Optional[int] = size


class Group:
    def __init__(self, description: Optional[str] = None, color_mark: Optional[int] = None, visual_id: Optional[int] = None, patched_elements_ids: Optional[List[int]] = None, grid: Optional[Dict[int, Tuple[int, int]]] = None, steps: Optional[Dict[int, int]] = None, automatico: Optional[bool] = None, group_id: Optional[int] = None) -> None:
        self.description: Optional[str] = description
        self.color_mark: Optional[int] = color_mark
        self.visual_id: Optional[int] = visual_id
        self.patched_elements_ids: List[int] = patched_elements_ids if patched_elements_ids is not None else []
        self.grid: Dict[int, Tuple[int, int]] = grid if grid is not None else {}
        self.steps: Dict[int, int] = steps if steps is not None else {}
        self.automatico: Optional[bool] = automatico
        self.group_id: Optional[int] = group_id

class UserPalette:
    def __init__(self, section: Any = None, user_palette_id: Any = None, name: Optional[str] = None, orders: Optional[List[Any]] = None) -> None:
        self.section: Any = section
        self.user_palette_id: Any = user_palette_id
        self.name: Optional[str] = name
        self.orders: List[Any] = orders if orders is not None else []
    
    def to_dict(self) -> dict:
        return {
            'section': self.section,
            'user_palette_id': self.user_palette_id,
            'name': self.name,
            'orders': [order.to_dict() if hasattr(order, 'to_dict') else str(order) for order in self.orders]
        }

class Order:
    def __init__(self, palette_id: Any = None, universe: Any = None, section: Any = None, receptor_type: Any = None, patch_id: Any = None, ftype: Any = None, value: Any = None, channel: Any = None) -> None:
        self.palette_id: Any = palette_id
        self.universe: Any = universe
        self.section: Any = section
        self.receptor_type: Any = receptor_type
        self.patch_id: Any = patch_id
        self.ftype: Any = ftype
        self.value: Any = value
        self.channel: Any = channel
    
    def to_dict(self) -> dict:
        return {
            'palette_id': self.palette_id,
            'universe': self.universe,
            'section': self.section,
            'receptor_type': self.receptor_type,
            'patch_id': self.patch_id,
            'ftype': self.ftype if isinstance(self.ftype, (str, int, float, bool, type(None))) else str(self.ftype),
            'value': self.value if isinstance(self.value, (str, int, float, bool, type(None))) else str(self.value),
            'channel': self.channel
        }


class Cue:
    def __init__(self, fx_palette=None, cue_id=None, visualid=None, fxs=[], fxs_channels=[], orders=[], name=None):
        self.fx_palette = fx_palette
        self.cue_id = cue_id
        self.visualid = visualid
        self.fxs = fxs
        self.fxs_channels = fxs_channels
        self.orders = orders
        self.name = name


class FX:
    def __init__(self, cyclos=None, direction=None, speed=None, group_steps=None, size=None, layers=[], Patches=None, speed_in_bpm=None, width=None, spread=None, basic=None, gfxid=None, internal_speed=None, fx_ref=None, splits=None, groups=None, rect_width=None, name=None, phase_offset=None, bpm=None, render_id=None, mode=None, repeats=None, rect_height=None):
        self.cyclos = cyclos
        self.direction = direction
        self.speed = speed
        self.group_steps = group_steps
        self.size = size
        self.layers = layers
        self.Patches = Patches
        self.speed_in_bpm = speed_in_bpm
        self.width = width
        self.spread = spread
        self.basic = basic
        self.gfxid = gfxid
        self.internal_speed = internal_speed
        self.fx_ref = fx_ref
        self.splits = splits
        self.groups = groups
        self.rect_width = rect_width
        self.name = name
        self.phase_offset = phase_offset
        self.bpm = bpm
        self.render_id = render_id
        self.mode = mode
        self.repeats = repeats
        self.rect_height = rect_height


class Layer:
    def __init__(self, blind=None, phase_offset=None, section=None, curve=None, steps=None, ftypes=None, id=None, size=None):
        self.blind = blind
        self.phase_offset = phase_offset
        self.section = section
        self.curve = curve
        self.steps = steps
        self.ftypes = ftypes
        self.id = id
        self.size = size

