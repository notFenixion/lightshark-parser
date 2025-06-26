from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging


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
