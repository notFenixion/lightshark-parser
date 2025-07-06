from __future__ import annotations
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
        # filepath: str = None,
        fileinfo: FileInfo = None,
        models: Dict[int, Model] = None,
        patches: Dict[int, Patch] = None,
        groups: Dict[int, Group] = None,
        user_palettes: Dict[int, UserPalette] = None,
        cues: Dict[int, Cue] = None,
        cuelists: Dict[int, Cuelist] = None,
        playbacks: Dict[str, Playback] = None,
        fxpalettes: Dict[int, FXPalette] = None,
        general: General = None,
    ):  
        # if filepath is not None:
        #     self._filepath = Path(filepath)
        #     if not self._filepath.exists():
        #         raise FileNotFoundError(f"File {filepath} does not exist")
        #     self._filename = self._filepath.name
        #     stats = self._filepath.stat()
        #     created_at = datetime.fromtimestamp(stats.st_ctime)
        #     modified_at = datetime.fromtimestamp(stats.st_mtime)
        #     self._created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        #     self._modified_at = modified_at.strftime("%Y-%m-%d %H:%M:%S")
        # else:
        #     self._filepath = None
        #     self._filename = None
        #     self._created_at = None
        #     self._modified_at = None

        self._parsed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._fileinfo: FileInfo = fileinfo
        self._models: Dict[int, Model] = models
        self._patches: Dict[int, Patch] = patches
        self._groups: Dict[int, Group] = groups
        self._user_palettes: Dict[int, UserPalette] = user_palettes
        self._cues: Dict[int, Cue] = cues
        self._cuelists: Dict[int, Cuelist] = cuelists
        self._playbacks: Dict[str, Playback] = playbacks
        self._fxpalettes: Dict[int, FXPalette] = fxpalettes
        self._general: General = general

    # Getters and setters
    # @property
    # def filepath(self) -> Path:
    #     return self._filepath
        
    # @property
    # def filename(self) -> str:
    #     return self._filename
        
    # @property
    # def parsed_date(self) -> str:
    #     return self._parsed_date
        
    # @property
    # def created_at(self) -> str:
    #     return self._created_at
        
    # @property
    # def modified_at(self) -> str:
    #     return self._modified_at

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

    def add_group(self, group: Group) -> None:
        if group.__class__.__name__ != 'Group':
            raise TypeError("Parameter given must be a Group object")
        self._groups[group.group_id] = group
    
        
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


    def __repr__(self):
        return (
            f"Lightshow(fileinfo={self._fileinfo!r}, models={self._models!r}, "
            f"patches={self._patches!r}, groups={self._groups!r}, "
            f"user_palettes={self._user_palettes!r}, cues={self._cues!r}, "
            f"cuelists={self._cuelists!r}, playbacks={self._playbacks!r}, "
            f"fxpalettes={self._fxpalettes!r}, general={self._general!r})"
        )


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
            # "filepath": str(self._filepath) if self._filepath else None,
            # "filename": self._filename,
            # "parsed_date": self._parsed_date,
            # "created_at": self._created_at,
            # "modified_at": self._modified_at,
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lightshow":
        fileinfo = FileInfo.from_dict(data.get("fileinfo"))
        models = {int(k): Model.from_dict(v) for k, v in data.get("models", {}).items()}
        patches = {int(k): Patch.from_dict(v) for k, v in data.get("patches", {}).items()}
        groups = {int(k): Group.from_dict(v) for k, v in data.get("groups", {}).items()}
        user_palettes = {int(k): UserPalette.from_dict(v) for k, v in data.get("user_palettes", {}).items()}
        cues = {int(k): Cue.from_dict(v) for k, v in data.get("cues", {}).items()}
        cuelists = {int(k): Cuelist.from_dict(v) for k, v in data.get("cuelists", {}).items()}
        playbacks = {str(k): Playback.from_dict(v) for k, v in data.get("playbacks", {}).items()}
        fxpalettes = {int(k): FXPalette.from_dict(v) for k, v in data.get("fxpalettes", {}).items()}
        general = General.from_dict(data.get("general"))
        return cls(
            fileinfo=fileinfo,
            models=models,
            patches=patches,
            groups=groups,
            user_palettes=user_palettes,
            cues=cues,
            cuelists=cuelists,
            playbacks=playbacks,
            fxpalettes=fxpalettes,
            general=general,
        )

    def summarise(self):
        from lightshark_parser.summariser import format_lightshow
        return format_lightshow(self)
    
    def save_lightshow(self, filepath: Union[str, Path]) -> None:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.suffix == ".lshw":
            raise ValueError("Filepath must have .lshw extension")
        
        logging.debug(f"Saving Lightshow to {filepath}")
        with open(filepath, "wb") as f:
            f.write(self.to_bytes())
        logging.info(f"Lightshow saved to {filepath}")


    def to_bytes(self) -> bytes:
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
        
        return result

    def add_patch(self, patch: Patch) -> None:
        if patch.id in self._patches:
            raise ValueError(f"Duplicate patch ID: {patch.id}")
        self._patches[patch.id] = patch

    def add_cue(self, cue: Cue) -> None:
        if cue.cue_id in self._cues:
            raise ValueError(f"Duplicate cue ID: {cue.cue_id}")
        self._cues[cue.cue_id] = cue

    def add_model(self, model: Model) -> None:
        if model.model_id in self._models:
            raise ValueError(f"Duplicate model ID: {model.model_id}")
        self._models[model.model_id] = model

    def add_user_palette(self, palette: UserPalette) -> None:
        if palette.user_palette_id in self._user_palettes:
            raise ValueError(f"Duplicate user_palette_id: {palette.user_palette_id}")
        self._user_palettes[palette.user_palette_id] = palette

    def add_cuelist(self, cuelist: Cuelist) -> None:
        if cuelist.cuelist_id in self._cuelists:
            raise ValueError(f"Duplicate cuelist ID: {cuelist.cuelist_id}")
        self._cuelists[cuelist.cuelist_id] = cuelist

    def add_playback(self, playback: Playback) -> None:
        if playback.combined_id in self._playbacks:
            raise ValueError(f"Duplicate playback ID: {playback.combined_id}")
        self._playbacks[playback.combined_id] = playback

    def add_fxpalette(self, fxpalette: FXPalette) -> None:
        if fxpalette.fx_palette in self._fxpalettes:
            raise ValueError(f"Duplicate FX palette ID: {fxpalette.fx_palette}")
        self._fxpalettes[fxpalette.fx_palette] = fxpalette