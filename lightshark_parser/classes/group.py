from typing import Dict, List, Any, Optional
from lightshark_parser.serialisers.attribute_serialisers import *
import logging


class Group:

    """
    Compulsory attributes: patched_elements_ids
    Optional attributes (defaults): 
        description = "Group {group_id}"
        color_mark = 0
        visual_id = max(Group._all_visual_ids) + 1
        grid = linear
        steps = 0
        automatico = False
        group_id = max(Group._all_groups.keys(), default=0) + 1

    """

    def __init__(
        self,
        patched_elements_ids: List[int],
        description: Optional[str] = None,
        color_mark: int = 0,
        visual_id: Optional[int] = None,
        grid: Optional[Dict[int, List[int]]] = None,
        steps: Optional[Dict[int, int]] = None,
        automatico: bool = False,
        group_id: Optional[int] = None,
    ) -> None:

        # If description not given, auto-assign to "Group {group_id}"
        if description is None:
            description = f"Group {group_id}"

        # If no grid, defaults to linear
        if grid is None:
            grid = {}
            for i, fixture_id in enumerate(patched_elements_ids, start=0):
                grid[fixture_id] = [0, i]
        else:
            for fixture_id, fixture_pos in grid.items():
                if fixture_id not in patched_elements_ids:
                    raise ValueError(f"Fixture ID {fixture_id} not found in patched_elements_ids")
                if len(fixture_pos) != 2 or not all(isinstance(x, int) for x in fixture_pos):
                    raise ValueError(f"Fixture position {fixture_pos} must be a list of 2 integers")
                if list(grid.values()).count(fixture_pos) > 1:
                    raise ValueError(f"Duplicate fixture position {fixture_pos}")

        # If no step, defaults to 0 (all same priority in playback order)
        if steps is None:
            steps = {}
            for fixture_id in patched_elements_ids:
                steps[fixture_id] = 0
        else:
            for fixture_id, step in steps.items():
                if fixture_id not in patched_elements_ids:
                    raise ValueError(f"Fixture ID {fixture_id} not found in patched_elements_ids")
                if not isinstance(step, int):
                    raise ValueError(f"Step {step} must be an integer")


        self.description = description
        self.color_mark = color_mark
        self.visual_id = visual_id
        self.patched_elements_ids = patched_elements_ids
        self.grid = grid
        self.steps = steps
        self.automatico = automatico
        self.group_id = group_id

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



