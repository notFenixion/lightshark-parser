FTYPE_MAPPINGS = {
    "INTENSITY": {
        "516": "Intensity",
        "519": "Intensity Ctrl",
        "532": "Shutter",
        "535": "Shutter Ctrl"
    },
    "POSITION": {
        "536": "Pan",
        "537": "Pan Fine",
        "540": "Tilt",
        "541": "Tilt Fine"
    },
    "BEAM": {
        "624": "Focus",
        "628": "Zoom",
        "632": "Iris",
        "636": "Frost",
        "644": "Prism",
        "656": "Prism Rot",
        "664": "Hotspot"
    },
    "GOBO": {
        "680": "Gobo",
        "684": "Gobo2",
        "696": "Gobo Rot",
        "697": "GoboRot Fine",
        "700": "Gobo Rot2"
    },
    "ADVANCED": {
        "756": "Funct",
        "760": "Funct2",
        "792": "Macro",
        "795": "Macros Speed"
    },
    "COLOR": {
        "564": "Red",
        "568": "Green",
        "572": "Blue",
        "576": "Amber",
        "580": "Warm White",
        "583": "White Ctrl",
        "584": "Cyan",
        "588": "Magenta",
        "592": "Yellow",
        "596": "Color Temp / Color Wheel",
        "600": "",
        "608": "CMY Macro",
        "616": "CTO"
    },
    "UNKNOWN": {
        "544": "PTSpeed",
        "744": "",
        "747": "FX Ctrl",
        "748": "",
        "752": "",
        "768": "",
        "772": "",
        "800": "Custom",
        "840": "Empty",
        "884": "Strobe",
        "1000": "UV"
    }
}

SECTION_MAPPINGS = {
    1: 'POSITION',
    2: 'INTENSITY',
    3: 'COLOR',
    4: 'GOBO',
    5: 'BEAM',
    7: 'ADVANCED',
}

def get_section_from_ftype(ftype: int) -> int:
    """
    Gets the section ID from a given ftype.
    """
    ftype_str = str(ftype)
    for section_name, ftypes in FTYPE_MAPPINGS.items():
        if ftype_str in ftypes:
            for section_id, name in SECTION_MAPPINGS.items():
                if name == section_name:
                    return section_id
    return 0 # Default to 0 if not found
