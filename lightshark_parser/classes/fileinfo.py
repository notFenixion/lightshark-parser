from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from lightshark_parser.serialisers.attribute_serialisers import *
import logging



@dataclass
class Version:
    subversion: int = None
    version: int = None
    autoload: bool = None
    software: str = None


    def __repr__(self):
        return f"Version(subversion={self.subversion!r}, version={self.version!r}, autoload={self.autoload!r}, software={self.software!r})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subversion": self.subversion,
            "version": self.version,
            "autoload": self.autoload,
            "software": self.software,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Version":
        return cls(
            subversion=data.get("subversion"),
            version=data.get("version"),
            autoload=data.get("autoload"),
            software=data.get("software"),
        )

    def to_bytes(self):
        logging.debug(f"Starting serialization of Version object")
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
        

class FileInfo:


    def __init__(self, version: Optional[Version] = None):
        self.version = version if version is not None else self.Version()


    def __repr__(self):
        return f"FileInfo(version={self.version!r})"



    def to_dict(self) -> Dict[str, Any]:
        return {"version": self.version.to_dict() if self.version else None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileInfo":
        if data is None:
            return None
        version = Version.from_dict(data.get("version")) if data.get("version") else None
        return cls(version=version)

    def to_bytes(self):
        logging.debug(f"Starting serialization of FileInfo section")
        bytestr = bytearray(serialise_section_header("#fileinfo#"))
        for obj in self.__dict__.values():
            if obj is not None:
                bytestr.extend(obj.to_bytes())
        logging.info("FileInfo section serialised")
        logging.debug(bytestr)
        return bytes(bytestr)