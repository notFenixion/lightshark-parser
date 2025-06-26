from typing import Dict, Any, Optional, Union
from pathlib import Path
from datetime import datetime
from lightshark_parser.serialisers.attribute_serialisers import *
import logging
from lightshark_parser.classes.fileinfo import FileInfo
from lightshark_parser.classes.model import Model
from lightshark_parser.classes.patch import Patch
from lightshark_parser.classes.group import Group
from lightshark_parser.classes.user_palette import UserPalette
from lightshark_parser.classes.cue import Cue
from lightshark_parser.classes.cuelist import Cuelist
from lightshark_parser.classes.playback import Playback
from lightshark_parser.classes.fx import FXPalette
from lightshark_parser.classes.general import General


class Lightshow:
    def __init__(
        self,
        filepath: str,
        fileinfo: FileInfo = None,
        models: Dict[Any, Model] = None,
        patches: Dict[Any, Patch] = None,
        groups: Dict[Any, Group] = None,
        user_palettes: Dict[Any, UserPalette] = None,
        cues: Dict[Any, Cue] = None,
        cuelists: Dict[Any, Cuelist] = None,
        playbacks: Dict[Any, Playback] = None,
        fxpalettes: Dict[Any, FXPalette] = None,
        general: General = None,
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

        self._fileinfo: FileInfo = fileinfo
        self._models: Dict[Any, Model] = models
        self._patches: Dict[Any, Patch] = patches
        self._groups: Dict[Any, Group] = groups
        self._user_palettes: Dict[Any, UserPalette] = user_palettes
        self._cues: Dict[Any, Cue] = cues
        self._cuelists: Dict[Any, Cuelist] = cuelists
        self._playbacks: Dict[Any, Playback] = playbacks
        self._fxpalettes: Dict[Any, FXPalette] = fxpalettes
        self._general: General = general

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
    def fileinfo(self) -> FileInfo:
        return self._fileinfo
        
    @fileinfo.setter
    def fileinfo(self, value: FileInfo) -> None:
        self._fileinfo = value
        
    @property
    def models(self) -> Dict[Any, Model]:
        return self._models
        
    @models.setter
    def models(self, value: Dict[Any, Model]) -> None:
        for model in value.values():
            if model.__class__.__name__ != 'Model':
                raise TypeError("All model values must be Model objects")
        self._models = value
        
    @property
    def patches(self) -> Dict[Any, Patch]:
        return self._patches
        
    @patches.setter
    def patches(self, value: Dict[Any, Patch]) -> None:
        for patch in value.values():
            if patch.__class__.__name__ != 'Patch':
                raise TypeError("All patch values must be Patch objects")
        self._patches = value
        
    @property
    def groups(self) -> Dict[Any, Group]:
        return self._groups
        
    @groups.setter
    def groups(self, value: Dict[Any, Group]) -> None:
        for group in value.values():
            if group.__class__.__name__ != 'Group':
                raise TypeError("All group values must be Group objects")
        self._groups = value
        
    @property
    def user_palettes(self) -> Dict[Any, UserPalette]:
        return self._user_palettes
        
    @user_palettes.setter
    def user_palettes(self, value: Dict[Any, UserPalette]) -> None:
        for palette in value.values():
            if palette.__class__.__name__ != 'UserPalette':
                raise TypeError("All user_palette values must be UserPalette objects")
        self._user_palettes = value
        
    @property
    def cues(self) -> Dict[Any, Cue]:
        return self._cues
        
    @cues.setter
    def cues(self, value: Dict[Any, Cue]) -> None:
        for cue in value.values():
            if cue.__class__.__name__ != 'Cue':
                raise TypeError("All cue values must be Cue objects")
        self._cues = value
        
    @property
    def cuelists(self) -> Dict[Any, Cuelist]:
        return self._cuelists
        
    @cuelists.setter
    def cuelists(self, value: Dict[Any, Cuelist]) -> None:
        for cuelist in value.values():
            if cuelist.__class__.__name__ != 'Cuelist':
                raise TypeError("All cuelist values must be Cuelist objects")
        self._cuelists = value
        
    @property
    def playbacks(self) -> Dict[Any, Playback]:
        return self._playbacks
        
    @playbacks.setter
    def playbacks(self, value: Dict[Any, Playback]) -> None:
        for playback in value.values():
            if playback.__class__.__name__ != 'Playback':
                raise TypeError("All playback values must be Playback objects")
        self._playbacks = value
        
    @property
    def fxpalettes(self) -> Dict[Any, FXPalette]:
        return self._fxpalettes
        
    @fxpalettes.setter
    def fxpalettes(self, value: Dict[Any, FXPalette]) -> None:
        for fxpalette in value.values():
            if fxpalette.__class__.__name__ != 'FXPalette':
                raise TypeError("All fxpalette values must be FXPalette objects")
        self._fxpalettes = value
        
    @property
    def general(self) -> General:
        return self._general
        
    @general.setter
    def general(self, value: General) -> None:
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
        from lightshark_parser.summariser import format_lightshow
        return format_lightshow(self)

    def to_bytes(self, filepath: Optional[Union[str, Path]] = None) -> bytes:
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
        
        result = bytes(bytestr)
        
        # If filepath is provided, write the bytes to the file
        if filepath is not None:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(result)
            logging.info(f"Lightshow saved to {filepath}")
        
        return result