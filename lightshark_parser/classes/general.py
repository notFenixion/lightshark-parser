from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging

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

