import orjson
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
        """Convert the Lightshow object to a dictionary for JSON serialization."""
        # Helper function to convert objects to dicts
        def to_dict_recursive(obj):
            if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
                return obj.to_dict()
            elif hasattr(obj, '__dict__'):
                return {k: to_dict_recursive(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, (list, tuple)):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): to_dict_recursive(v) for k, v in obj.items()}
            return obj
            
        return {
            'fileinfo': to_dict_recursive(self._fileinfo),
            'models': [to_dict_recursive(model) for model in self._models.values()],
            'patches': [to_dict_recursive(patch) for patch in self._patches.values()],
            'groups': [to_dict_recursive(group) for group in self._groups.values()],
            'user_palettes': {str(k): to_dict_recursive(v) for k, v in self._user_palettes.items()},
            'cues': {str(k): to_dict_recursive(v) for k, v in self._cues.items()}
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

    def to_dict(self) -> dict:
        """Convert the Patch object to a dictionary for JSON serialization."""
        return {
            'model_id': self.model_id,
            'inverse_tilt': self.inverse_tilt,
            'name': self.name,
            'channels_ftype': self.channels_ftype,
            'index': self.index,
            'universe': self.universe,
            'description': self.description,
            'inverse_pan': self.inverse_pan,
            'visual_id': self.visual_id,
            'parked': self.parked,
            'color_mark': self.color_mark,
            'dimmer': self.dimmer,
            'swap_pan_tilt': self.swap_pan_tilt,
            'virtual_dimmer': self.virtual_dimmer,
            'id': self.id,
            'size': self.size
        }


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

    def to_dict(self) -> dict:
        """Convert the Group object to a dictionary for JSON serialization."""
        # Convert grid tuples to lists for JSON serialization
        grid_dict = {}
        for k, v in self.grid.items():
            if isinstance(v, tuple):
                grid_dict[str(k)] = list(v)
            else:
                grid_dict[str(k)] = v
                
        # Convert steps keys to strings
        steps_dict = {str(k): v for k, v in self.steps.items()}
        
        return {
            'description': self.description,
            'color_mark': self.color_mark,
            'visual_id': self.visual_id,
            'patched_elements_ids': self.patched_elements_ids,
            'grid': grid_dict,
            'steps': steps_dict,
            'automatico': self.automatico,
            'group_id': self.group_id
        }


class UserPalette:
    def __init__(self, section: int = None, user_palette_id: int = None, name: str = None, orders: Optional[List['Order']] = None) -> None:
        self.section: int = section
        self.user_palette_id: int = user_palette_id
        self.name: str = name
        self.orders: List['Order'] = orders if orders is not None else []
    
    def to_dict(self) -> dict:
        """Convert the UserPalette object to a dictionary for JSON serialization."""
        return {
            'section': self.section,
            'user_palette_id': self.user_palette_id,
            'name': self.name,
            'orders': [
                order.to_dict() if hasattr(order, 'to_dict') else order
                for order in self.orders
            ]
        }

class Order:
    def __init__(self, palette_id: int = None, universe: int = None, section: int = None, 
                 receptor_type: int = None, patch_id: int = None, ftype: str = None, 
                 value: int = None, channel: int = None) -> None:
        self.palette_id: int = palette_id
        self.universe: int = universe
        self.section: int = section
        self.receptor_type: int = receptor_type
        self.patch_id: int = patch_id
        self.ftype: str = ftype
        self.value: int = value
        self.channel: int = channel

    def to_dict(self) -> dict:
        """Convert the Order object to a dictionary for JSON serialization."""
        return {
            'palette_id': self.palette_id,
            'universe': self.universe,
            'section': self.section,
            'receptor_type': self.receptor_type,
            'patch_id': self.patch_id,
            'ftype': self.ftype,
            'value': self.value,
            'channel': self.channel
        }


class Cue:
    def __init__(self, fx_palette: int = None, cue_id: int = None, visual_id: int = None, 
                 fxs: List['FX'] = None, fxs_channels: List[dict] = None, 
                 orders: List[Order] = None, name: str = None) -> None:
        self.fx_palette: int = fx_palette
        self.cue_id: int = cue_id
        self.visual_id: int = visual_id
        self.fxs: List['FX'] = fxs if fxs is not None else []
        self.fxs_channels: List[dict] = fxs_channels if fxs_channels is not None else []
        self.orders: List[Order] = orders if orders is not None else []
        self.name: str = name
        
    def to_dict(self) -> dict:
        """Convert the Cue object to a dictionary for JSON serialization."""
        # Helper function to convert bytes to Unicode escape sequences in nested structures
        def convert_bytes(obj):
            if isinstance(obj, bytes):
                # Convert bytes to a string of Unicode escape sequences (e.g., b'\x02\x04' -> '\\u0002\\u0004')
                return ''.join(f'\\u{byte:04x}' for byte in obj)
            elif isinstance(obj, dict):
                return {str(k): convert_bytes(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_bytes(item) for item in obj]
            return obj
            
        # Convert fxs_channels to ensure all bytes are converted to Unicode escape sequences
        converted_fxs_channels = convert_bytes(self.fxs_channels)
        
        # Convert fxs list
        fxs_list = []
        for fx in self.fxs:
            if hasattr(fx, 'to_dict'):
                fxs_list.append(fx.to_dict())
            elif hasattr(fx, '__dict__'):
                fxs_list.append(fx.__dict__)
            else:
                fxs_list.append(fx)
        
        # Convert orders
        orders_list = []
        for order in self.orders:
            if hasattr(order, 'to_dict'):
                orders_list.append(order.to_dict())
            elif hasattr(order, '__dict__'):
                orders_list.append(order.__dict__)
            else:
                orders_list.append(order)
        
        return {
            'fx_palette': self.fx_palette,
            'cue_id': self.cue_id,
            'visual_id': self.visual_id,
            'fxs': fxs_list if self.fxs else None,  # Set to None if empty list
            'fxs_channels': converted_fxs_channels,
            'orders': orders_list,
            'name': self.name
        }


class FX:
    class FXLayer:
        def __init__(self, blind: bool = None, phase_offset: int = None, section: int = None, 
                    curve: int = None, steps: List['FX.FXLayerSteps'] = None, 
                    ftypes: List[str] = None, id: int = None, size: int = None) -> None:
            self.blind: bool = blind
            self.phase_offset: int = phase_offset
            self.section: int = section
            self.curve: int = curve
            self.steps: List['FX.FXLayerSteps'] = steps if steps is not None else []
            self.ftypes: List[str] = ftypes if ftypes is not None else []
            self.id: int = id
            self.size: int = size
            
        def to_dict(self) -> dict:
            # Convert steps to their dictionary representation
            steps_list = []
            for step in self.steps:
                if hasattr(step, 'to_dict'):
                    steps_list.append(step.to_dict())
                elif hasattr(step, '__dict__'):
                    steps_list.append(step.__dict__)
                else:
                    steps_list.append(step)
                    
            return {
                'blind': self.blind,
                'phase_offset': self.phase_offset,
                'section': self.section,
                'curve': self.curve,
                'steps': steps_list,
                'ftypes': self.ftypes,
                'id': self.id,
                'size': self.size
            }
    
    class FXLayerStep:
        def __init__(self, start_limit: int = None, palette_type: int = None, name: str = None, 
                    ancho: int = None, curve_in: int = None, curve_out: int = None, 
                    strength: int = None, curve_type: int = None, palette_value: Any = None, 
                    inicio: int = None, end_limit: int = None, jumps: int = None) -> None:
            self.start_limit: int = start_limit
            self.palette_type: int = palette_type
            self.name: str = name
            self.ancho: int = ancho
            self.curve_in: int = curve_in
            self.curve_out: int = curve_out
            self.strength: int = strength
            self.curve_type: int = curve_type
            self.palette_value: Any = palette_value  # Could be multi-value
            self.inicio: int = inicio
            self.end_limit: int = end_limit
            self.jumps: int = jumps
            
        def to_dict(self) -> dict:
            # Convert palette_value if it's a complex object
            palette_value = self.palette_value
            if hasattr(palette_value, 'to_dict'):
                palette_value = palette_value.to_dict()
            elif hasattr(palette_value, '__dict__'):
                palette_value = palette_value.__dict__
                
            return {
                'start_limit': self.start_limit,
                'palette_type': self.palette_type,
                'name': self.name,
                'ancho': self.ancho,
                'curve_in': self.curve_in,
                'curve_out': self.curve_out,
                'strength': self.strength,
                'curve_type': self.curve_type,
                'palette_value': palette_value,
                'inicio': self.inicio,
                'end_limit': self.end_limit,
                'jumps': self.jumps
            }
    
    def __init__(self, cyclos: int = None, direction: int = None, speed: int = None, group_steps: int = None, 
                 size: int = None, layers: List[FXLayer] = None, patches: List[int] = None, 
                 speed_in_bpm: bool = None, width: int = None, spread: int = None, basic: bool = None, 
                 gfxid: int = None, internal_speed: int = None, fx_ref: int = None, splits: int = None, 
                 groups: List[int] = None, rect_width: int = None, name: str = None, 
                 phase_offset: int = None, bpm: int = None, render_id: int = None, 
                 mode: int = None, repeats: int = None, rect_height: int = None) -> None:
        # Single byte attributes
        self.cyclos: int = cyclos
        self.direction: int = direction
        self.group_steps: int = group_steps
        self.gfxid: int = gfxid
        self.splits: int = splits
        self.rect_width: int = rect_width
        self.render_id: int = render_id
        self.mode: int = mode
        self.repeats: int = repeats
        self.rect_height: int = rect_height
        # Multibyte attributes
        self.speed: int = speed
        self.size: int = size
        self.width: int = width
        self.spread: int = spread
        self.internal_speed: int = internal_speed
        self.fx_ref: int = fx_ref
        self.phase_offset: int = phase_offset
        self.bpm: int = bpm
        # String attribute
        self.name: str = name
        # Boolean attributes
        self.speed_in_bpm: bool = speed_in_bpm
        self.basic: bool = basic
        # List attributes
        self.patches: List[int] = patches if patches is not None else []
        self.groups: List[int] = groups if groups is not None else []
        
        # Object attributes
        self.layers: List[FX.FXLayer] = layers if layers is not None else []
        
    def to_dict(self) -> dict:
        """Convert the FX object to a dictionary for JSON serialization."""
        # Convert layers to their dictionary representation
        layers_list = []
        for layer in self.layers:
            if hasattr(layer, 'to_dict'):
                layers_list.append(layer.to_dict())
            elif hasattr(layer, '__dict__'):
                layers_list.append(layer.__dict__)
            else:
                layers_list.append(layer)
                
        return {
            # Single byte attributes
            'cyclos': self.cyclos,
            'direction': self.direction,
            'group_steps': self.group_steps,
            'gfxid': self.gfxid,
            'splits': self.splits,
            'rect_width': self.rect_width,
            'render_id': self.render_id,
            'mode': self.mode,
            'repeats': self.repeats,
            'rect_height': self.rect_height,
            # Multibyte attributes
            'speed': self.speed,
            'size': self.size,
            'width': self.width,
            'spread': self.spread,
            'internal_speed': self.internal_speed,
            'fx_ref': self.fx_ref,
            'phase_offset': self.phase_offset,
            'bpm': self.bpm,
            # String attribute
            'name': self.name,
            # Boolean attributes
            'speed_in_bpm': self.speed_in_bpm,
            'basic': self.basic,
            # List attributes
            'patches': self.patches,
            'groups': self.groups,
            # Object attributes
            'layers': [layer.to_dict() for layer in self.layers] if hasattr(self, 'layers') else []
        }
        

class Playback:
    def __init__(self, fader_value=None, on_load_play=None, fader_mode=None, chase=None, index=None, ms_chase_time=None, fader_up_play=None, priority=None, bpm_chase=None, on_page_stop=None, trigger_level=None, is_executor=None, pcrossfade=None, ms_fadeout=None, fader_down_stop=None, ms_fadein=None, ms_crossfade=None, on_page_play=None, xct_color=None, cuelist=None, xct_push_mode=None, docked=None, xct_cuelist=None, page=None):
        self.fader_value = fader_value
        self.on_load_play = on_load_play
        self.fader_mode = fader_mode
        self.chase = chase
        self.index = index
        self.ms_chase_time = ms_chase_time
        self.fader_up_play = fader_up_play
        self.priority = priority
        self.bpm_chase = bpm_chase
        self.on_page_stop = on_page_stop
        self.trigger_level = trigger_level
        self.is_executor = is_executor
        self.pcrossfade = pcrossfade
        self.ms_fadeout = ms_fadeout
        self.fader_down_stop = fader_down_stop
        self.ms_fadein = ms_fadein
        self.ms_crossfade = ms_crossfade
        self.on_page_play = on_page_play
        self.xct_color = xct_color
        self.cuelist = cuelist
        self.xct_push_mode = xct_push_mode
        self.docked = docked
        self.xct_cuelist = xct_cuelist
        self.page = page


class General:
    class Config:
        def __init__(self, update_mode=None, executors_exclusive_mode=None, remove_non_empty_cuelist=None, clear_ltp=None, bpm_mode=None, show_password=None, show_password_enabled=None):
            self.update_mode = update_mode
            self.executors_exclusive_mode = executors_exclusive_mode
            self.remove_non_empty_cuelist = remove_non_empty_cuelist
            self.clear_ltp = clear_ltp
            self.bpm_mode = bpm_mode
            self.show_password = show_password
            self.show_password_enabled = show_password_enabled
    
    def __init__(self, config=None):
        self.config = config if config is not None else self.Config()
