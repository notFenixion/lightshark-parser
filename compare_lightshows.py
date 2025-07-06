import sys
from lightshark_parser import parse_lshw, parse_dict_to_lightshow

def compare_dicts(d1, d2, path=""):
    diffs = []

    # Handle cases where d1 or d2 might be None
    if d1 is None and d2 is None:
        return []
    if d1 is None:
        return [f"Value at '{path}' is None in first dict, but not in second: {d2!r}"]
    if d2 is None:
        return [f"Value at '{path}' is not None in first dict: {d1!r}, but is None in second."]

    # Ensure both are dictionaries before proceeding with key comparison
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        if d1 != d2:
            return [f"Type or value differs at '{path}'. First: {d1!r} ({type(d1)}), Second: {d2!r} ({type(d2)})."]
        return []

    # Check keys present in d1 but not in d2
    for k in d1:
        if k not in d2:
            diffs.append(f"Key '{path}{k}' in first dict but not in second.")
    
    # Check keys present in d2 but not in d1
    for k in d2:
        if k not in d1:
            diffs.append(f"Key '{path}{k}' in second dict but not in first.")

    # Compare common keys
    for k in d1:
        if k in d2:
            v1 = d1[k]
            v2 = d2[k]
            current_path = f"{path}{k}." if path else f"{k}."

            if isinstance(v1, dict) and isinstance(v2, dict):
                diffs.extend(compare_dicts(v1, v2, current_path))
            elif isinstance(v1, list) and isinstance(v2, list):
                # Track if list lengths are different
                if len(v1) != len(v2):
                    diffs.append(f"List length differs at '{current_path}'. First: {len(v1)}, Second: {len(v2)}")
                
                # Compare elements up to the minimum length to avoid index errors
                min_len = min(len(v1), len(v2))
                for i in range(min_len):
                    item1 = v1[i]
                    item2 = v2[i]
                    list_path = f"{current_path}[{i}]"
                    if isinstance(item1, dict) and isinstance(item2, dict):
                        diffs.extend(compare_dicts(item1, item2, list_path + "."))
                    elif isinstance(item1, list) and isinstance(item2, list):
                        diffs.extend(compare_dicts(item1, item2, list_path + "."))
                    elif item1 != item2:
                        diffs.append(f"List item differs at '{list_path}'. First: {item1!r}, Second: {item2!r}")
            elif v1 != v2:
                diffs.append(f"Value differs at '{current_path}'. First: {v1!r}, Second: {v2!r}")
    return diffs

# Main execution
try:
    lightshow_original = parse_lshw("Lightshows/testing/MASTER SHOW (REPATCH).lshw")
    print("Original Lightshow parsed.")

    lsdict = lightshow_original.to_dict()
    print("Original Lightshow converted to dict.")

    new_lightshow = parse_dict_to_lightshow(lsdict)
    print("New Lightshow created from dict.")

    original_dict = lightshow_original.to_dict()
    new_dict = new_lightshow.to_dict()

    differences = compare_dicts(original_dict, new_dict)

    if not differences:
        print("Parse dict test passed! No differences found.")
    else:
        print("Differences found:")
        for diff in differences:
            print(f"- {diff}")

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)
