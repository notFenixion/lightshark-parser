from __future__ import annotations
from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
from lightshark_parser.classes.order import Order
from lightshark_parser.utils.logger import logger


class UserPalette:
    def __init__(
        self,
        section: int = None,
        user_palette_id: int = None,
        name: str = None,
        icon: str = None,
        orders: Optional[dict[int, dict[int, Order]]] = None,
    ) -> None:
        if orders is not None:
            for ftype in orders.values():
                for order in ftype.values():
                    if order.section != section:
                        raise ValueError(f"Order section {order.section} does not match UserPalette section {section}")

        self.section: int = section
        self.user_palette_id: int = user_palette_id
        self.name: str = name
        self.icon: str = icon
        self.orders: dict[int, dict[int, Order]] = orders



    def __repr__(self):
        return (
            f"UserPalette(section={self.section!r}, user_palette_id={self.user_palette_id!r}, "
            f"name={self.name!r}, icon={self.icon!r}, orders={self.orders!r})"
        )
    
    def to_dict(self) -> dict:
        return {
            "section": self.section,
            "user_palette_id": self.user_palette_id,
            "name": self.name,
            "icon": self.icon,
            "orders": {
                patch_id: {
                    ftype: order.to_dict()
                    for ftype, order in ftype_orders.items()
                }
                for patch_id, ftype_orders in self.orders.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserPalette":
        if data is None:
            return None
        orders_data = data.get("orders", {})
        orders = {
            int(patch_id): {
                int(ftype): Order.from_dict(order_data)
                for ftype, order_data in ftype_orders.items()
            }
            for patch_id, ftype_orders in orders_data.items()
        }
        return cls(
            section=data.get("section"),
            user_palette_id=data.get("user_palette_id"),
            name=data.get("name"),
            icon=data.get("icon"),
            orders=orders,
        )

    def to_bytes(self) -> bytes:
        logger.debug(f"Starting serialization of UserPalette object {self.name} (id: {self.user_palette_id})")
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
                    num_orders = sum(len(ftype_orders) for ftype_orders in attr_value.values())
                    content.extend(serialise_objlist_len(num_orders))
                    for ftype_orders in attr_value.values():
                        for order in ftype_orders.values():
                            content.extend(order.to_bytes())

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logger.info("UserPalette object serialised")
        logger.debug(bytestr)
        return bytes(bytestr)