

def section_header(section_name: str):
    return (
        (len(section_name)+1).to_bytes(4, "big") +
        (len(section_name) + 0xA0).to_bytes(1, "big") +
        section_name.encode("utf-8")
    )
