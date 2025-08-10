from __future__ import annotations
from typing import Dict, List, Any, Optional, Union
from lightshark_parser.serialisers.attribute_serialisers import *
from lightshark_parser.utils.logger import logger

class Playback:
    def __init__(
        self,
        index: int,
        page: int,
        cuelist: int,
        fader_value: int = 0,
        on_load_play: bool = False,
        fader_mode: int = 256,
        chase: bool = False,
        ms_chase_time: int = 2000,
        fader_up_play: bool = True,
        priority: int = 1,
        bpm_chase: int = 30000,
        on_page_stop: bool = False,
        trigger_level: int = 0,
        is_executor: bool = False,
        pcrossfade: int = 100000,
        ms_fadeout: int = 2000,
        fader_down_stop: bool = True,
        ignore_swap: Optional[bool] = None,
        swap_always: Optional[bool] = None,
        ms_fadein: int = 2000,
        ms_crossfade: int = 2000,
        on_page_play: bool = False,
        xct_color: Optional[List[int]] = None,
        xct_push_mode: Optional[List[bool]] = None,
        docked: bool = False,
        used_in_alarm: Optional[bool] = None,
        xct_cuelist: Optional[List[int]] = None,
        ignore_grand_master: Optional[bool] = None,
        xct_swap: Optional[List[bool]] = None,
    ) -> None:
        self.fader_value: int = fader_value
        self.on_load_play: bool = on_load_play
        self.fader_mode: int = fader_mode
        self.chase: bool = chase
        self.index: int = index
        self.ms_chase_time: int = ms_chase_time
        self.fader_up_play: bool = fader_up_play
        self.priority: int = priority
        self.bpm_chase: int = bpm_chase
        self.on_page_stop: bool = on_page_stop
        self.trigger_level: int = trigger_level
        self.is_executor: bool = is_executor
        self.pcrossfade: int = pcrossfade
        self.ms_fadeout: int = ms_fadeout
        self.fader_down_stop: bool = fader_down_stop
        self.ignore_swap: Optional[bool] = ignore_swap
        self.swap_always: Optional[bool] = swap_always
        self.ms_fadein: int = ms_fadein
        self.ms_crossfade: int = ms_crossfade
        self.on_page_play: bool = on_page_play
        self.xct_color: List[int] = xct_color if xct_color is not None else []
        self.cuelist: Union[int, str] = cuelist
        self.xct_push_mode: List[bool] = xct_push_mode if xct_push_mode is not None else []
        self.docked: bool = docked
        self.used_in_alarm: Optional[bool] = used_in_alarm
        self.xct_cuelist: List[int] = xct_cuelist if xct_cuelist is not None else []
        self.page: int = page
        self.ignore_grand_master: Optional[bool] = ignore_grand_master
        self.xct_swap: Optional[List[bool]] = xct_swap

    @property
    def combined_id(self):
        """Return a combined ID using both page and index in the format 'page.index'"""
        return f"{self.page}.{self.index}" if self.page is not None and self.index is not None else str(self.index)
    
    def __repr__(self):
        return (
            f"Playback(fader_value={self.fader_value!r}, on_load_play={self.on_load_play!r}, "
            f"fader_mode={self.fader_mode!r}, chase={self.chase!r}, index={self.index!r}, "
            f"ms_chase_time={self.ms_chase_time!r}, fader_up_play={self.fader_up_play!r}, "
            f"priority={self.priority!r}, bpm_chase={self.bpm_chase!r}, on_page_stop={self.on_page_stop!r}, "
            f"trigger_level={self.trigger_level!r}, is_executor={self.is_executor!r}, "
            f"pcrossfade={self.pcrossfade!r}, ms_fadeout={self.ms_fadeout!r}, "
            f"fader_down_stop={self.fader_down_stop!r}, ignore_swap={self.ignore_swap!r}, "
            f"swap_always={self.swap_always!r}, ms_fadein={self.ms_fadein!r}, "
            f"ms_crossfade={self.ms_crossfade!r}, on_page_play={self.on_page_play!r}, "
            f"xct_color={self.xct_color!r}, cuelist={self.cuelist!r}, xct_push_mode={self.xct_push_mode!r}, "
            f"docked={self.docked!r}, used_in_alarm={self.used_in_alarm!r}, xct_cuelist={self.xct_cuelist!r}, "
            f"page={self.page!r}, ignore_grand_master={self.ignore_grand_master!r}, xct_swap={self.xct_swap!r})"
        )

    def to_dict(self) -> dict:
        return {
            "fader_value": self.fader_value,
            "on_load_play": self.on_load_play,
            "fader_mode": self.fader_mode,
            "chase": self.chase,
            "index": self.index,
            "ms_chase_time": self.ms_chase_time,
            "fader_up_play": self.fader_up_play,
            "priority": self.priority,
            "bpm_chase": self.bpm_chase,
            "on_page_stop": self.on_page_stop,
            "trigger_level": self.trigger_level,
            "is_executor": self.is_executor,
            "pcrossfade": self.pcrossfade,
            "ms_fadeout": self.ms_fadeout,
            "fader_down_stop": self.fader_down_stop,
            "ignore_swap": self.ignore_swap,
            "swap_always": self.swap_always,
            "ms_fadein": self.ms_fadein,
            "ms_crossfade": self.ms_crossfade,
            "on_page_play": self.on_page_play,
            "xct_color": self.xct_color,
            "cuelist": self.cuelist,
            "xct_push_mode": self.xct_push_mode,
            "docked": self.docked,
            "used_in_alarm": self.used_in_alarm,
            "xct_cuelist": self.xct_cuelist,
            "page": self.page,
            "ignore_grand_master": self.ignore_grand_master,
            "combined_id": self.combined_id,
            "xct_swap": self.xct_swap,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Playback":
        if data is None:
            return None
        return cls(
            fader_value=data.get("fader_value"),
            on_load_play=data.get("on_load_play"),
            fader_mode=data.get("fader_mode"),
            chase=data.get("chase"),
            index=data.get("index"),
            ms_chase_time=data.get("ms_chase_time"),
            fader_up_play=data.get("fader_up_play"),
            priority=data.get("priority"),
            bpm_chase=data.get("bpm_chase"),
            on_page_stop=data.get("on_page_stop"),
            trigger_level=data.get("trigger_level"),
            is_executor=data.get("is_executor"),
            pcrossfade=data.get("pcrossfade"),
            ms_fadeout=data.get("ms_fadeout"),
            fader_down_stop=data.get("fader_down_stop"),
            ignore_swap=data.get("ignore_swap"),
            swap_always=data.get("swap_always"),
            ms_fadein=data.get("ms_fadein"),
            ms_crossfade=data.get("ms_crossfade"),
            on_page_play=data.get("on_page_play"),
            xct_color=data.get("xct_color"),
            cuelist=data.get("cuelist"),
            xct_push_mode=data.get("xct_push_mode"),
            docked=data.get("docked"),
            used_in_alarm=data.get("used_in_alarm"),
            xct_cuelist=data.get("xct_cuelist"),
            page=data.get("page"),
            ignore_grand_master=data.get("ignore_grand_master"),
            xct_swap=data.get("xct_swap"),
        )

    def to_bytes(self) -> bytes:
        logger.debug(f"Starting serialisation of Playback object {self.combined_id}")
        bytestr = bytearray(serialise_section_header("playback"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = [
            "fader_value", "fader_mode", "index", "ms_chase_time", "priority", "bpm_chase", "trigger_level", "pcrossfade", "ms_fadeout", "ms_fadein",
            "ms_crossfade", "page"
        ]
        bool_attrs = [
            "on_load_play", "chase", "fader_up_play", "on_page_stop", "is_executor", "fader_down_stop", "ignore_swap",
            "swap_always", "on_page_play", "docked", "used_in_alarm", "ignore_grand_master"
        ]
        num_list_attrs = ["xct_color", "xct_cuelist"]
        bool_list_attrs = ["xct_push_mode", "xct_swap"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name == "cuelist":
                    if attr_value == "N/A":
                        content.extend(b'\xFF')
                    else:
                        content.extend(serialise_num_value(attr_value, cc_check=True))

                elif attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in num_list_attrs:
                    content.extend(serialise_num_list(attr_value))
                elif attr_name in bool_list_attrs:
                    content.extend(serialise_bool_list(attr_value))

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logger.info("Playback object serialised")
        logger.debug(bytestr)
        return bytes(bytestr)