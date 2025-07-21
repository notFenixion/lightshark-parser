#!/usr/bin/env python3
"""
Test script to verify cuelist_elements dictionary changes work correctly.
"""

from lightshark_parser.classes.cuelist import Cuelist, CuelistElement

def test_cuelist_elements_dict():
    """Test that cuelist_elements works as a dictionary."""
    
    # Create test cuelist elements
    element1 = CuelistElement(dotted_id=1000, cue_id=1, ms_fadein=3000)
    element2 = CuelistElement(dotted_id=2000, cue_id=2, ms_fadein=4000)
    element3 = CuelistElement(dotted_id=1500, cue_id=3, ms_fadein=2000)
    
    # Create cuelist with dictionary of elements
    cuelist_elements_dict = {
        1000: element1,
        2000: element2, 
        1500: element3
    }
    
    cuelist = Cuelist(
        cuelist_id=1,
        name="Test Cuelist",
        cuelist_elements=cuelist_elements_dict
    )
    
    print("=== Testing Cuelist Elements Dictionary ===")
    print(f"Cuelist: {cuelist.name}")
    print(f"Number of elements: {len(cuelist.cuelist_elements)}")
    
    # Test accessing elements by dotted_id
    print("\nElements by dotted_id:")
    for dotted_id in sorted(cuelist.cuelist_elements.keys()):
        element = cuelist.cuelist_elements[dotted_id]
        print(f"  dotted_id {dotted_id}: cue_id={element.cue_id}, fadein={element.ms_fadein}ms")
    
    # Test to_dict
    print("\n=== Testing to_dict ===")
    cuelist_dict = cuelist.to_dict()
    print("cuelist_elements in dict format:")
    for dotted_id, elem_dict in cuelist_dict["cuelist_elements"].items():
        print(f"  {dotted_id}: {elem_dict}")
    
    # Test from_dict
    print("\n=== Testing from_dict ===")
    cuelist_restored = Cuelist.from_dict(cuelist_dict)
    print(f"Restored cuelist elements count: {len(cuelist_restored.cuelist_elements)}")
    for dotted_id in sorted(cuelist_restored.cuelist_elements.keys()):
        element = cuelist_restored.cuelist_elements[dotted_id]
        print(f"  dotted_id {dotted_id}: cue_id={element.cue_id}, fadein={element.ms_fadein}ms")
    
    # Test to_bytes (basic check - just ensure it doesn't crash)
    print("\n=== Testing to_bytes ===")
    try:
        cuelist_bytes = cuelist.to_bytes()
        print(f"Successfully serialized to {len(cuelist_bytes)} bytes")
    except Exception as e:
        print(f"Error in to_bytes: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_cuelist_elements_dict()
