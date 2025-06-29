from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from lightshark_parser.serialisers.attribute_serialisers import *
import logging


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
        model_id: Optional[int] = None,
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