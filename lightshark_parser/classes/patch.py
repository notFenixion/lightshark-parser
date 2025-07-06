from __future__ import annotations
from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging

class Patch:
    def __init__(
        self,
        model_id: Optional[int] = None,
        inverse_tilt: Optional[bool] = None,
        name: Optional[str] = None,
        channels_ftype: Optional[List[int]] = None,
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

    def __repr__(self):
        return (
            f"Patch(model_id={self.model_id!r}, inverse_tilt={self.inverse_tilt!r}, "
            f"name={self.name!r}, channels_ftype={self.channels_ftype!r}, "
            f"index={self.index!r}, universe={self.universe!r}, "
            f"description={self.description!r}, inverse_pan={self.inverse_pan!r}, "
            f"visual_id={self.visual_id!r}, parked={self.parked!r}, "
            f"color_mark={self.color_mark!r}, dimmer={self.dimmer!r}, "
            f"swap_pan_tilt={self.swap_pan_tilt!r}, virtual_dimmer={self.virtual_dimmer!r}, "
            f"id={self.id!r}, size={self.size!r}, frozen={self.frozen!r})"
        )

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Patch":
        if data is None:
            return None
        return cls(
            model_id=data.get("model_id"),
            inverse_tilt=data.get("inverse_tilt"),
            name=data.get("name"),
            channels_ftype=data.get("channels_ftype"),
            index=data.get("index"),
            universe=data.get("universe"),
            description=data.get("description"),
            inverse_pan=data.get("inverse_pan"),
            visual_id=data.get("visual_id"),
            parked=data.get("parked"),
            color_mark=data.get("color_mark"),
            dimmer=data.get("dimmer"),
            swap_pan_tilt=data.get("swap_pan_tilt"),
            virtual_dimmer=data.get("virtual_dimmer"),
            id=data.get("id"),
            size=data.get("size"),
            frozen=data.get("frozen"),
        )

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
