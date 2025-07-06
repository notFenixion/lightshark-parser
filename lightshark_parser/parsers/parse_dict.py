from typing import Dict, Any
from lightshark_parser.classes import Lightshow

def parse_dict_to_lightshow(lsdict: Dict[str, Any]) -> Lightshow:
    """Parses a dictionary to a Lightshow object."""
    return Lightshow.from_dict(lsdict)