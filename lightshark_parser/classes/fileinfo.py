from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from lightshark_parser.serialisers.attribute_serialisers import *
import logging


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