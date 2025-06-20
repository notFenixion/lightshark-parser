from lightshark_parser.classes import Lightshow

def format_show_info(lightshow: Lightshow) -> str:
    return f"""========== SHOW INFO ==========

File name: {lightshow._filename}
Date parsed: {lightshow._parsed_date}
Creation Date: {lightshow._created_at}
Last Modified: {lightshow._modified_at}

Fixtures: {len(lightshow._patches)}
Cues: {len(lightshow._cues)}
Cuelists: {len(lightshow._cuelists)}"""


def format_patches(lightshow: Lightshow) -> str:
    output = """========== FIXTURES/PATCHES =========="""

    grouped_patches = {}
    for patch in lightshow._patches.values():
        model_id = patch.model_id
        if model_id not in grouped_patches:
            grouped_patches[model_id] = []
        grouped_patches[model_id].append(patch)

    for model_id, patches in grouped_patches.items():
        patches_sorted = sorted(patches, key=lambda patch: patch.id)
        model = lightshow._models.get(model_id)

        output += (
            f"\n\n{model.name} (IDs: {', '.join(str(patch.id) for patch in patches_sorted)})" +
            f"\n    Universe - {patches_sorted[0].universe}" +
            f"\n    Inverse Tilt - {patches_sorted[0].inverse_tilt}" +
            f"\n    Inverse Pan - {patches_sorted[0].inverse_pan}" +
            f"\n    Uses Virtual Dimmer? - {model.use_virtual_dimmer}" +
            f"\n    Fixture Attributes - "
        )
        
        values = getattr(model, "values", None)
        if model and values:
            descriptions = [
                value.description if getattr(value, "description", None) else "N/A"
                for value in values
            ]
            output += ", ".join(descriptions)
    
    return output


def format_groups(lightshow: Lightshow) -> str:
    output = """========== GROUPS =========="""

    for group in lightshow._groups.values():
        output += (
            f"\n\n{group.description} (Group ID: {group.group_id})" +
            f" {'(AUTO-GENERATED)' if group.automatico else ''}" + 
            f"\n    Fixtures:"
        )
        # Group patched_elements_ids by their model_id
        model_to_patch_ids = {}
        for patch_id in group.patched_elements_ids:
            patch = lightshow._patches.get(patch_id)
            if patch:
                model_id = patch.model_id
                if model_id not in model_to_patch_ids:
                    model_to_patch_ids[model_id] = []
                model_to_patch_ids[model_id].append(patch_id)
        for model_id, patch_ids in model_to_patch_ids.items():
            model = lightshow._models.get(model_id)
            model_name = model.name if model and hasattr(model, "name") else str(model_id)
            output += f"\n        {model_name}: {', '.join(str(pid) for pid in sorted(patch_ids))}"

        output += f"\n    Grid:"
        if hasattr(group, "grid") and isinstance(group.grid, dict):
            # Build a 2D grid box representation
            grid_coords = list(group.grid.items())
            if not grid_coords:
                output += "\n        (No grid data available)"
            else:
                max_x = max(coords[0] for _, coords in grid_coords)
                max_y = max(coords[1] for _, coords in grid_coords)
                # Build empty grid
                grid_2d = [["" for _ in range(max_y + 1)] for _ in range(max_x + 1)]
                # Place patch IDs in grid
                for patch_id, (x, y) in grid_coords:
                    grid_2d[x][y] = str(patch_id)
                # Determine cell width for pretty boxing
                cell_width = max(
                    max((len(str(pid)) for pid, _ in grid_coords), default=1),
                    2
                )
                # Build horizontal border
                horiz_border = "┌" + "┬".join(["─" * cell_width for _ in range(max_y + 1)]) + "┐"
                mid_border   = "├" + "┼".join(["─" * cell_width for _ in range(max_y + 1)]) + "┤"
                bottom_border= "└" + "┴".join(["─" * cell_width for _ in range(max_y + 1)]) + "┘"
                # Output boxed grid
                output += "\n        " + horiz_border + "\n"
                for i, row in enumerate(grid_2d):
                    output += "        │" + "│".join(
                        f"{cell:^{cell_width}}" if cell else " " * cell_width for cell in row
                    ) + "│\n"
                    if i < len(grid_2d) - 1:
                        output += "        " + mid_border + "\n"
                output += "        " + bottom_border

    return output

def format_user_palettes(lightshow: Lightshow) -> str:
    output = """========== USER PALETTES =========="""


    return output
