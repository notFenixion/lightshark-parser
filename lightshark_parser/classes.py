from typing import Dict, List, Any, Optional, TypedDict
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from .serialisers.attribute_serialisers import *
import logging


class Lightshow:
    def __init__(
        self,
        filepath: str,
        fileinfo: "FileInfo" = None,
        models: Dict[Any, "Model"] = None,
        patches: Dict[Any, "Patch"] = None,
        groups: Dict[Any, "Group"] = None,
        user_palettes: Dict[Any, "UserPalette"] = None,
        cues: Dict[Any, "Cue"] = None,
        cuelists: Dict[Any, "Cuelist"] = None,
        playbacks: Dict[Any, "Playback"] = None,
        fxpalettes: Dict[Any, "FXPalette"] = None,
        general: "General" = None,
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

        self._fileinfo: "FileInfo" = fileinfo
        self._models: Dict[Any, "Model"] = models
        self._patches: Dict[Any, "Patch"] = patches
        self._groups: Dict[Any, "Group"] = groups
        self._user_palettes: Dict[Any, "UserPalette"] = user_palettes
        self._cues: Dict[Any, "Cue"] = cues
        self._cuelists: Dict[Any, "Cuelist"] = cuelists
        self._playbacks: Dict[Any, "Playback"] = playbacks
        self._fxpalettes: Dict[Any, "FXPalette"] = fxpalettes
        self._general: "General" = general

    # Getters and setters
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
    def fileinfo(self) -> "FileInfo":
        return self._fileinfo
        
    @fileinfo.setter
    def fileinfo(self, value: "FileInfo") -> None:
        self._fileinfo = value
        
    @property
    def models(self) -> Dict[Any, Any]:
        return self._models
        
    @models.setter
    def models(self, value: Dict[Any, Any]) -> None:
        for model in value.values():
            if model.__class__.__name__ != 'Model':
                raise TypeError("All model values must be Model objects")
        self._models = value
        
    @property
    def patches(self) -> Dict[Any, "Patch"]:
        return self._patches
        
    @patches.setter
    def patches(self, value: Dict[Any, "Patch"]) -> None:
        for patch in value.values():
            if patch.__class__.__name__ != 'Patch':
                raise TypeError("All patch values must be Patch objects")
        self._patches = value
        
    @property
    def groups(self) -> Dict[Any, "Group"]:
        return self._groups
        
    @groups.setter
    def groups(self, value: Dict[Any, "Group"]) -> None:
        for group in value.values():
            if group.__class__.__name__ != 'Group':
                raise TypeError("All group values must be Group objects")
        self._groups = value
        
    @property
    def user_palettes(self) -> Dict:
        return self._user_palettes
        
    @user_palettes.setter
    def user_palettes(self, value: Dict) -> None:
        for palette in value.values():
            if palette.__class__.__name__ != 'UserPalette':
                raise TypeError("All user_palette values must be UserPalette objects")
        self._user_palettes = value
        
    @property
    def cues(self) -> Dict:
        return self._cues
        
    @cues.setter
    def cues(self, value: Dict) -> None:
        for cue in value.values():
            if cue.__class__.__name__ != 'Cue':
                raise TypeError("All cue values must be Cue objects")
        self._cues = value
        
    @property
    def cuelists(self) -> Dict:
        return self._cuelists
        
    @cuelists.setter
    def cuelists(self, value: Dict) -> None:
        for cuelist in value.values():
            if cuelist.__class__.__name__ != 'Cuelist':
                raise TypeError("All cuelist values must be Cuelist objects")
        self._cuelists = value
        
    @property
    def playbacks(self) -> Dict:
        return self._playbacks
        
    @playbacks.setter
    def playbacks(self, value: Dict) -> None:
        for playback in value.values():
            if playback.__class__.__name__ != 'Playback':
                raise TypeError("All playback values must be Playback objects")
        self._playbacks = value
        
    @property
    def fxpalettes(self) -> Dict:
        return self._fxpalettes
        
    @fxpalettes.setter
    def fxpalettes(self, value: Dict) -> None:
        for fxpalette in value.values():
            if fxpalette.__class__.__name__ != 'FXPalette':
                raise TypeError("All fxpalette values must be FXPalette objects")
        self._fxpalettes = value
        
    @property
    def general(self) -> "General":
        return self._general
        
    @general.setter
    def general(self, value: "General") -> None:
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
            "models": {str(k): to_dict_recursive(v) for k, v in self._models.items()} if self._models else {},
            "patches": {str(k): to_dict_recursive(v) for k, v in self._patches.items()} if self._patches else {},
            "groups": {str(k): to_dict_recursive(v) for k, v in self._groups.items()} if self._groups else {},
            "user_palettes": {str(k): to_dict_recursive(v) for k, v in self._user_palettes.items()} if self._user_palettes else {},
            "cues": {str(k): to_dict_recursive(v) for k, v in self._cues.items()} if self._cues else {},
            "cuelists": {str(k): to_dict_recursive(v) for k, v in self._cuelists.items()} if self._cuelists else {},
            "playbacks": {str(k): to_dict_recursive(v) for k, v in self._playbacks.items()} if self._playbacks else {},
            "fxpalettes": {str(k): to_dict_recursive(v) for k, v in self._fxpalettes.items()} if self._fxpalettes else {},
            "general": to_dict_recursive(self._general),
        }

    def summarise(self):
        from .summariser import format_lightshow
        return format_lightshow(self)

    def to_bytes(self):
        logging.debug(f"Starting serialization of Lightshow object")
        bytestr = bytearray()
        if self._fileinfo is not None:
            bytestr.extend(self._fileinfo.to_bytes())

        bytestr.extend(serialise_section_header("#models#"))
        if self._models is not None:
            for model in self._models.values():
                bytestr.extend(model.to_bytes()) 

        bytestr.extend(serialise_section_header("#patching#"))
        if self._patches is not None:
            for patch in self._patches.values():
                bytestr.extend(patch.to_bytes())
        if self._groups is not None:
            for group in self._groups.values():
                bytestr.extend(group.to_bytes())
        
        bytestr.extend(serialise_section_header("#user_palettes#"))
        if self._user_palettes is not None:
            for palette in self._user_palettes.values():
                bytestr.extend(palette.to_bytes())

        bytestr.extend(serialise_section_header("#cues#"))
        if self._cues is not None:
            for cue in self._cues.values():
                bytestr.extend(cue.to_bytes())
        
        bytestr.extend(serialise_section_header("#cuelists#"))
        if self._cuelists is not None:
            for cuelist in self._cuelists.values():
                bytestr.extend(cuelist.to_bytes())
        
        bytestr.extend(serialise_section_header("#playbacks#"))
        if self._playbacks is not None:
            for playback in self._playbacks.values():
                bytestr.extend(playback.to_bytes())

        if self._general is not None:
            bytestr.extend(self._general.to_bytes())

        bytestr.extend(serialise_section_header("#fxpalettes#"))
        if self._fxpalettes is not None:
            for fxpalette in self._fxpalettes.values():
                bytestr.extend(fxpalette.to_bytes())
        
        bytestr.extend(serialise_section_header("#end#"))

        return bytestr


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
            logging.debug(f"Starting serialization of FileInfo.Version object")
            bytestr = bytearray(serialise_section_header("version"))

            content = bytearray()
            num_attr = 0
            
            num_attrs = ["subversion", "version"]
            bool_attrs = ["autoload"]
            string_attrs = ["software"]
            
            for attr_name, value in self.__dict__.items():
                if value is not None:
                    content.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        content.extend(serialise_num_value(value))
                    elif attr_name in bool_attrs:
                        content.extend(serialise_bool_value(value))
                    elif attr_name in string_attrs:
                        content.extend(serialise_str_value(value))

            content[0:0] = serialise_num_attr(num_attr)
            
            bytestr.extend(serialise_content_length(content))
            bytestr.extend(content)
            logging.info("FileInfo version object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)


    def __init__(self, version: Optional[Version] = None):
        self.version = version if version is not None else self.Version()

    def to_dict(self) -> Dict[str, Any]:
        return {"version": self.version.to_dict() if self.version else None}

    def to_bytes(self):
        logging.debug(f"Starting serialization of FileInfo section")
        bytestr = bytearray(serialise_section_header("#fileinfo#"))
        for obj in self.__dict__.values():
            if obj is not None:
                bytestr.extend(obj.to_bytes())
        logging.info("FileInfo section serialised")
        logging.debug(bytestr)
        return bytes(bytestr)
        



@dataclass
class ModelPalette:
    color: Optional[str] = None
    icon: Optional[str] = None
    # Values List[int,int] corresponds to [ftype, value]
    values: Optional[dict[int, int]] = None
    name: Optional[str] = None
    type_id: Optional[str] = None

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of ModelPalette")
        bytestr = bytearray()
        num_attr = 0
        
        string_attrs = ["name", "icon", "color", "type_id"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name == "values":
                    num_values = len(attr_value)
                    bytestr.extend(serialise_objlist_len(num_values))
                    for ftype, value in attr_value.items():
                        bytestr.extend(b'\x92')
                        bytestr.extend(serialise_num_value(ftype, cc_check=True))
                        bytestr.extend(serialise_num_value(value, cc_check=True))

        bytestr[0:0] = serialise_num_attr(num_attr)
        
        logging.info("ModelPalette object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


@dataclass
class ModelHardware:
    width: Optional[str] = None
    depth: Optional[str] = None
    max_power: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None


    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of ModelHardware")
        bytestr = bytearray()
        num_attr = 0
        
        string_attrs = ["width", "depth", "max_power", "weight", "height"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))

        bytestr[0:0] = serialise_num_attr(num_attr)
        
        logging.info("ModelHardware object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


@dataclass
class MacroStep:
    ms_wait: Optional[int] = None
    values: Optional[List[Any]] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of MacroStep")
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = ["ms_wait"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value))
                elif attr_name == "values":
                    num_values = len(attr_value)
                    bytestr.extend(serialise_objlist_len(num_values))
                    for value in attr_value:
                        if len(value) != 2:
                            raise ValueError("Value list must contain exactly 2 elements")
                        bytestr.extend(b'\x92')
                        bytestr.extend(serialise_str_value(value["name"]))
                        bytestr.extend(serialise_num_value(value["value"], cc_check=True))

        bytestr[0:0] = serialise_num_attr(num_attr)
        
        logging.info("MacroStep object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


@dataclass
class Macro:
    macro_type: Optional[str] = None
    steps: Optional[List[MacroStep]] = field(default_factory=list)
    name: Optional[str] = None

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Macro")
        bytestr = bytearray()
        num_attr = 0
        
        string_attrs = ["name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None and attr_name != "macro_type":  # macro_type is handled separately
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name == "steps":
                    num_steps = len(attr_value)
                    bytestr.extend(serialise_objlist_len(num_steps))
                    for step in attr_value:
                        bytestr.extend(step.to_bytes())
        

        bytestr[0:0] = serialise_str_value(self.macro_type) + serialise_num_attr(num_attr)
        
        logging.info("Macro object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


@dataclass
class ModelValueStep:
    step_name: Optional[str] = None
    step_value: Optional[int] = None
    # im not too sure about these 3
    min_str: Optional[str] = None
    max_str: Optional[str] = None
    symbol: Optional[str] = None


    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of ModelValueStep")
        bytestr = bytearray()
        num_attr = 0
        
        string_attrs = ["step_name", "min_str", "max_str", "symbol"]
        num_attrs = ["step_value"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                num_attr += 1

                if attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))

        if num_attr != 5:
            raise ValueError("ModelValueStep object should have exactly 5 attributes. (NOTE: Unconfirmed)")
        bytestr[0:0] = serialise_objlist_len(num_attr)
        
        logging.info("ModelValueStep object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


@dataclass
class ModelValue:
    index: Optional[int] = None
    inverse: Optional[bool] = None
    instant: Optional[bool] = None
    description: Optional[str] = None
    ftype: Optional[int] = None
    steps: Optional[dict[int, ModelValueStep]] = field(default_factory=dict)
    htp: Optional[bool] = None
    size: Optional[int] = None

    def to_bytes(self) -> bytes:
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = ["index", "ftype", "size"]
        string_attrs = ["description"]
        bool_attrs = ["inverse", "instant", "htp"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value))
                elif attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name in bool_attrs:
                    bytestr.extend(serialise_bool_value(attr_value))
                elif attr_name == "steps":
                    num_steps = len(attr_value)
                    bytestr.extend(serialise_num_attr(num_steps))
                    for id, step in attr_value.items():
                        bytestr.extend(serialise_num_value(id, cc_check=True))
                        bytestr.extend(step.to_bytes())

        bytestr[0:0] = serialise_num_attr(num_attr)
        
        logging.info("ModelValue object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


class Model:
    def __init__(
        self,
        model_id: int,
        palette: Optional[Dict[str, ModelPalette]] = None,
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
        self.palette = palette
        self.name = name
        self.short_name = short_name
        self.default_inverted_pan = default_inverted_pan
        self.brand = brand
        self.hardware = hardware
        self.macros = macros
        self.use_virtual_dimmer = use_virtual_dimmer
        self.default_inverted_tilt = default_inverted_tilt
        self.values = values
        self.mode_name = mode_name
        self.virtual_dimmer_channels = virtual_dimmer_channels
        self.size = size

    def to_bytes(self):
        logging.debug(f"Starting serialization of Model {getattr(self, 'name', '')} (id: {getattr(self, 'model_id', 'N/A')})")
        bytestr = bytearray(serialise_section_header("model"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["model_id", "size"]
        bool_attrs = ["default_inverted_pan", "default_inverted_tilt", "use_virtual_dimmer"]
        string_attrs = ["name", "short_name", "brand", "mode_name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == "palette":
                    num_palettes = len(attr_value)
                    content.extend(serialise_num_attr(num_palettes))
                    for palette_id, palette in attr_value.items():
                        content.extend(serialise_num_value(int(palette_id)))
                        content.extend(palette.to_bytes())
                elif attr_name == "hardware":
                    content.extend(attr_value.to_bytes())
                elif attr_name == "macros":
                    num_macros = len(attr_value)
                    content.extend(serialise_num_attr(num_macros))
                    for macro in attr_value.values():
                        content.extend(macro.to_bytes())
                elif attr_name == "values":
                    num_values = len(attr_value)
                    has_virtual_intensity = any(value.description == "Intensity (Virtual)" for value in attr_value)
                    if has_virtual_intensity:
                        num_values -= 1
                    
                    content.extend(serialise_objlist_len(num_values))
                    for value in attr_value:
                        if value.description == "Intensity (Virtual)":
                            continue
                        content.extend(value.to_bytes())
                elif attr_name == "virtual_dimmer_channels":
                    content.extend(serialise_num_list(attr_value))

        content[0:0] = serialise_num_attr(num_attr)
        
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Model object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


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
        self.channels_ftype: List[int] = channels_ftype
        self.index: Optional[int] = index
        self.universe: Optional[int] = universe
        self.description: Optional[str] = description
        self.inverse_pan: Optional[bool] = inverse_pan
        self.visual_id: Optional[int] = visual_id
        self.parked: Optional[bool] = parked
        self.color_mark: Optional[int] = color_mark
        self.dimmer: List[int] = dimmer
        self.swap_pan_tilt: Optional[bool] = swap_pan_tilt
        self.virtual_dimmer: List[int] = virtual_dimmer
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

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Patch object {self.name} (ID: {self.id})")
        bytestr = bytearray(serialise_section_header("patch"))

        content = bytearray()
        num_attr = 0
        
        num_attrs = ["model_id", "index", "universe", "visual_id", "color_mark", "id", "size", "frozen"]
        string_attrs = ["name", "description"]
        bool_attrs = ["inverse_tilt", "inverse_pan", "parked", "swap_pan_tilt"]
        num_list_attrs = ["channels_ftype", "virtual_dimmer"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in num_list_attrs:
                    content.extend(serialise_num_list(attr_value, cc_check=True))
                elif attr_name == "dimmer":
                    if len(attr_value) != 8:
                        raise ValueError("dimmer should contain exactly 8 elements (NOTE: unconfirmed)")
                    dimmer_content = bytearray(serialise_num_list(attr_value))
                    dimmer_content[0] = 0xCB  # Convert to integer for bytearray assignment
                    content.extend(dimmer_content)


        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Patch object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


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
        self.patched_elements_ids: List[int] = patched_elements_ids
        self.grid: Dict[int, List[int]] = grid
        self.steps: Dict[int, int] = steps
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

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Group object {self.description} (id: {self.group_id})")
        bytestr = bytearray(serialise_section_header("group"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["group_id", "visual_id", "color_mark"]
        string_attrs = ["description"]
        bool_attrs = ["automatico"]
        num_list_attrs = ["patched_elements_ids"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in num_list_attrs:
                    content.extend(serialise_num_list(attr_value, cc_check=True))
                elif attr_name == "grid":
                    num_fixtures = len(attr_value)
                    content.extend(serialise_num_attr(num_fixtures))
                    for fixture_id, fixture_pos in attr_value.items():
                        content.extend(serialise_num_value(int(fixture_id)))
                        content.extend(serialise_num_list(fixture_pos))
                elif attr_name in ["steps"]:
                    num_steps = len(attr_value)
                    content.extend(serialise_num_attr(num_steps))
                    for step_id, step in attr_value.items():
                        content.extend(serialise_num_value(int(step_id)))
                        content.extend(serialise_num_value(step))

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Group object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)

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
        self.orders: List["Order"] = orders

    def to_dict(self) -> dict:
        return {
            "section": self.section,
            "user_palette_id": self.user_palette_id,
            "name": self.name,
            "icon": self.icon,
            "orders": [order.to_dict() if hasattr(order, "to_dict") else order for order in self.orders],
        }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of UserPalette object {self.name} (id: {self.user_palette_id})")
        bytestr = bytearray(serialise_section_header("user_palette"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["section", "user_palette_id"]
        string_attrs = ["name", "icon"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == "orders":
                    num_orders = len(attr_value)
                    content.extend(serialise_objlist_len(num_orders))
                    for order in attr_value:
                        content.extend(order.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("UserPalette object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


class Order:
    def __init__(
        self,
        palette_id: int = None,
        universe: int = None,
        section: int = None,
        receptor_type: int = None,
        patch_id: int = None,
        ftype: int = None,
        value: int = None,
        channel: int = None,
    ) -> None:
        self.palette_id: int = palette_id
        self.universe: int = universe
        self.section: int = section
        self.receptor_type: int = receptor_type
        self.patch_id: int = patch_id
        self.ftype: int = ftype
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

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Order object for palette ID: {self.palette_id})")
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = ["palette_id", "universe", "section", "receptor_type", "ftype", "patch_id", "value", "channel"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))

        bytestr[0:0] = serialise_num_attr(num_attr)
        logging.info("Order object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)

class Cue:
    def __init__(
        self,
        fx_palette: Optional[int] = None,
        cue_id: Optional[int] = None,
        description: Optional[str] = None,
        visual_id: Optional[int] = None,
        fxs: Optional[List["FX"]] = None,
        fxs_channels: Optional[List[Dict[int, Any]]] = None,
        orders: Optional[List[Order]] = None,
        actions: Optional[List["Action"]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fx_palette: int = fx_palette
        self.cue_id: int = cue_id
        self.description: str = description
        self.visual_id: int = visual_id
        self.fxs: List["FX"] = fxs
        self.fxs_channels: List[dict] = fxs_channels
        self.orders: List[Order] = orders
        self.actions: List["Action"] = actions
        self.name: str = name

    def to_dict(self) -> dict:
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
            "description": self.description,
            "visual_id": self.visual_id,
            "actions": self.actions,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": self.fxs_channels,
            "orders": orders_list,
            "name": self.name,
        }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Cue object {self.name} (id: {self.cue_id})")
        bytestr = bytearray(serialise_section_header("cue"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["cue_id", "visual_id"]
        string_attrs = ["description", "name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_name == "fx_palette" or attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name == "fx_palette":
                    if attr_value is None:
                        content.extend(b'\xFF')
                    else:
                        content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == 'fxs_channels':
                    num_lists = len(attr_value)
                    content.extend(serialise_objlist_len(num_lists))
                    for fx_channel in attr_value:
                        list_content = bytearray()
                        list_len = sum(1 for value in fx_channel if not isinstance(value, str))
                        if list_len != 16:
                            raise ValueError("FX channel list length should be 16 (NOTE: unconfirmed. though this error shouldn't happen either way...)")
                        list_content.extend(serialise_objlist_len(list_len))
                        for value in fx_channel:
                            # \xd1 \x?? instances
                            if isinstance(value, str):
                                list_content.extend(bytes.fromhex(value))
                            else:
                                list_content.extend(serialise_num_value(value, cc_check=True))
                        content.extend(list_content)

                elif attr_name == 'fxs':
                    num_fxs = len(attr_value)
                    content.extend(serialise_objlist_len(num_fxs))
                    for fx in attr_value:
                        content.extend(fx.to_bytes())
                elif attr_name == 'orders':
                    num_orders = len(attr_value)
                    content.extend(serialise_objlist_len(num_orders))
                    for order in attr_value:
                        content.extend(order.to_bytes())
                elif attr_name == 'actions':
                    raise NotImplementedError("Actions not implemented yet")
                    # num_actions = len(attr_value)
                    # bytestr.extend(serialise_objlist_len(num_actions))
                    # for action in attr_value:
                    #     bytestr.extend(action.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Cue object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


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
            self.steps: List["FX.FXLayerSteps"] = steps
            self.ftypes: List[int] = ftypes
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

        def to_bytes(self) -> bytes:
            logging.debug(f"Starting serialization of FXLayer object {self.id}")
            bytestr = bytearray()
            num_attr = 0
            
            num_attrs = ["id", "phase_offset", "section", "curve", "size"]
            bool_attrs = ["blind"]
            num_list_attrs = ["ftypes"]
            
            for attr_name, attr_value in self.__dict__.items():
                if attr_value is not None:
                    bytestr.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                    elif attr_name in bool_attrs:
                        bytestr.extend(serialise_bool_value(attr_value))
                    elif attr_name in num_list_attrs:
                        bytestr.extend(serialise_num_list(attr_value, cc_check=True))
                    elif attr_name == "steps":
                        num_steps = len(attr_value)
                        bytestr.extend(serialise_objlist_len(num_steps))
                        for step in attr_value:
                            bytestr.extend(step.to_bytes())

            bytestr[0:0] = serialise_num_attr(num_attr)
            logging.info("FXLayer object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)

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

        def to_bytes(self) -> bytes:
            logging.debug(f"Starting serialization of FXLayerStep object {self.name}")
            bytestr = bytearray()
            num_attr = 0
            
            num_attrs = [
                "start_limit", "palette_type", "ancho", "curve_in", "curve_out",
                "strength", "curve_type", "palette_value", "inicio", "end_limit", "jumps"
            ]
            string_attrs = ["name"]
            
            for attr_name, attr_value in self.__dict__.items():
                if attr_value is not None:
                    bytestr.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                    elif attr_name in string_attrs:
                        bytestr.extend(serialise_str_value(attr_value))

            bytestr[0:0] = serialise_num_attr(num_attr)
            logging.info("FXLayerStep object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)

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
        # Attributes ordered to match to_dict()
        self.cyclos: int = cyclos
        self.direction: int = direction
        self.speed: int = speed
        self.group_steps: int = group_steps
        self.size: int = size
        self.layers: List[FX.FXLayer] = layers
        self.patches: List[int] = patches
        self.speed_in_bpm: bool = speed_in_bpm
        self.width: int = width
        self.spread: int = spread
        self.basic: bool = basic
        self.gfxid: int = gfxid
        self.internal_speed: int = internal_speed
        self.fx_ref: int = fx_ref
        self.splits: int = splits
        self.groups: List[int] = groups
        self.rect_width: int = rect_width
        self.name: str = name
        self.phase_offset: int = phase_offset
        self.bpm: int = bpm
        self.render_id: int = render_id
        self.mode: int = mode
        self.repeats: int = repeats
        self.rect_height: int = rect_height

    def to_dict(self) -> dict:
        return {
        "cyclos": self.cyclos,
        "direction": self.direction,
        "speed": self.speed,
        "group_steps": self.group_steps,
        "size": self.size,
        "layers": [layer.to_dict() for layer in self.layers] if self.layers else [],
        "patches": self.patches,
        "speed_in_bpm": self.speed_in_bpm,
        "width": self.width,
        "spread": self.spread,
        "basic": self.basic,
        "gfxid": self.gfxid,
        "internal_speed": self.internal_speed,
        "fx_ref": self.fx_ref,
        "splits": self.splits,
        "groups": self.groups,
        "rect_width": self.rect_width,
        "name": self.name,
        "phase_offset": self.phase_offset,
        "bpm": self.bpm,
        "render_id": self.render_id,
        "mode": self.mode,
        "repeats": self.repeats,
        "rect_height": self.rect_height
    }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of FX object {self.name}")
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = [
            "cyclos", "direction", "group_steps", "gfxid", "splits", "rect_width",
            "render_id", "mode", "repeats", "rect_height", "speed", "size",
            "width", "spread", "internal_speed", "fx_ref", "phase_offset", "bpm"
        ]
        bool_attrs = ["speed_in_bpm", "basic"]
        string_attrs = ["name"]
        num_list_attrs = ["patches", "groups"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    bytestr.extend(serialise_bool_value(attr_value))
                elif attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name in num_list_attrs:
                    bytestr.extend(serialise_num_list(attr_value))
                elif attr_name == "layers":
                    num_layers = len(attr_value)
                    bytestr.extend(serialise_objlist_len(num_layers))
                    for layer in attr_value:
                        bytestr.extend(layer.to_bytes())

        bytestr[0:0] = serialise_num_attr(num_attr)
        logging.info("FX object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


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

        def to_bytes(self) -> bytes:
            logging.debug(f"Starting serialization of CuelistElement object {self.cue_id}")
            bytestr = bytearray()
            num_attr = 0
            
            num_attrs = [
                "ms_fadeout", "cue_id", "ms_delay", "next", "dotted_id", "ms_fadein", "ms_crossfade",
                "ms_duration"
            ]
            bool_attrs = ["halt"]
            
            for attr_name, attr_value in self.__dict__.items():
                if attr_value is not None:
                    bytestr.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                    elif attr_name in bool_attrs:
                        bytestr.extend(serialise_bool_value(attr_value))

            bytestr[0:0] = serialise_num_attr(num_attr)
            logging.info("CuelistElement object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)

    def __init__(
        self,
        ms_flash_attack: Optional[int] = None,
        autoreset: Optional[bool] = None,
        at_end_pause: Optional[bool] = None,
        loops: Optional[int] = None,
        chase: Optional[bool] = None,
        ms_chase_time: Optional[int] = None,
        visual_id: Optional[int] = None,
        bpm_chase: Optional[int] = None,
        ms_flash_decay: Optional[int] = None,
        pcrossfade: Optional[int] = None,
        ms_fadeout: Optional[int] = None,
        direction: Optional[int] = None,
        at_end_stop: Optional[bool] = None,
        flash_mode: Optional[int] = None,
        cuelist_id: Optional[int] = None,
        ms_fadein: Optional[int] = None,
        ms_crossfade: Optional[int] = None,
        no_first_fade: Optional[bool] = None,
        name: Optional[str] = None,
        block_fx: Optional[bool] = None,
        cuelist_elements: Optional[List[CuelistElement]] = None,
        ms_flash_hold: Optional[int] = None,
        ms_stop_time: Optional[int] = None,
    ) -> None:
        # Match the order from to_dict()
        self.ms_flash_attack: Optional[int] = ms_flash_attack
        self.autoreset: Optional[bool] = autoreset
        self.at_end_pause: Optional[bool] = at_end_pause
        self.loops: Optional[int] = loops
        self.chase: Optional[bool] = chase
        self.ms_chase_time: Optional[int] = ms_chase_time
        self.visual_id: Optional[int] = visual_id
        self.bpm_chase: Optional[int] = bpm_chase
        self.ms_flash_decay: Optional[int] = ms_flash_decay
        self.pcrossfade: Optional[int] = pcrossfade
        self.ms_fadeout: Optional[int] = ms_fadeout
        self.direction: Optional[int] = direction
        self.at_end_stop: Optional[bool] = at_end_stop
        self.flash_mode: Optional[int] = flash_mode
        self.cuelist_id: Optional[int] = cuelist_id
        self.ms_fadein: Optional[int] = ms_fadein
        self.ms_crossfade: Optional[int] = ms_crossfade
        self.no_first_fade: Optional[bool] = no_first_fade
        self.name: Optional[str] = name
        self.block_fx: Optional[bool] = block_fx
        self.cuelist_elements: List[CuelistElement] = cuelist_elements
        self.ms_flash_hold: Optional[int] = ms_flash_hold
        self.ms_stop_time: Optional[int] = ms_stop_time

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

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialisation of Cuelist object {self.name}")
        bytestr = bytearray(serialise_section_header("cuelist"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = [
            "ms_flash_attack", "ms_flash_decay", "ms_flash_hold", "ms_chase_time", "ms_fadein", "ms_fadeout",
            "ms_crossfade", "ms_stop_time", "visual_id", "bpm_chase", "pcrossfade", "direction", "flash_mode", "cuelist_id", "loops"
        ]
        bool_attrs = ["autoreset", "chase", "at_end_pause", "at_end_stop", "no_first_fade", "block_fx"]
        string_attrs = ["name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == "cuelist_elements":
                    num_elements = len(attr_value) if attr_value else 0
                    content.extend(serialise_objlist_len(num_elements))
                    if attr_value:  # Only process if there are elements
                        for element in attr_value:
                            content.extend(element.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Cuelist object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


class Playback:
    def __init__(
        self,
        fader_value: Optional[int] = None,
        on_load_play: Optional[bool] = None,
        fader_mode: Optional[int] = None,
        chase: Optional[bool] = None,
        index: Optional[int] = None,
        ms_chase_time: Optional[int] = None,
        fader_up_play: Optional[bool] = None,
        priority: Optional[int] = None,
        bpm_chase: Optional[int] = None,
        on_page_stop: Optional[bool] = None,
        trigger_level: Optional[int] = None,
        is_executor: Optional[bool] = None,
        pcrossfade: Optional[int] = None,
        ms_fadeout: Optional[int] = None,
        fader_down_stop: Optional[bool] = None,
        ignore_swap: Optional[bool] = None,
        swap_always: Optional[bool] = None,
        ms_fadein: Optional[int] = None,
        ms_crossfade: Optional[int] = None,
        on_page_play: Optional[bool] = None,
        xct_color: Optional[List[int]] = None,
        cuelist: Optional[int] = None,
        xct_push_mode: Optional[List[bool]] = None,
        docked: Optional[bool] = None,
        used_in_alarm: Optional[bool] = None,
        xct_cuelist: Optional[List[int]] = None,
        page: Optional[int] = None,
        ignore_grand_master: Optional[bool] = None,
        xct_swap: Optional[List[bool]] = None,
    ) -> None:
        self.fader_value: Optional[int] = fader_value
        self.on_load_play: Optional[bool] = on_load_play
        self.fader_mode: Optional[int] = fader_mode
        self.chase: Optional[bool] = chase
        self.index: Optional[int] = index
        self.ms_chase_time: Optional[int] = ms_chase_time
        self.fader_up_play: Optional[bool] = fader_up_play
        self.priority: Optional[int] = priority
        self.bpm_chase: Optional[int] = bpm_chase
        self.on_page_stop: Optional[bool] = on_page_stop
        self.trigger_level: Optional[int] = trigger_level
        self.is_executor: Optional[bool] = is_executor
        self.pcrossfade: Optional[int] = pcrossfade
        self.ms_fadeout: Optional[int] = ms_fadeout
        self.fader_down_stop: Optional[bool] = fader_down_stop
        self.ignore_swap: Optional[bool] = ignore_swap
        self.swap_always: Optional[bool] = swap_always
        self.ms_fadein: Optional[int] = ms_fadein
        self.ms_crossfade: Optional[int] = ms_crossfade
        self.on_page_play: Optional[bool] = on_page_play
        self.xct_color: Optional[List[int]] = xct_color
        self.cuelist: Optional[int] = cuelist
        self.xct_push_mode: Optional[List[bool]] = xct_push_mode
        self.docked: Optional[bool] = docked
        self.used_in_alarm: Optional[bool] = used_in_alarm
        self.xct_cuelist: Optional[List[int]] = xct_cuelist
        self.page: Optional[int] = page
        self.ignore_grand_master: Optional[bool] = ignore_grand_master
        self.xct_swap: Optional[List[bool]] = xct_swap

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

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialisation of Playback object {self.combined_id}")
        bytestr = bytearray(serialise_section_header("playback"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = [
            "fader_value", "fader_mode", "index", "ms_chase_time", "priority", "bpm_chase", "trigger_level", "pcrossfade", "ms_fadeout", "ms_fadein",
            "ms_crossfade", "cuelist", "page"
        ]
        bool_attrs = [
            "on_load_play", "chase", "fader_up_play", "on_page_stop", "is_executor", "fader_down_stop", "ignore_swap",
            "swap_always", "on_page_play", "docked", "used_in_alarm", "ignore_grand_master"
        ]
        num_list_attrs = ["xct_color", "xct_cuelist"]
        bool_list_attrs = ["xct_push_mode", "xct_swap"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in num_list_attrs:
                    content.extend(serialise_num_list(attr_value))
                elif attr_name in bool_list_attrs:
                    content.extend(serialise_bool_list(attr_value))

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Playback object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)

class General:
    class Config:
        def __init__(
            self,
            update_mode: Optional[int] = None,
            executors_exclusive_mode: Optional[bool] = None,
            remove_non_empty_cuelist: Optional[bool] = None,
            clear_ltp: Optional[bool] = None,
            bpm_mode: Optional[bool] = None,
            show_password: Optional[str] = None,
            show_password_enabled: Optional[bool] = None,
        ) -> None:
            self.update_mode: Optional[int] = update_mode
            self.executors_exclusive_mode: Optional[bool] = executors_exclusive_mode
            self.remove_non_empty_cuelist: Optional[bool] = remove_non_empty_cuelist
            self.clear_ltp: Optional[bool] = clear_ltp
            self.bpm_mode: Optional[bool] = bpm_mode
            self.show_password: Optional[str] = show_password
            self.show_password_enabled: Optional[bool] = show_password_enabled

        def to_dict(self) -> dict:
            return {
                "update_mode": self.update_mode,
                "executors_exclusive_mode": self.executors_exclusive_mode,
                "remove_non_empty_cuelist": self.remove_non_empty_cuelist,
                "clear_ltp": self.clear_ltp,
                "bpm_mode": self.bpm_mode,
                "show_password": self.show_password,
                "show_password_enabled": self.show_password_enabled
            }

        def to_bytes(self) -> bytes:
            logging.debug("Starting serialisation of General.Config object")
            bytestr = bytearray(serialise_section_header("config"))
            content = bytearray()
            num_attr = 0
            
            num_attrs = ["update_mode"]
            bool_attrs = ["executors_exclusive_mode", "remove_non_empty_cuelist", "clear_ltp", "bpm_mode", "show_password_enabled"]
            string_attrs = ["show_password"]

            for attr_name, attr_value in self.__dict__.items():
                if attr_value is not None:
                    content.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        content.extend(serialise_num_value(attr_value, cc_check=True))
                    elif attr_name in bool_attrs:
                        content.extend(serialise_bool_value(attr_value))
                    elif attr_name in string_attrs:
                        content.extend(serialise_str_value(attr_value))

            content[0:0] = serialise_num_attr(num_attr)
            bytestr.extend(serialise_content_length(content))
            bytestr.extend(content)
            logging.info("General.Config object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config: Optional[General.Config] = config

    def to_dict(self) -> dict:
        return {
            "config": self.config.to_dict() if self.config else None
        }

    def to_bytes(self) -> bytes:
        logging.debug("Starting serialisation of General object")
        bytestr = bytearray(serialise_section_header("#general#"))
        content = bytearray()
        
        if self.config is not None:
            content.extend(self.config.to_bytes())

        bytestr.extend(content)
        logging.info("General object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)


class FXPalette:
    def __init__(
        self,
        fx_palette: Optional[int] = None,
        cue_id: Optional[int] = None,
        description: Optional[str] = None,
        visual_id: Optional[int] = None,
        fxs: Optional[List["FX"]] = None,
        fxs_channels: Optional[List[Dict[str, Any]]] = None,
        orders: Optional[List[Order]] = None,
        actions: Optional[List["Action"]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fx_palette: Optional[int] = fx_palette
        self.cue_id: Optional[int] = cue_id
        self.description: Optional[str] = description
        self.visual_id: Optional[int] = visual_id
        self.fxs: List["FX"] = fxs
        self.fxs_channels: List[Dict[str, Any]] = fxs_channels 
        self.orders: List[Order] = orders
        self.actions: List["Action"] = actions
        self.name: Optional[str] = name

    def to_dict(self) -> dict:
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
            "description": self.description,
            "visual_id": self.visual_id,
            "actions": self.actions,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": self.fxs_channels,
            "orders": orders_list,
            "name": self.name,
        }
        
    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of FXPalette object {self.name} (id: {self.fx_palette})")
        bytestr = bytearray(serialise_section_header("fxpalette"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["fx_palette", "cue_id", "visual_id"]
        string_attrs = ["description", "name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == 'fxs_channels':
                    num_lists = len(attr_value)
                    content.extend(serialise_objlist_len(num_lists))
                    for fx_channel in attr_value:
                        list_content = bytearray()
                        logging.debug(fx_channel)
                        list_len = sum(1 for value in fx_channel if not isinstance(value, str))
                        if list_len != 16:
                            raise ValueError(f"FX channel list length should be 16, {list_len} detected (NOTE: unconfirmed. though this error shouldn't happen either way...)")
                        list_content.extend(serialise_objlist_len(list_len))
                        for value in fx_channel:
                            # \xd1 \x?? instances
                            if isinstance(value, str):
                                list_content.extend(bytes.fromhex(value))
                            else:
                                list_content.extend(serialise_num_value(value, cc_check=True))
                        content.extend(list_content)
                elif attr_name == 'fxs':
                    num_fxs = len(attr_value)
                    content.extend(serialise_objlist_len(num_fxs))
                    for fx in attr_value:
                        content.extend(fx.to_bytes())
                elif attr_name == 'orders':
                    num_orders = len(attr_value)
                    content.extend(serialise_objlist_len(num_orders))
                    for order in attr_value:
                        content.extend(order.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("FXPalette object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)
