from __future__ import annotations
from typing import Dict, List, Any, Optional, Union
from lightshark_parser.serialisers.attribute_serialisers import *
import logging

from lightshark_parser.classes.order import Order
from lightshark_parser.classes.action import Action

class FX:
    def __init__(
        self,
        cyclos: int = None,
        direction: int = None,
        speed: int = None,
        group_steps: int = None,
        size: int = None,
        layers: List[FXLayer] = None,
        patches: List[int] = None,
        speed_in_bpm: bool = None,
        width: int = None,
        spread: int = None,
        basic: bool = None,
        gfxid: int = None,
        internal_speed: int = None,
        fx_ref: int = None,
        splits: int = None,
        groups: List[int] = None,
        rect_width: int = None,
        name: str = None,
        phase_offset: int = None,
        bpm: int = None,
        render_id: int = None,
        mode: int = None,
        repeats: int = None,
        rect_height: int = None,
    ) -> None:
        # Attributes ordered to match to_dict()
        self.cyclos: int = cyclos
        self.direction: int = direction
        self.speed: int = speed
        self.group_steps: int = group_steps
        self.size: int = size
        self.layers: List[FXLayer] = layers
        self.patches: List[int] = patches
        self.speed_in_bpm: bool = speed_in_bpm
        self.width: int = width
        self.spread: int = spread
        self.basic: bool = basic
        self.gfxid: int = gfxid
        self.internal_speed: int = internal_speed
        self.fx_ref: int = fx_ref
        self.splits: int = splits
        self.groups: List[int] = groups
        self.rect_width: int = rect_width
        self.name: str = name
        self.phase_offset: int = phase_offset
        self.bpm: int = bpm
        self.render_id: int = render_id
        self.mode: int = mode
        self.repeats: int = repeats
        self.rect_height: int = rect_height


    def __repr__(self):
        return (
            f"FX(cyclos={self.cyclos!r}, direction={self.direction!r}, speed={self.speed!r}, "
            f"group_steps={self.group_steps!r}, size={self.size!r}, layers={self.layers!r}, "
            f"patches={self.patches!r}, speed_in_bpm={self.speed_in_bpm!r}, width={self.width!r}, "
            f"spread={self.spread!r}, basic={self.basic!r}, gfxid={self.gfxid!r}, "
            f"internal_speed={self.internal_speed!r}, fx_ref={self.fx_ref!r}, splits={self.splits!r}, "
            f"groups={self.groups!r}, rect_width={self.rect_width!r}, name='{self.name}', "
            f"phase_offset={self.phase_offset!r}, bpm={self.bpm!r}, render_id={self.render_id!r}, "
            f"mode={self.mode!r}, repeats={self.repeats!r}, rect_height={self.rect_height!r})"
        )

    def to_dict(self) -> dict:
        return {
        "cyclos": self.cyclos,
        "direction": self.direction,
        "speed": self.speed,
        "group_steps": self.group_steps,
        "size": self.size,
        "layers": [layer.to_dict() for layer in self.layers] if self.layers else [],
        "patches": self.patches,
        "speed_in_bpm": self.speed_in_bpm,
        "width": self.width,
        "spread": self.spread,
        "basic": self.basic,
        "gfxid": self.gfxid,
        "internal_speed": self.internal_speed,
        "fx_ref": self.fx_ref,
        "splits": self.splits,
        "groups": self.groups,
        "rect_width": self.rect_width,
        "name": self.name,
        "phase_offset": self.phase_offset,
        "bpm": self.bpm,
        "render_id": self.render_id,
        "mode": self.mode,
        "repeats": self.repeats,
        "rect_height": self.rect_height
    }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FX":
        if data is None:
            return None
        layers = [FXLayer.from_dict(layer) for layer in data.get("layers", [])]
        return cls(
            cyclos=data.get("cyclos"),
            direction=data.get("direction"),
            speed=data.get("speed"),
            group_steps=data.get("group_steps"),
            size=data.get("size"),
            layers=layers,
            patches=data.get("patches"),
            speed_in_bpm=data.get("speed_in_bpm"),
            width=data.get("width"),
            spread=data.get("spread"),
            basic=data.get("basic"),
            gfxid=data.get("gfxid"),
            internal_speed=data.get("internal_speed"),
            fx_ref=data.get("fx_ref"),
            splits=data.get("splits"),
            groups=data.get("groups"),
            rect_width=data.get("rect_width"),
            name=data.get("name"),
            phase_offset=data.get("phase_offset"),
            bpm=data.get("bpm"),
            render_id=data.get("render_id"),
            mode=data.get("mode"),
            repeats=data.get("repeats"),
            rect_height=data.get("rect_height"),
        )

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of FX object {self.name}")
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = [
            "cyclos", "direction", "group_steps", "gfxid", "splits", "rect_width",
            "render_id", "mode", "repeats", "rect_height", "speed", "size",
            "width", "spread", "internal_speed", "fx_ref", "phase_offset", "bpm"
        ]
        bool_attrs = ["speed_in_bpm", "basic"]
        string_attrs = ["name"]
        num_list_attrs = ["patches", "groups"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in bool_attrs:
                    bytestr.extend(serialise_bool_value(attr_value))
                elif attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))
                elif attr_name in num_list_attrs:
                    bytestr.extend(serialise_num_list(attr_value))
                elif attr_name == "layers":
                    num_layers = len(attr_value)
                    bytestr.extend(serialise_objlist_len(num_layers))
                    for layer in attr_value:
                        bytestr.extend(layer.to_bytes())

        bytestr[0:0] = serialise_num_attr(num_attr)
        logging.info("FX object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)



class FXLayer:
        def __init__(
            self,
            blind: bool = None,
            phase_offset: int = None,
            section: int = None,
            curve: int = None,
            steps: List[FXLayerStep] = None,
            ftypes: List[int] = None,
            id: int = None,
            size: int = None,
        ) -> None:
            self.blind: bool = blind
            self.phase_offset: int = phase_offset
            self.section: int = section
            self.curve: int = curve
            self.steps: List[FXLayerStep] = steps
            self.ftypes: List[int] = ftypes
            self.id: int = id
            self.size: int = size

        def __repr__(self):
            return (
                f"FXLayer(blind={self.blind!r}, phase_offset={self.phase_offset!r}, "
                f"section={self.section!r}, curve={self.curve!r}, steps={self.steps!r}, "
                f"ftypes={self.ftypes!r}, id={self.id!r}, size={self.size!r})"
            )

        def to_dict(self) -> dict:
            steps_list = []
            for step in self.steps:
                if hasattr(step, "to_dict"):
                    steps_list.append(step.to_dict())
                elif hasattr(step, "__dict__"):
                    steps_list.append(step.__dict__)
                else:
                    steps_list.append(step)

            return {
                "blind": self.blind,
                "phase_offset": self.phase_offset,
                "section": self.section,
                "curve": self.curve,
                "steps": steps_list,
                "ftypes": self.ftypes,
                "id": self.id,
                "size": self.size,
            }

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> "FXLayer":
            steps = [FXLayerStep.from_dict(step) for step in data.get("steps", [])]
            return cls(
                blind=data.get("blind"),
                phase_offset=data.get("phase_offset"),
                section=data.get("section"),
                curve=data.get("curve"),
                steps=steps,
                ftypes=data.get("ftypes"),
                id=data.get("id"),
                size=data.get("size"),
            )

        def to_bytes(self) -> bytes:
            logging.debug(f"Starting serialization of FXLayer object {self.id}")
            bytestr = bytearray()
            num_attr = 0
            
            num_attrs = ["id", "phase_offset", "section", "curve", "size"]
            bool_attrs = ["blind"]
            num_list_attrs = ["ftypes"]
            
            for attr_name, attr_value in self.__dict__.items():
                if attr_value is not None:
                    bytestr.extend(serialise_attr_name(attr_name))
                    num_attr += 1

                    if attr_name in num_attrs:
                        bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                    elif attr_name in bool_attrs:
                        bytestr.extend(serialise_bool_value(attr_value))
                    elif attr_name in num_list_attrs:
                        bytestr.extend(serialise_num_list(attr_value, cc_check=True))
                    elif attr_name == "steps":
                        num_steps = len(attr_value)
                        bytestr.extend(serialise_objlist_len(num_steps))
                        for step in attr_value:
                            bytestr.extend(step.to_bytes())

            bytestr[0:0] = serialise_num_attr(num_attr)
            logging.info("FXLayer object serialised")
            logging.debug(bytestr)
            return bytes(bytestr)


class FXLayerStep:
    def __init__(
        self,
        start_limit: int = None,
        palette_type: int = None,
        name: str = None,
        ancho: int = None,
        curve_in: int = None,
        curve_out: int = None,
        strength: int = None,
        curve_type: int = None,
        palette_value: Any = None,
        inicio: int = None,
        end_limit: int = None,
        jumps: int = None,
    ) -> None:
        self.start_limit: int = start_limit
        self.palette_type: int = palette_type
        self.name: str = name
        self.ancho: int = ancho
        self.curve_in: int = curve_in
        self.curve_out: int = curve_out
        self.strength: int = strength
        self.curve_type: int = curve_type
        self.palette_value: Any = palette_value
        self.inicio: int = inicio
        self.end_limit: int = end_limit
        self.jumps: int = jumps

    def __repr__(self):
        return (
            f"FXLayerStep(start_limit={self.start_limit!r}, palette_type={self.palette_type!r}, "
            f"name='{self.name}', ancho={self.ancho!r}, curve_in={self.curve_in!r}, "
            f"curve_out={self.curve_out!r}, strength={self.strength!r}, "
            f"curve_type={self.curve_type!r}, palette_value={self.palette_value!r}, "
            f"inicio={self.inicio!r}, end_limit={self.end_limit!r}, jumps={self.jumps!r})"
        )

    def to_dict(self) -> dict:
        return {
            "start_limit": self.start_limit,
            "palette_type": self.palette_type,
            "name": self.name,
            "ancho": self.ancho,
            "curve_in": self.curve_in,
            "curve_out": self.curve_out,
            "strength": self.strength,
            "curve_type": self.curve_type,
            "palette_value": self.palette_value,
            "inicio": self.inicio,
            "end_limit": self.end_limit,
            "jumps": self.jumps,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FXLayerStep":
        return cls(
            start_limit=data.get("start_limit"),
            palette_type=data.get("palette_type"),
            name=data.get("name"),
            ancho=data.get("ancho"),
            curve_in=data.get("curve_in"),
            curve_out=data.get("curve_out"),
            strength=data.get("strength"),
            curve_type=data.get("curve_type"),
            palette_value=data.get("palette_value"),
            inicio=data.get("inicio"),
            end_limit=data.get("end_limit"),
            jumps=data.get("jumps"),
        )

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of FXLayerStep object {self.name}")
        bytestr = bytearray()
        num_attr = 0
        
        num_attrs = [
            "start_limit", "palette_type", "ancho", "curve_in", "curve_out",
            "strength", "curve_type", "palette_value", "inicio", "end_limit", "jumps"
        ]
        string_attrs = ["name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                bytestr.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    bytestr.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    bytestr.extend(serialise_str_value(attr_value))

        bytestr[0:0] = serialise_num_attr(num_attr)
        logging.info("FXLayerStep object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)




class FXPalette:

    """
    Basically the same attributes as cue, the only parts where their values differ are
    cue_id, visual_id, orders
    """

    def __init__(
        self,
        fx_palette: Optional[int] = None,
        cue_id: Optional[int] = None,
        description: Optional[str] = None,
        visual_id: Optional[int] = None,
        fxs: Optional[List["FX"]] = None,
        fxs_channels: Optional[List[List[Union[int, str]]]] = None,
        orders: Optional[dict[int, dict[int, Order]]] = None,
        actions: Optional[List[Action]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fx_palette: Optional[int] = fx_palette
        self.cue_id: Optional[int] = cue_id
        self.description: Optional[str] = description
        self.visual_id: Optional[int] = visual_id
        self.fxs: List["FX"] = fxs
        self.fxs_channels: List[List[Union[int, str]]] = fxs_channels 
        self.orders: dict[int, dict[int, Order]] = orders
        self.actions: List["Action"] = actions
        self.name: Optional[str] = name

    def __repr__(self):
        return (
            f"FXPalette(fx_palette={self.fx_palette!r}, cue_id={self.cue_id!r}, "
            f"description={self.description!r}, visual_id={self.visual_id!r}, "
            f"fxs={self.fxs!r}, fxs_channels={self.fxs_channels!r}, "
            f"orders={self.orders!r}, actions={self.actions!r}, name={self.name!r})"
        )

    def to_dict(self) -> dict:
        fxs_list = []
        for fx in self.fxs:
            if hasattr(fx, "to_dict"):
                fxs_list.append(fx.to_dict())
            elif hasattr(fx, "__dict__"):
                fxs_list.append(fx.__dict__)
            else:
                fxs_list.append(fx)

        orders_dict = {
            patch_id: {
                ftype: order.to_dict() if hasattr(order, "to_dict") else order
                for ftype, order in ftype_orders.items()
            }
            for patch_id, ftype_orders in self.orders.items()
        }

        return {
            "fx_palette": self.fx_palette,
            "cue_id": self.cue_id,
            "description": self.description,
            "visual_id": self.visual_id,
            "actions": self.actions,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": self.fxs_channels,
            "orders": orders_dict,
            "name": self.name,
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FXPalette":
        if data is None:
            return None
        fxs = [FX.from_dict(fx) for fx in data.get("fxs", [])] if data.get("fxs") else None
        orders_data = data.get("orders", {})
        orders = {
            int(patch_id): {
                int(ftype): Order.from_dict(order_data)
                for ftype, order_data in ftype_orders.items()
            }
            for patch_id, ftype_orders in orders_data.items()
        }
        actions = [Action.from_dict(action) for action in data.get("actions", [])] if data.get("actions") else None
        return cls(
            fx_palette=data.get("fx_palette"),
            cue_id=data.get("cue_id"),
            description=data.get("description"),
            visual_id=data.get("visual_id"),
            fxs=fxs,
            fxs_channels=data.get("fxs_channels"),
            orders=orders,
            actions=actions,
            name=data.get("name"),
        )
        
    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of FXPalette object {self.name} (id: {self.fx_palette})")
        bytestr = bytearray(serialise_section_header("fxpalette"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["fx_palette", "cue_id", "visual_id"]
        string_attrs = ["description", "name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == 'fxs_channels':
                    num_lists = len(attr_value)
                    content.extend(serialise_objlist_len(num_lists))
                    for fx_channel in attr_value:
                        list_content = bytearray()
                        logging.debug(fx_channel)
                        list_len = sum(1 for value in fx_channel if not isinstance(value, str))
                        if list_len != 16:
                            raise ValueError(f"FX channel list length should be 16, {list_len} detected (NOTE: unconfirmed. though this error shouldn't happen either way...)")
                        list_content.extend(serialise_objlist_len(list_len))
                        for value in fx_channel:
                            # \xd1 \x?? instances
                            if isinstance(value, str):
                                list_content.extend(bytes.fromhex(value))
                            else:
                                list_content.extend(serialise_num_value(value, cc_check=True))
                        content.extend(list_content)
                elif attr_name == 'fxs':
                    num_fxs = len(attr_value)
                    content.extend(serialise_objlist_len(num_fxs))
                    for fx in attr_value:
                        content.extend(fx.to_bytes())
                elif attr_name == 'orders':
                    num_orders = sum(len(ftype_orders) for ftype_orders in attr_value.values())
                    content.extend(serialise_objlist_len(num_orders))
                    for ftype_orders in attr_value.values():
                        for order in ftype_orders.values():
                            content.extend(order.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("FXPalette object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)
