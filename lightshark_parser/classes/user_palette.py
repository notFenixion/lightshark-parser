from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging
from lightshark_parser.classes.order import Order


class UserPalette:
    def __init__(
        self,
        section: int = None,
        user_palette_id: int = None,
        name: str = None,
        icon: str = None,
        orders: Optional[List["Order"]] = None,
    ) -> None:
        self.section: int = section
        self.user_palette_id: int = user_palette_id
        self.name: str = name
        self.icon: str = icon
        self.orders: List["Order"] = orders

    def to_dict(self) -> dict:
        return {
            "section": self.section,
            "user_palette_id": self.user_palette_id,
            "name": self.name,
            "icon": self.icon,
            "orders": [order.to_dict() if hasattr(order, "to_dict") else order for order in self.orders],
        }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of UserPalette object {self.name} (id: {self.user_palette_id})")
        bytestr = bytearray(serialise_section_header("user_palette"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["section", "user_palette_id"]
        string_attrs = ["name", "icon"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name == "orders":
                    num_orders = len(attr_value)
                    content.extend(serialise_objlist_len(num_orders))
                    for order in attr_value:
                        content.extend(order.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("UserPalette object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)