from __future__ import annotations
from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging

class Playback:
    def __init__(
        self,
        fader_value: Optional[int] = None,
        on_load_play: Optional[bool] = None,
        fader_mode: Optional[int] = None,
        chase: Optional[bool] = None,
        index: Optional[int] = None,
        ms_chase_time: Optional[int] = None,
        fader_up_play: Optional[bool] = None,
        priority: Optional[int] = None,
        bpm_chase: Optional[int] = None,
        on_page_stop: Optional[bool] = None,
        trigger_level: Optional[int] = None,
        is_executor: Optional[bool] = None,
        pcrossfade: Optional[int] = None,
        ms_fadeout: Optional[int] = None,
        fader_down_stop: Optional[bool] = None,
        ignore_swap: Optional[bool] = None,
        swap_always: Optional[bool] = None,
        ms_fadein: Optional[int] = None,
        ms_crossfade: Optional[int] = None,
        on_page_play: Optional[bool] = None,
        xct_color: Optional[List[int]] = None,
        cuelist: Optional[int] = None,
        xct_push_mode: Optional[List[bool]] = None,
        docked: Optional[bool] = None,
        used_in_alarm: Optional[bool] = None,
        xct_cuelist: Optional[List[int]] = None,
        page: Optional[int] = None,
        ignore_grand_master: Optional[bool] = None,
        xct_swap: Optional[List[bool]] = None,
    ) -> None:
        self.fader_value: Optional[int] = fader_value
        self.on_load_play: Optional[bool] = on_load_play
        self.fader_mode: Optional[int] = fader_mode
        self.chase: Optional[bool] = chase
        self.index: Optional[int] = index
        self.ms_chase_time: Optional[int] = ms_chase_time
        self.fader_up_play: Optional[bool] = fader_up_play
        self.priority: Optional[int] = priority
        self.bpm_chase: Optional[int] = bpm_chase
        self.on_page_stop: Optional[bool] = on_page_stop
        self.trigger_level: Optional[int] = trigger_level
        self.is_executor: Optional[bool] = is_executor
        self.pcrossfade: Optional[int] = pcrossfade
        self.ms_fadeout: Optional[int] = ms_fadeout
        self.fader_down_stop: Optional[bool] = fader_down_stop
        self.ignore_swap: Optional[bool] = ignore_swap
        self.swap_always: Optional[bool] = swap_always
        self.ms_fadein: Optional[int] = ms_fadein
        self.ms_crossfade: Optional[int] = ms_crossfade
        self.on_page_play: Optional[bool] = on_page_play
        self.xct_color: Optional[List[int]] = xct_color
        self.cuelist: Optional[int] = cuelist
        self.xct_push_mode: Optional[List[bool]] = xct_push_mode
        self.docked: Optional[bool] = docked
        self.used_in_alarm: Optional[bool] = used_in_alarm
        self.xct_cuelist: Optional[List[int]] = xct_cuelist
        self.page: Optional[int] = page
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
        logging.debug(f"Starting serialisation of Playback object {self.combined_id}")
        bytestr = bytearray(serialise_section_header("playback"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = [
            "fader_value", "fader_mode", "index", "ms_chase_time", "priority", "bpm_chase", "trigger_level", "pcrossfade", "ms_fadeout", "ms_fadein",
            "ms_crossfade", "cuelist", "page"
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

                if attr_name in num_attrs:
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
        logging.info("Playback object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)