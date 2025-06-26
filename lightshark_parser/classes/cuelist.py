from __future__ import annotations
from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging

class Cuelist:


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
            "ms_fadeout", "cue_id", "ms_delay", "dotted_id", "ms_fadein", "ms_crossfade",
            "ms_duration"
        ]
        bool_attrs = ["halt"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name == "next":
                    if attr_value == "N/A":
                        bytestr.extend(b'\xFF')
                    else:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    bytestr.extend(serialise_bool_value(attr_value))

        bytestr[0:0] = serialise_num_attr(num_attr)
        logging.info("CuelistElement object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)