
from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging


class Group:
    def __init__(
        self,
        description: Optional[str] = None,
        color_mark: Optional[int] = None,
        visual_id: Optional[int] = None,
        patched_elements_ids: Optional[List[int]] = None,
        grid: Optional[Dict[int, List[int]]] = None,
        steps: Optional[Dict[int, int]] = None,
        automatico: Optional[bool] = None,
        group_id: Optional[int] = None,
    ) -> None:
        self.description: Optional[str] = description
        self.color_mark: Optional[int] = color_mark
        self.visual_id: Optional[int] = visual_id
        self.patched_elements_ids: List[int] = patched_elements_ids
        self.grid: Dict[int, List[int]] = grid
        self.steps: Dict[int, int] = steps
        self.automatico: Optional[bool] = automatico
        self.group_id: Optional[int] = group_id

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "color_mark": self.color_mark,
            "visual_id": self.visual_id,
            "patched_elements_ids": self.patched_elements_ids,
            "grid": {str(k): v for k, v in self.grid.items()},
            "steps": {str(k): v for k, v in self.steps.items()},
            "automatico": self.automatico,
            "group_id": self.group_id,
        }

    def to_bytes(self) -> bytes:
        logging.debug(f"Starting serialization of Group object {self.description} (id: {self.group_id})")
        bytestr = bytearray(serialise_section_header("group"))
        content = bytearray()
        num_attr = 0
        
        num_attrs = ["group_id", "visual_id", "color_mark"]
        string_attrs = ["description"]
        bool_attrs = ["automatico"]
        num_list_attrs = ["patched_elements_ids"]
        
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                content.extend(serialise_attr_name(attr_name))
                num_attr += 1

                if attr_name in num_attrs:
                    content.extend(serialise_num_value(attr_value))
                elif attr_name in string_attrs:
                    content.extend(serialise_str_value(attr_value))
                elif attr_name in bool_attrs:
                    content.extend(serialise_bool_value(attr_value))
                elif attr_name in num_list_attrs:
                    content.extend(serialise_num_list(attr_value, cc_check=True))
                elif attr_name == "grid":
                    num_fixtures = len(attr_value)
                    content.extend(serialise_num_attr(num_fixtures))
                    for fixture_id, fixture_pos in attr_value.items():
                        content.extend(serialise_num_value(int(fixture_id)))
                        content.extend(serialise_num_list(fixture_pos))
                elif attr_name in ["steps"]:
                    num_steps = len(attr_value)
                    content.extend(serialise_num_attr(num_steps))
                    for step_id, step in attr_value.items():
                        content.extend(serialise_num_value(int(step_id)))
                        content.extend(serialise_num_value(step))

        content[0:0] = serialise_num_attr(num_attr)
        bytestr.extend(serialise_content_length(content))
        bytestr.extend(content)
        logging.info("Group object serialised")
        logging.debug(bytestr)
        return bytes(bytestr)