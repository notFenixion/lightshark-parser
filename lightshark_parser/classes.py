from typing import Dict, List, Any, Optional, TypedDict
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field


class Lightshow:
    def __init__(
        self,
        filepath: str,
        fileinfo: Dict[Any, "FileInfo"] = None,
        models: Dict[Any, "Model"] = None,
        patches: Dict[Any, "Patch"] = None,
        groups: Dict[Any, "Group"] = None,
        user_palettes: Dict[Any, "UserPalette"] = None,
        cues: Dict[Any, "Cue"] = None,
        cuelists: Dict[Any, "Cuelist"] = None,
        playbacks: Dict[Any, "Playback"] = None,
        fxpalettes: Dict[Any, "FXPalette"] = None,
        general: Dict[Any, "General"] = None,
    ):
        self._filepath = Path(filepath)
        if not self._filepath.exists():
            raise FileNotFoundError(f"File {filepath} does not exist")
        self._filename = self._filepath.name
        stats = self._filepath.stat()
        created_at = datetime.fromtimestamp(stats.st_ctime)
        modified_at = datetime.fromtimestamp(stats.st_mtime)
        self._parsed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        self._modified_at = modified_at.strftime("%Y-%m-%d %H:%M:%S")

        # Initialize section attributes with private names
        self._fileinfo: Dict[Any, "FileInfo"] = fileinfo if fileinfo is not None else {}
        self._models: Dict[Any, "Model"] = models if models is not None else {}
        self._patches: Dict[Any, "Patch"] = patches if patches is not None else {}
        self._groups: Dict[Any, "Group"] = groups if groups is not None else {}
        self._user_palettes: Dict[Any, "UserPalette"] = user_palettes if user_palettes is not None else {}
        self._cues: Dict[Any, "Cue"] = cues if cues is not None else {}
        self._cuelists: Dict[Any, "Cuelist"] = cuelists if cuelists is not None else {}
        self._playbacks: Dict[Any, "Playback"] = playbacks if playbacks is not None else {}
        self._fxpalettes: Dict[Any, "FXPalette"] = fxpalettes if fxpalettes is not None else {}
        self._general: Dict[Any, "General"] = general if general is not None else {}

    # Property getters for non-section attributes
    @property
    def filepath(self) -> Path:
        return self._filepath
        
    @property
    def filename(self) -> str:
        return self._filename
        
    @property
    def parsed_date(self) -> str:
        return self._parsed_date
        
    @property
    def created_at(self) -> str:
        return self._created_at
        
    @property
    def modified_at(self) -> str:
        return self._modified_at

    # Property getters for section attributes
    @property
    def fileinfo(self) -> Dict:
        return self._fileinfo
        
    @fileinfo.setter
    def fileinfo(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("fileinfo must be a dictionary")
        from .classes import FileInfo  # Import here to avoid circular imports
        for model in value.values():
            if not isinstance(model, FileInfo):
                raise TypeError("All model values must be FileInfo objects")
        self._fileinfo = value
        
    @property
    def models(self) -> Dict[Any, Any]:
        return self._models
        
    @models.setter
    def models(self, value: Dict[Any, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("models must be a dictionary")
        from .classes import Model  # Import here to avoid circular imports
        for model in value.values():
            if not isinstance(model, Model):
                raise TypeError("All model values must be Model objects")
        self._models = value
        
    @property
    def patches(self) -> Dict[Any, "Patch"]:
        return self._patches
        
    @patches.setter
    def patches(self, value: Dict[Any, "Patch"]) -> None:
        if not isinstance(value, dict):
            raise TypeError("patches must be a dictionary")
        from .classes import Patch  # Import here to avoid circular imports
        for patch in value.values():
            if not isinstance(patch, Patch):
                raise TypeError("All patch values must be Patch objects")
        self._patches = value
        
    @property
    def groups(self) -> Dict[Any, "Group"]:
        return self._groups
        
    @groups.setter
    def groups(self, value: Dict[Any, "Group"]) -> None:
        if not isinstance(value, dict):
            raise TypeError("groups must be a dictionary")
        from .classes import Group  # Import here to avoid circular imports
        for group in value.values():
            if not isinstance(group, Group):
                raise TypeError("All group values must be Group objects")
        self._groups = value
        
    @property
    def user_palettes(self) -> Dict:
        return self._user_palettes
        
    @user_palettes.setter
    def user_palettes(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("user_palettes must be a dictionary")
        # Assuming UserPalette objects have a specific attribute or method
        for palette in value.values():
            if not hasattr(palette, 'user_palette_id'):
                raise TypeError("All user_palette values must be UserPalette objects")
        self._user_palettes = value
        
    @property
    def cues(self) -> Dict:
        return self._cues
        
    @cues.setter
    def cues(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("cues must be a dictionary")
        # Assuming Cue objects have a specific attribute or method
        for cue in value.values():
            if not hasattr(cue, 'cue_id'):
                raise TypeError("All cue values must be Cue objects")
        self._cues = value
        
    @property
    def cuelists(self) -> Dict:
        return self._cuelists
        
    @cuelists.setter
    def cuelists(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("cuelists must be a dictionary")
        # Assuming CueList objects have a specific attribute or method
        for cuelist in value.values():
            if not hasattr(cuelist, 'cuelist_id'):
                raise TypeError("All cuelist values must be CueList objects")
        self._cuelists = value
        
    @property
    def playbacks(self) -> Dict:
        return self._playbacks
        
    @playbacks.setter
    def playbacks(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("playbacks must be a dictionary")
        # Assuming Playback objects have a specific attribute or method
        for playback in value.values():
            if not hasattr(playback, 'playback_id'):
                raise TypeError("All playback values must be Playback objects")
        self._playbacks = value
        
    @property
    def fxpalettes(self) -> Dict:
        return self._fxpalettes
        
    @fxpalettes.setter
    def fxpalettes(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("fxpalettes must be a dictionary")
        # Assuming FXPalette objects have a specific attribute or method
        for fxpalette in value.values():
            if not hasattr(fxpalette, 'fx_palette_id'):
                raise TypeError("All fxpalette values must be FXPalette objects")
        self._fxpalettes = value
        
    @property
    def general(self) -> Dict:
        return self._general
        
    @general.setter
    def general(self, value: Dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("general must be a dictionary")
        # General section might contain mixed types, so we just validate it's a dict
        self._general = value

    def to_dict(self) -> Dict:
        def to_dict_recursive(obj):
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                return obj.to_dict()
            elif hasattr(obj, "__dict__"):
                return {k: to_dict_recursive(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, (list, tuple)):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): to_dict_recursive(v) for k, v in obj.items()}
            return obj

        return {
            "fileinfo": to_dict_recursive(self._fileinfo),
            "models": [to_dict_recursive(model) for model in self._models.values()],
            "patches": [to_dict_recursive(patch) for patch in self._patches.values()],
            "groups": [to_dict_recursive(group) for group in self._groups.values()],
            "user_palettes": {str(k): to_dict_recursive(v) for k, v in self._user_palettes.items()},
            "cues": {str(k): to_dict_recursive(v) for k, v in self._cues.items()},
            "cuelists": {str(k): to_dict_recursive(v) for k, v in self._cuelists.items()},
            "playbacks": {str(k): to_dict_recursive(v) for k, v in self._playbacks.items()},
            "fxpalettes": {str(k): to_dict_recursive(v) for k, v in self._fxpalettes.items()},
            "general": to_dict_recursive(self._general),
        }

    def summarise(self):
        from .summariser import format_lightshow
        return format_lightshow(self)

    def to_bytes(self):
        from .serialiser import serialise_lightshow
        return serialise_lightshow(self)


class FileInfo:
    @dataclass
    class Version:
        subversion: int = None
        version: int = None
        autoload: bool = None
        software: str = None

        def to_dict(self) -> Dict[str, Any]:
            return {
                "subversion": self.subversion,
                "version": self.version,
                "autoload": self.autoload,
                "software": self.software,
            }

        def to_bytes(self):
            content = bytearray()


    def __init__(self, version: Optional[Version] = None):
        self.version = version if version is not None else self.Version()

    def to_dict(self) -> Dict[str, Any]:
        return {"version": self.version.to_dict() if self.version else None}

    def to_bytes(self):
        content = bytearray()
        



@dataclass
class ModelPalette:
    color: Optional[str] = None
    icon: Optional[str] = None
    values: Optional[List[Any]] = field(default_factory=list)
    name: Optional[str] = None
    type_id: Optional[int] = None


@dataclass
class ModelHardware:
    width: Optional[float] = None
    depth: Optional[float] = None
    max_power: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None


@dataclass
class MacroStep:
    ms_wait: Optional[int] = None
    values: Optional[List[Any]] = field(default_factory=list)


@dataclass
class Macro:
    macro_type: Optional[str] = None
    steps: Optional[List[MacroStep]] = field(default_factory=list)
    name: Optional[str] = None


@dataclass
class ModelValueStep:
    step_name: Optional[str] = None
    step_value: Optional[int] = None
    # im not too sure about these 3
    min_str: Optional[str] = None
    max_str: Optional[str] = None
    symbol: Optional[str] = None


@dataclass
class ModelValue:
    index: Optional[int] = None
    inverse: Optional[bool] = None
    instant: Optional[bool] = None
    description: Optional[str] = None
    ftype: Optional[int] = None
    steps: Optional[List[Any]] = field(default_factory=list)
    htp: Optional[bool] = None
    size: Optional[int] = None


class Model:
    def __init__(
        self,
        model_id: int,
        palette: Optional[ModelPalette] = None,
        name: Optional[str] = None,
        short_name: Optional[str] = None,
        default_inverted_pan: Optional[bool] = None,
        brand: Optional[str] = None,
        hardware: Optional[ModelHardware] = None,
        macros: Optional[List[Macro]] = None,
        use_virtual_dimmer: Optional[bool] = None,
        default_inverted_tilt: Optional[bool] = None,
        values: Optional[List[ModelValue]] = None,
        mode_name: Optional[str] = None,
        virtual_dimmer_channels: Optional[List[int]] = None,
        size: Optional[int] = None,
    ) -> None:
        self.model_id = model_id
        self.palette = palette if palette is not None else ModelPalette()
        self.name = name
        self.short_name = short_name
        self.default_inverted_pan = default_inverted_pan
        self.brand = brand
        self.hardware = hardware if hardware is not None else ModelHardware()
        self.macros = macros if macros is not None else []
        self.use_virtual_dimmer = use_virtual_dimmer
        self.default_inverted_tilt = default_inverted_tilt
        self.values = values if values is not None else []
        self.mode_name = mode_name
        self.virtual_dimmer_channels = virtual_dimmer_channels if virtual_dimmer_channels is not None else []
        self.size = size


class Patch:
    def __init__(
        self,
        model_id: Optional[int] = None,
        inverse_tilt: Optional[bool] = None,
        name: Optional[str] = None,
        channels_ftype: Optional[List[str]] = None,
        index: Optional[int] = None,
        universe: Optional[int] = None,
        description: Optional[str] = None,
        inverse_pan: Optional[bool] = None,
        visual_id: Optional[int] = None,
        parked: Optional[bool] = None,
        color_mark: Optional[int] = None,
        dimmer: Optional[List[int]] = None,
        swap_pan_tilt: Optional[bool] = None,
        virtual_dimmer: Optional[List[int]] = None,
        id: Optional[int] = None,
        size: Optional[int] = None,
        frozen: Optional[int] = None,
    ) -> None:
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
        self.frozen: Optional[int] = frozen

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id,
            "inverse_tilt": self.inverse_tilt,
            "name": self.name,
            "channels_ftype": self.channels_ftype,
            "index": self.index,
            "universe": self.universe,
            "description": self.description,
            "inverse_pan": self.inverse_pan,
            "visual_id": self.visual_id,
            "parked": self.parked,
            "color_mark": self.color_mark,
            "dimmer": self.dimmer,
            "swap_pan_tilt": self.swap_pan_tilt,
            "virtual_dimmer": self.virtual_dimmer,
            "id": self.id,
            "size": self.size,
            "frozen": self.frozen,
        }


class Group:
    def __init__(
        self,
        description: Optional[str] = None,
        color_mark: Optional[int] = None,
        visual_id: Optional[int] = None,
        patched_elements_ids: Optional[List[int]] = None,
        grid: Optional[Dict[int, List[int]]] = None,
        steps: Optional[Dict[int, int]] = None,
        automatico: Optional[bool] = None,
        group_id: Optional[int] = None,
    ) -> None:
        self.description: Optional[str] = description
        self.color_mark: Optional[int] = color_mark
        self.visual_id: Optional[int] = visual_id
        self.patched_elements_ids: List[int] = patched_elements_ids if patched_elements_ids is not None else []
        self.grid: Dict[int, List[int]] = grid if grid is not None else {}
        self.steps: Dict[int, int] = steps if steps is not None else {}
        self.automatico: Optional[bool] = automatico
        self.group_id: Optional[int] = group_id

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "color_mark": self.color_mark,
            "visual_id": self.visual_id,
            "patched_elements_ids": self.patched_elements_ids,
            "grid": {str(k): v for k, v in self.grid.items()},
            "steps": {str(k): v for k, v in self.steps.items()},
            "automatico": self.automatico,
            "group_id": self.group_id,
        }


class UserPalette:
    def __init__(
        self,
        section: int = None,
        user_palette_id: int = None,
        name: str = None,
        icon: str = None,
        orders: Optional[List["Order"]] = None,
    ) -> None:
        self.section: int = section
        self.user_palette_id: int = user_palette_id
        self.name: str = name
        self.icon: str = icon
        self.orders: List["Order"] = orders if orders is not None else []

    def to_dict(self) -> dict:
        return {
            "section": self.section,
            "user_palette_id": self.user_palette_id,
            "name": self.name,
            "icon": self.icon,
            "orders": [order.to_dict() if hasattr(order, "to_dict") else order for order in self.orders],
        }


class Order:
    def __init__(
        self,
        palette_id: int = None,
        universe: int = None,
        section: int = None,
        receptor_type: int = None,
        patch_id: int = None,
        ftype: str = None,
        value: int = None,
        channel: int = None,
    ) -> None:
        self.palette_id: int = palette_id
        self.universe: int = universe
        self.section: int = section
        self.receptor_type: int = receptor_type
        self.patch_id: int = patch_id
        self.ftype: str = ftype
        self.value: int = value
        self.channel: int = channel

    def to_dict(self) -> dict:
        return {
            "palette_id": self.palette_id,
            "universe": self.universe,
            "section": self.section,
            "receptor_type": self.receptor_type,
            "patch_id": self.patch_id,
            "ftype": self.ftype,
            "value": self.value,
            "channel": self.channel,
        }


class Cue:
    def __init__(
        self,
        fx_palette: int = None,
        cue_id: int = None,
        description: str = None,
        visual_id: int = None,
        fxs: List["FX"] = None,
        fxs_channels: List[dict] = None,
        orders: List[Order] = None,
        actions: List["Action"] = None,
        name: str = None,
    ) -> None:
        self.fx_palette: int = fx_palette
        self.cue_id: int = cue_id
        self.description: str = description
        self.visual_id: int = visual_id
        self.fxs: List["FX"] = fxs if fxs is not None else []
        self.fxs_channels: List[dict] = fxs_channels if fxs_channels is not None else []
        self.orders: List[Order] = orders if orders is not None else []
        self.actions: List["Action"] = actions if actions is not None else []
        self.name: str = name

    def to_dict(self) -> dict:
        def convert_bytes(obj):
            if isinstance(obj, bytes):
                # Convert bytes to a string of Unicode escape sequences (e.g., b'\x02\x04' -> '\\u0002\\u0004')
                return "".join(f"\\u{byte:04x}" for byte in obj)
            elif isinstance(obj, dict):
                return {str(k): convert_bytes(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_bytes(item) for item in obj]
            return obj

        converted_fxs_channels = convert_bytes(self.fxs_channels)
        fxs_list = []
        for fx in self.fxs:
            if hasattr(fx, "to_dict"):
                fxs_list.append(fx.to_dict())
            elif hasattr(fx, "__dict__"):
                fxs_list.append(fx.__dict__)
            else:
                fxs_list.append(fx)

        # Convert orders
        orders_list = []
        for order in self.orders:
            if hasattr(order, "to_dict"):
                orders_list.append(order.to_dict())
            elif hasattr(order, "__dict__"):
                orders_list.append(order.__dict__)
            else:
                orders_list.append(order)

        return {
            "fx_palette": self.fx_palette,
            "cue_id": self.cue_id,
            "description": self.description,
            "visual_id": self.visual_id,
            "actions": self.actions,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": converted_fxs_channels,
            "orders": orders_list,
            "name": self.name,
        }


class FX:
    class FXLayer:
        def __init__(
            self,
            blind: bool = None,
            phase_offset: int = None,
            section: int = None,
            curve: int = None,
            steps: List["FX.FXLayerSteps"] = None,
            ftypes: List[str] = None,
            id: int = None,
            size: int = None,
        ) -> None:
            self.blind: bool = blind
            self.phase_offset: int = phase_offset
            self.section: int = section
            self.curve: int = curve
            self.steps: List["FX.FXLayerSteps"] = steps if steps is not None else []
            self.ftypes: List[str] = ftypes if ftypes is not None else []
            self.id: int = id
            self.size: int = size

        def to_dict(self) -> dict:
            steps_list = []
            for step in self.steps:
                if hasattr(step, "to_dict"):
                    steps_list.append(step.to_dict())
                elif hasattr(step, "__dict__"):
                    steps_list.append(step.__dict__)
                else:
                    steps_list.append(step)

            return {
                "blind": self.blind,
                "phase_offset": self.phase_offset,
                "section": self.section,
                "curve": self.curve,
                "steps": steps_list,
                "ftypes": self.ftypes,
                "id": self.id,
                "size": self.size,
            }

    class FXLayerStep:
        def __init__(
            self,
            start_limit: int = None,
            palette_type: int = None,
            name: str = None,
            ancho: int = None,
            curve_in: int = None,
            curve_out: int = None,
            strength: int = None,
            curve_type: int = None,
            palette_value: Any = None,
            inicio: int = None,
            end_limit: int = None,
            jumps: int = None,
        ) -> None:
            self.start_limit: int = start_limit
            self.palette_type: int = palette_type
            self.name: str = name
            self.ancho: int = ancho
            self.curve_in: int = curve_in
            self.curve_out: int = curve_out
            self.strength: int = strength
            self.curve_type: int = curve_type
            self.palette_value: Any = palette_value
            self.inicio: int = inicio
            self.end_limit: int = end_limit
            self.jumps: int = jumps

        def to_dict(self) -> dict:
            return {
                "start_limit": self.start_limit,
                "palette_type": self.palette_type,
                "name": self.name,
                "ancho": self.ancho,
                "curve_in": self.curve_in,
                "curve_out": self.curve_out,
                "strength": self.strength,
                "curve_type": self.curve_type,
                "palette_value": self.palette_value,
                "inicio": self.inicio,
                "end_limit": self.end_limit,
                "jumps": self.jumps,
            }

    def __init__(
        self,
        cyclos: int = None,
        direction: int = None,
        speed: int = None,
        group_steps: int = None,
        size: int = None,
        layers: List[FXLayer] = None,
        patches: List[int] = None,
        speed_in_bpm: bool = None,
        width: int = None,
        spread: int = None,
        basic: bool = None,
        gfxid: int = None,
        internal_speed: int = None,
        fx_ref: int = None,
        splits: int = None,
        groups: List[int] = None,
        rect_width: int = None,
        name: str = None,
        phase_offset: int = None,
        bpm: int = None,
        render_id: int = None,
        mode: int = None,
        repeats: int = None,
        rect_height: int = None,
    ) -> None:
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
        # Convert layers to their dictionary representation
        layers_list = []
        for layer in self.layers:
            if hasattr(layer, "to_dict"):
                layers_list.append(layer.to_dict())
            elif hasattr(layer, "__dict__"):
                layers_list.append(layer.__dict__)
            else:
                layers_list.append(layer)

        return {
            # Single byte attributes
            "cyclos": self.cyclos,
            "direction": self.direction,
            "group_steps": self.group_steps,
            "gfxid": self.gfxid,
            "splits": self.splits,
            "rect_width": self.rect_width,
            "render_id": self.render_id,
            "mode": self.mode,
            "repeats": self.repeats,
            "rect_height": self.rect_height,
            # Multibyte attributes
            "speed": self.speed,
            "size": self.size,
            "width": self.width,
            "spread": self.spread,
            "internal_speed": self.internal_speed,
            "fx_ref": self.fx_ref,
            "phase_offset": self.phase_offset,
            "bpm": self.bpm,
            # String attribute
            "name": self.name,
            # Boolean attributes
            "speed_in_bpm": self.speed_in_bpm,
            "basic": self.basic,
            # List attributes
            "patches": self.patches,
            "groups": self.groups,
            # Object attributes
            "layers": [layer.to_dict() for layer in self.layers] if hasattr(self, "layers") else [],
        }


class Cuelist:
    class CuelistElement:
        def __init__(
            self,
            ms_fadeout: Optional[int] = None,
            cue_id: Optional[int] = None,
            ms_delay: Optional[int] = None,
            next: Optional[int] = None,
            dotted_id: Optional[str] = None,
            ms_fadein: Optional[int] = None,
            ms_crossfade: Optional[int] = None,
            ms_duration: Optional[int] = None,
            halt: Optional[bool] = None,
        ) -> None:
            self.ms_fadeout: Optional[int] = ms_fadeout
            self.cue_id: Optional[int] = cue_id
            self.ms_delay: Optional[int] = ms_delay
            self.next: Optional[int] = next
            self.dotted_id: Optional[str] = dotted_id
            self.ms_fadein: Optional[int] = ms_fadein
            self.ms_crossfade: Optional[int] = ms_crossfade
            self.ms_duration: Optional[int] = ms_duration
            self.halt: Optional[bool] = halt

        def to_dict(self) -> dict:
            return {
                "ms_fadeout": self.ms_fadeout,
                "cue_id": self.cue_id,
                "ms_delay": self.ms_delay,
                "next": self.next,
                "dotted_id": self.dotted_id,
                "ms_fadein": self.ms_fadein,
                "ms_crossfade": self.ms_crossfade,
                "ms_duration": self.ms_duration,
                "halt": self.halt,
            }

    def __init__(
        self,
        ms_flash_attack: Optional[int] = None,
        autoreset: Optional[bool] = None,
        at_end_pause: Optional[bool] = None,
        loops: Optional[int] = None,
        chase: Optional[bool] = None,
        ms_chase_time: Optional[int] = None,
        visual_id: Optional[int] = None,
        bpm_chase: Optional[bool] = None,
        ms_flash_decay: Optional[int] = None,
        pcrossfade: Optional[bool] = None,
        ms_fadeout: Optional[int] = None,
        direction: Optional[int] = None,
        at_end_stop: Optional[bool] = None,
        flash_mode: Optional[bool] = None,
        cuelist_id: Optional[int] = None,
        ms_fadein: Optional[int] = None,
        ms_crossfade: Optional[int] = None,
        no_first_fade: Optional[bool] = None,
        name: Optional[str] = None,
        block_fx: Optional[bool] = None,
        cuelist_elements: Optional[List[Dict]] = None,
        ms_flash_hold: Optional[int] = None,
        ms_stop_time: Optional[int] = None,
    ) -> None:
        self.ms_flash_attack: Optional[int] = ms_flash_attack
        self.ms_flash_decay: Optional[int] = ms_flash_decay
        self.ms_flash_hold: Optional[int] = ms_flash_hold
        self.ms_chase_time: Optional[int] = ms_chase_time
        self.ms_fadein: Optional[int] = ms_fadein
        self.ms_fadeout: Optional[int] = ms_fadeout
        self.ms_crossfade: Optional[int] = ms_crossfade
        self.ms_stop_time: Optional[int] = ms_stop_time
        self.autoreset: Optional[bool] = autoreset
        self.chase: Optional[bool] = chase
        self.bpm_chase: Optional[bool] = bpm_chase
        self.pcrossfade: Optional[bool] = pcrossfade
        self.at_end_pause: Optional[bool] = at_end_pause
        self.at_end_stop: Optional[bool] = at_end_stop
        self.flash_mode: Optional[bool] = flash_mode
        self.no_first_fade: Optional[bool] = no_first_fade
        self.block_fx: Optional[bool] = block_fx
        self.loops: Optional[int] = loops
        self.visual_id: Optional[int] = visual_id
        self.direction: Optional[int] = direction
        self.cuelist_id: Optional[int] = cuelist_id
        self.name: Optional[str] = name
        self.cuelist_elements: List[CuelistElement] = [
            CuelistElement(**element) if isinstance(element, dict) else element for element in (cuelist_elements or [])
        ]

    def to_dict(self) -> dict:
        return {
            "ms_flash_attack": self.ms_flash_attack,
            "autoreset": self.autoreset,
            "at_end_pause": self.at_end_pause,
            "loops": self.loops,
            "chase": self.chase,
            "ms_chase_time": self.ms_chase_time,
            "visual_id": self.visual_id,
            "bpm_chase": self.bpm_chase,
            "ms_flash_decay": self.ms_flash_decay,
            "pcrossfade": self.pcrossfade,
            "ms_fadeout": self.ms_fadeout,
            "direction": self.direction,
            "at_end_stop": self.at_end_stop,
            "flash_mode": self.flash_mode,
            "cuelist_id": self.cuelist_id,
            "ms_fadein": self.ms_fadein,
            "ms_crossfade": self.ms_crossfade,
            "no_first_fade": self.no_first_fade,
            "name": self.name,
            "block_fx": self.block_fx,
            "cuelist_elements": [elem.to_dict() for elem in self.cuelist_elements],
            "ms_flash_hold": self.ms_flash_hold,
            "ms_stop_time": self.ms_stop_time,
        }


class Playback:
    def __init__(
        self,
        fader_value=None,
        on_load_play=None,
        fader_mode=None,
        chase=None,
        index=None,
        ms_chase_time=None,
        fader_up_play=None,
        priority=None,
        bpm_chase=None,
        on_page_stop=None,
        trigger_level=None,
        is_executor=None,
        pcrossfade=None,
        ms_fadeout=None,
        fader_down_stop=None,
        ignore_swap=None,
        swap_always=None,
        ms_fadein=None,
        ms_crossfade=None,
        on_page_play=None,
        xct_color=None,
        cuelist=None,
        xct_push_mode=None,
        docked=None,
        xct_cuelist=None,
        page=None,
        ignore_grand_master=None,
        used_in_alarm=None,
        xct_swap=None,
    ):
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
        self.ignore_swap = ignore_swap,
        self.swap_always = swap_always,
        self.ms_fadein = ms_fadein
        self.ms_crossfade = ms_crossfade
        self.on_page_play = on_page_play
        self.xct_color = xct_color
        self.cuelist = cuelist
        self.xct_push_mode = xct_push_mode
        self.docked = docked
        self.xct_cuelist = xct_cuelist
        self.page = page
        self.ignore_grand_master = ignore_grand_master
        self.used_in_alarm = used_in_alarm
        self.xct_swap = xct_swap

    @property
    def combined_id(self):
        """Return a combined ID using both page and index in the format 'page.index'"""
        return f"{self.page}.{self.index}" if self.page is not None and self.index is not None else str(self.index)

    def to_dict(self) -> dict:
        return {
            "fader_value": self.fader_value,
            "on_load_play": self.on_load_play,
            "fader_mode": self.fader_mode,
            "chase": self.chase,
            "index": self.index,
            "ms_chase_time": self.ms_chase_time,
            "fader_up_play": self.fader_up_play,
            "priority": self.priority,
            "bpm_chase": self.bpm_chase,
            "on_page_stop": self.on_page_stop,
            "trigger_level": self.trigger_level,
            "is_executor": self.is_executor,
            "pcrossfade": self.pcrossfade,
            "ms_fadeout": self.ms_fadeout,
            "fader_down_stop": self.fader_down_stop,
            "ignore_swap": self.ignore_swap,
            "swap_always": self.swap_always,
            "ms_fadein": self.ms_fadein,
            "ms_crossfade": self.ms_crossfade,
            "on_page_play": self.on_page_play,
            "xct_color": self.xct_color,
            "cuelist": self.cuelist,
            "xct_push_mode": self.xct_push_mode,
            "docked": self.docked,
            "used_in_alarm": self.used_in_alarm,
            "xct_cuelist": self.xct_cuelist,
            "page": self.page,
            "ignore_grand_master": self.ignore_grand_master,
            "combined_id": self.combined_id,
            "xct_swap": self.xct_swap,
        }


class General:
    class Config:
        def __init__(
            self,
            update_mode=None,
            executors_exclusive_mode=None,
            remove_non_empty_cuelist=None,
            clear_ltp=None,
            bpm_mode=None,
            show_password=None,
            show_password_enabled=None,
        ):
            self.update_mode = update_mode
            self.executors_exclusive_mode = executors_exclusive_mode
            self.remove_non_empty_cuelist = remove_non_empty_cuelist
            self.clear_ltp = clear_ltp
            self.bpm_mode = bpm_mode
            self.show_password = show_password
            self.show_password_enabled = show_password_enabled

    def __init__(self, config=None):
        self.config = config if config is not None else self.Config()


class FXPalette:
    def __init__(
        self,
        fx_palette: int = None,
        cue_id: int = None,
        visual_id: int = None,
        fxs: List["FX"] = None,
        fxs_channels: List[dict] = None,
        orders: List[Order] = None,
        name: str = None,
    ) -> None:
        self.fx_palette: int = fx_palette
        self.cue_id: int = cue_id
        self.visual_id: int = visual_id
        self.fxs: List["FX"] = fxs if fxs is not None else []
        self.fxs_channels: List[dict] = fxs_channels if fxs_channels is not None else []
        self.orders: List[Order] = orders if orders is not None else []
        self.name: str = name

    def to_dict(self) -> dict:
        def convert_bytes(obj):
            if isinstance(obj, bytes):
                # Convert bytes to a string of Unicode escape sequences (e.g., b'\x02\x04' -> '\\u0002\\u0004')
                return "".join(f"\\u{byte:04x}" for byte in obj)
            elif isinstance(obj, dict):
                return {str(k): convert_bytes(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_bytes(item) for item in obj]
            return obj

        converted_fxs_channels = convert_bytes(self.fxs_channels)
        fxs_list = []
        for fx in self.fxs:
            if hasattr(fx, "to_dict"):
                fxs_list.append(fx.to_dict())
            elif hasattr(fx, "__dict__"):
                fxs_list.append(fx.__dict__)
            else:
                fxs_list.append(fx)
        orders_list = []
        for order in self.orders:
            if hasattr(order, "to_dict"):
                orders_list.append(order.to_dict())
            elif hasattr(order, "__dict__"):
                orders_list.append(order.__dict__)
            else:
                orders_list.append(order)

        return {
            "fx_palette": self.fx_palette,
            "cue_id": self.cue_id,
            "visual_id": self.visual_id,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": converted_fxs_channels,
            "orders": orders_list,
            "name": self.name,
        }
