from __future__ import annotations
from typing import Dict, List, Any, Optional, Union
from lightshark_parser.serialisers.attribute_serialisers import *
from lightshark_parser.utils.logger import logger

class Cuelist:

    def __init__(
        self,
        ms_flash_attack: Optional[int] = 2000,
        autoreset: Optional[bool] = True,
        at_end_pause: Optional[bool] = False,
        loops: Optional[int] = 1,
        chase: Optional[bool] = False,
        ms_chase_time: Optional[int] = 2000,
        visual_id: Optional[int] = None,
        bpm_chase: Optional[int] = 30000,
        ms_flash_decay: Optional[int] = 2000,
        pcrossfade: Optional[int] = 100000,
        ms_fadeout: Optional[int] = 2000,
        direction: Optional[int] = 0,
        at_end_stop: Optional[bool] = False,
        flash_mode: Optional[int] = 0,
        cuelist_id: Optional[int] = None,
        ms_fadein: Optional[int] = 2000,
        ms_crossfade: Optional[int] = 2000,
        no_first_fade: Optional[bool] = False,
        name: Optional[str] = None,
        block_fx: Optional[bool] = False,
        cuelist_elements: Optional[Dict[int, CuelistElement]] = None,
        ms_flash_hold: Optional[int] = 2000,
        ms_stop_time: Optional[int] = 2000,
    ) -> None:
        
        if name is None:
            name = f"Cuelist {cuelist_id}"


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
        self.cuelist_elements: Dict[int, CuelistElement] = cuelist_elements if cuelist_elements is not None else {}
        self.ms_flash_hold: Optional[int] = ms_flash_hold
        self.ms_stop_time: Optional[int] = ms_stop_time

    def __repr__(self):
        return (
            f"Cuelist(ms_flash_attack={self.ms_flash_attack!r}, autoreset={self.autoreset!r}, "
            f"at_end_pause={self.at_end_pause!r}, loops={self.loops!r}, chase={self.chase!r}, "
            f"ms_chase_time={self.ms_chase_time!r}, visual_id={self.visual_id!r}, "
            f"bpm_chase={self.bpm_chase!r}, ms_flash_decay={self.ms_flash_decay!r}, "
            f"pcrossfade={self.pcrossfade!r}, ms_fadeout={self.ms_fadeout!r}, "
            f"direction={self.direction!r}, at_end_stop={self.at_end_stop!r}, "
            f"flash_mode={self.flash_mode!r}, cuelist_id={self.cuelist_id!r}, "
            f"ms_fadein={self.ms_fadein!r}, ms_crossfade={self.ms_crossfade!r}, "
            f"no_first_fade={self.no_first_fade!r}, name={self.name!r}, block_fx={self.block_fx!r}, "
            f"cuelist_elements={self.cuelist_elements!r}, "
            f"ms_flash_hold={self.ms_flash_hold!r}, ms_stop_time={self.ms_stop_time!r})"
        )


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
            "cuelist_elements": {dotted_id: elem.to_dict() for dotted_id, elem in self.cuelist_elements.items()},
            "ms_flash_hold": self.ms_flash_hold,
            "ms_stop_time": self.ms_stop_time,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Cuelist":
        if data is None:
            return None
        cuelist_elements = {int(dotted_id): CuelistElement.from_dict(elem) for dotted_id, elem in data.get("cuelist_elements", {}).items()}
        return cls(
            ms_flash_attack=data.get("ms_flash_attack"),
            autoreset=data.get("autoreset"),
            at_end_pause=data.get("at_end_pause"),
            loops=data.get("loops"),
            chase=data.get("chase"),
            ms_chase_time=data.get("ms_chase_time"),
            visual_id=data.get("visual_id"),
            bpm_chase=data.get("bpm_chase"),
            ms_flash_decay=data.get("ms_flash_decay"),
            pcrossfade=data.get("pcrossfade"),
            ms_fadeout=data.get("ms_fadeout"),
            direction=data.get("direction"),
            at_end_stop=data.get("at_end_stop"),
            flash_mode=data.get("flash_mode"),
            cuelist_id=data.get("cuelist_id"),
            ms_fadein=data.get("ms_fadein"),
            ms_crossfade=data.get("ms_crossfade"),
            no_first_fade=data.get("no_first_fade"),
            name=data.get("name"),
            block_fx=data.get("block_fx"),
            cuelist_elements=cuelist_elements,
            ms_flash_hold=data.get("ms_flash_hold"),
            ms_stop_time=data.get("ms_stop_time"),
        )

    def to_bytes(self) -> bytes:
        logger.debug(f"Starting serialisation of Cuelist object {self.name}")
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
                        # Sort by dotted_id to maintain consistent order
                        for dotted_id in sorted(attr_value.keys()):
                            element = attr_value[dotted_id]
                            content.extend(element.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logger.info("Cuelist object serialised")
        logger.debug(bytestr)
        return bytes(bytestr)


class CuelistElement:
    def __init__(
        self,
        ms_fadeout: Optional[int] = None,
        cue_id: Optional[int] = None,
        ms_delay: Optional[int] = None,
        next: Optional[Union[int, str]] = "Next",
        dotted_id: Optional[int] = None,
        ms_fadein: Optional[int] = None,
        ms_crossfade: Optional[int] = None,
        ms_duration: Optional[int] = None,
        halt: Optional[bool] = None,
    ) -> None:
        self.ms_fadeout: Optional[int] = ms_fadeout
        self.cue_id: Optional[int] = cue_id
        self.ms_delay: Optional[int] = ms_delay
        self.next: Optional[Union[int, str]] = next
        self.dotted_id: Optional[int] = dotted_id
        self.ms_fadein: Optional[int] = ms_fadein
        self.ms_crossfade: Optional[int] = ms_crossfade
        self.ms_duration: Optional[int] = ms_duration
        self.halt: Optional[bool] = halt


    def __repr__(self):
        return (
            f"CuelistElement(ms_fadeout={self.ms_fadeout!r}, cue_id={self.cue_id!r}, "
            f"ms_delay={self.ms_delay!r}, next={self.next!r}, dotted_id={self.dotted_id!r}, "
            f"ms_fadein={self.ms_fadein!r}, ms_crossfade={self.ms_crossfade!r}, "
            f"ms_duration={self.ms_duration!r}, halt={self.halt!r})"
        )

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CuelistElement":
        # Handle migration from "N/A" to "Next"
        next_value = data.get("next")
        if next_value == "N/A":
            next_value = "Next"
        
        return cls(
            ms_fadeout=data.get("ms_fadeout"),
            cue_id=data.get("cue_id"),
            ms_delay=data.get("ms_delay"),
            next=next_value,
            dotted_id=data.get("dotted_id"),
            ms_fadein=data.get("ms_fadein"),
            ms_crossfade=data.get("ms_crossfade"),
            ms_duration=data.get("ms_duration"),
            halt=data.get("halt"),
        )

    def to_bytes(self) -> bytes:
        logger.debug(f"Starting serialization of CuelistElement object {self.cue_id}")
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
                    if attr_value == "Next" or attr_value == "N/A":
                        bytestr.extend(b'\xFF')
                    else:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    bytestr.extend(serialise_bool_value(attr_value))

        bytestr[0:0] = serialise_num_attr(num_attr)
        logger.info("CuelistElement object serialised")
        logger.debug(bytestr)
        return bytes(bytestr)