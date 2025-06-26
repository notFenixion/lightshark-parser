from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging
from .fx import FX
from .order import Order


class Cue:

    """


    NOTE: Actions not implemented yet
    """

    def __init__(
        self,
        fx_palette: Optional[int] = None,
        cue_id: Optional[int] = None,
        description: Optional[str] = None,
        visual_id: Optional[int] = None,
        fxs: Optional[List["FX"]] = None,
        fxs_channels: Optional[List[Dict[int, Any]]] = None,
        orders: Optional[List[Order]] = None,
        actions: Optional[List["Action"]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fx_palette: int = fx_palette
        self.cue_id: int = cue_id
        self.description: str = description
        self.visual_id: int = visual_id
        self.fxs: List["FX"] = fxs
        self.fxs_channels: List[dict] = fxs_channels
        self.orders: List[Order] = orders
        self.actions: List["Action"] = actions
        self.name: str = name

    def to_dict(self) -> dict:
        fxs_list = []
        for fx in self.fxs:
            if hasattr(fx, "to_dict"):
                fxs_list.append(fx.to_dict())
            elif hasattr(fx, "__dict__"):
                fxs_list.append(fx.__dict__)
            else:
                fxs_list.append(fx)

        orders_list = []
        for order in self.orders:
            if hasattr(order, "to_dict"):
                orders_list.append(order.to_dict())
            elif hasattr(order, "__dict__"):
                orders_list.append(order.__dict__)
            else:
                orders_list.append(order)

        return {
            "fx_palette": self.fx_palette,
            "cue_id": self.cue_id,
            "description": self.description,
            "visual_id": self.visual_id,
            "actions": self.actions,
            "fxs": fxs_list if self.fxs else None,  # Set to None if no fxs
            "fxs_channels": self.fxs_channels,
            "orders": orders_list,
            "name": self.name,
        }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Cue object {self.name} (id: {self.cue_id})")
        bytestr = bytearray(serialise_section_header("cue"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["cue_id", "visual_id"]
        string_attrs = ["description", "name"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1
                
                if attr_name == "fx_palette":
                    if attr_value == "N/A":
                        content.extend(b'\xFF')
                    else:
                        content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value, cc_check=True))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == 'fxs_channels':
                    num_lists = len(attr_value)
                    content.extend(serialise_objlist_len(num_lists))
                    for fx_channel in attr_value:
                        list_content = bytearray()
                        list_len = sum(1 for value in fx_channel if not isinstance(value, str))
                        if list_len != 16:
                            raise ValueError("FX channel list length should be 16 (NOTE: unconfirmed. though this error shouldn't happen either way...)")
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
                    num_orders = len(attr_value)
                    content.extend(serialise_objlist_len(num_orders))
                    for order in attr_value:
                        content.extend(order.to_bytes())
                elif attr_name == 'actions':
                    raise NotImplementedError("Actions not implemented yet")
                    # num_actions = len(attr_value)
                    # bytestr.extend(serialise_objlist_len(num_actions))
                    # for action in attr_value:
                    #     bytestr.extend(action.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Cue object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)
