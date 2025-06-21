from lightshark_parser.classes import Lightshow


def format_lightshow(lightshow: Lightshow) -> str:
    return (
            format_show_info(lightshow) + "\n\n" +
            format_patches(lightshow) + "\n\n" +
            format_groups(lightshow) + "\n\n" +
            format_user_palettes(lightshow) + "\n\n" +
            format_fx_palettes(lightshow) + "\n\n" +
            format_cues(lightshow) + "\n\n" +
            format_cuelists(lightshow)
        )


def format_show_info(lightshow: Lightshow) -> str:
    return f"""========== SHOW INFO ==========

File name: {lightshow.filename}
Date parsed: {lightshow.parsed_date}
Creation Date: {lightshow.created_at}
Last Modified: {lightshow.modified_at}

Fixtures: {len(lightshow.patches)}
Cues: {len(lightshow.cues)}
Cuelists: {len(lightshow.cuelists)}
FX Palettes: {len(lightshow.fxpalettes)}
User Palettes: {len(lightshow.user_palettes)}"""


def format_patches(lightshow: Lightshow) -> str:
    output = """========== FIXTURES/PATCHES =========="""
    
    if not lightshow.patches:
        return output + "\n\nNo fixtures found."

    grouped_patches = {}
    for patch in lightshow.patches.values():
        model_id = patch.model_id
        if model_id not in grouped_patches:
            grouped_patches[model_id] = []
        grouped_patches[model_id].append(patch)

    for model_id, patches in grouped_patches.items():
        patches_sorted = sorted(patches, key=lambda patch: patch.id)
        model = lightshow.models.get(model_id)
        model = lightshow._models.get(model_id)

        output += (
            f"\n\n{model.name} (IDs: {', '.join(str(patch.id) for patch in patches_sorted)})" +
            f"\n    Universe - {patches_sorted[0].universe}" +
            f"\n    Inverse Tilt - {patches_sorted[0].inverse_tilt}" +
            f"\n    Inverse Pan - {patches_sorted[0].inverse_pan}" +
            f"\n    Uses Virtual Dimmer? - {model.use_virtual_dimmer}" +
            f"\n    Fixture Attributes - "
        )
        
        if model and model.values:
            descriptions = [
                value.description
                for value in model.values
            ]
            output += ", ".join(descriptions)
    
    return output


def format_groups(lightshow: Lightshow) -> str:
    output = """========== GROUPS =========="""
    
    if not lightshow.groups:
        return output + "\n\nNo groups found."

    for group in lightshow.groups.values():
        output += (
            f"\n\n{group.description} (GrpID:{group.group_id})" +
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
            model = lightshow.models.get(model_id)
            model_name = model.name
            output += f"\n        {model_name}: {', '.join(str(pid) for pid in sorted(patch_ids))}"

        output += f"\n    Grid:"
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
    
    if not lightshow.user_palettes:
        return output + "\n\nNo user palettes found."
    for palette in lightshow.user_palettes.values():
        output += f"\n\n{palette.name} (ID:{palette.user_palette_id})"
        output += f"\n    Section: {palette.section}"
        output += f"\n    Values/Orders:"
        
        # Group orders by patch_id so that we can output multiple attributes for one patch
        orders_by_patch = {}
        for order in palette.orders:
            if order.patch_id not in orders_by_patch:
                orders_by_patch[order.patch_id] = []
            orders_by_patch[order.patch_id].append(order)
        
        # Group patches by their attribute values
        value_groups = {}
        for patch_id, orders in orders_by_patch.items():
            # Get the patch and model once per patch_id
            patch = lightshow._patches.get(patch_id)
            if not patch:
                continue
                
            model = lightshow.models.get(patch.model_id)
            if not model:
                continue
            
            attributes = []
            for order in orders:
                description = "Unknown"
                for value in model.values:
                    if value.ftype == order.ftype:
                        description = value.description
                        break
                attributes.append((description, order.value))
            
            attributes_tuple = tuple(sorted(attributes))
            
            if attributes_tuple not in value_groups:
                value_groups[attributes_tuple] = []
            value_groups[attributes_tuple].append(patch_id)
        
        for attributes, patch_ids in value_groups.items():
            patch_ids = sorted(patch_ids)
            
            if len(patch_ids) > 1:
                ranges = []
                start = patch_ids[0]
                prev = start
                
                for pid in patch_ids[1:]:
                    if pid == prev + 1:
                        prev = pid
                    else:
                        ranges.append((start, prev))
                        start = prev = pid
                ranges.append((start, prev))
                
                range_strs = []
                for start, end in ranges:
                    if start == end:
                        range_strs.append(str(start))
                    else:
                        range_strs.append(f"{start}-{end}")
                
                patch_str = ", ".join(range_strs)
            else:
                patch_str = str(patch_ids[0])
            
            attr_str = " | ".join(f"{desc}: {val}" for desc, val in attributes)
            
            output += f"\n        {patch_str} - {attr_str}"

    return output


def format_fx_palettes(lightshow: Lightshow) -> str:
    output = """===== FXPALETTES ====="""
    
    if not lightshow.fxpalettes:
        return output + "\n\nNo FX palettes found."
    
    for fx_palette_id, fx_palette in lightshow.fxpalettes.items():
        output += f"\n\n{fx_palette.name} (ID:{fx_palette_id})"
        
        if not fx_palette.fxs:
            output += "\n    No FXs used!"
            continue
            
        for fx in fx_palette.fxs:
            output += f"\n    FX {fx.gfxid}:"
            output += f"\n        Patches: {', '.join(map(str, fx.patches)) if fx.patches else 'None'}"
            
            direction_map = {
                0: "Forward",
                1: "Backward",
                2: "Ping Pong",
                3: "Random"
            }
            direction = direction_map.get(fx.direction, f"Unknown ({fx.direction})")
            output += f"\n        Direction: {direction}"
            output += f"\n        Split: {fx.splits}"
            output += f"\n        Repeats: {fx.repeats}"
            
            if fx.speed_in_bpm and fx.bpm:
                output += f"\n        Speed: {fx.bpm} BPM"
            else:
                output += f"\n        Speed: {fx.speed} ms"
            
            output += f"\n        Width: {fx.width/100:.2f}%"
            output += f"\n        Phase/Spread: {fx.spread * 360 / 1024:.1f}°"
            output += f"\n        Offset: {fx.phase_offset * 360 / 1024:.1f}°"
            output += f"\n        Basic: {fx.basic} (fx_ref: {fx.fx_ref})"
            
            # Advanced FX Layers
            if not fx.basic:
                output += "\n\n        Advanced FX Layers:"
                
                for layer in fx.layers:
                    ftype_descriptions = []
                    for ftype in layer.ftypes:
                        desc = f"{ftype}"
                        # Use the first patch to look up the model
                        first_patch_id = fx.patches[0]
                        if first_patch_id in lightshow.patches:
                            patch = lightshow.patches[first_patch_id]
                            if patch.model_id in lightshow.models:
                                model = lightshow.models[patch.model_id]
                                for value in model.values:
                                    if str(value.ftype) == str(ftype):
                                        desc = value.description
                                        break

                        ftype_descriptions.append(desc)
                    ftypes_str = ", ".join(ftype_descriptions)

                    output += (
                        f"\n        {layer.id}: {ftypes_str}" +
                        f"\n            Layer Offset: {layer.phase_offset * 360 / 1024:.1f}°" +
                        f"\n            Size: {layer.size/100:.2f}%" +
                        f"\n            Blind: {layer.blind}"
                    )
                    
                    for step in layer.steps:
                        ancho = getattr(step, 'ancho', 0)
                        start_deg = (step.inicio / 1024) * 360
                        width_deg = (ancho / 1024) * 360
                        end_deg = start_deg + width_deg
                        
                        output += (
                            f"\n            {step.name}:" +
                            f"\n                Range: {start_deg:.1f}° to {end_deg:.1f}° (width: {width_deg:.1f}°)" +
                            f"\n                Start Limit: {step.start_limit/100:.2f}%" +
                            f"\n                End Limit: {step.end_limit/100:.2f}%" +
                            f"\n                Curve Type: {step.curve_type}" +
                            f"\n                Curve Parameters:" +
                            f"\n                    Start Point: {step.inicio * 360 / 1024:.1f}°" +
                            f"\n                    In - {step.curve_in/100:.2f}%" +
                            f"\n                    Out - {step.curve_out/100:.2f}%" +
                            f"\n                    Strength - {step.strength}" +
                            f"\n                    Jumps - {step.jumps}"
                        )

    return output


def format_cues(lightshow: Lightshow) -> str:
    output = """===== CUES ====="""
    
    if not lightshow.cues:
        return output + "\n\nNo cues found."
    
    for cue_id, cue in sorted(lightshow.cues.items()):
        output += f"\n\n{cue.name} (ID:{cue_id})"
        output += "\n    Fixtures:"
        
        if not cue.orders:
            output += "\n        No fixtures in this cue"

        # Group orders by palette_id
        palette_orders = {}
        standalone_orders = []
        
        for order in cue.orders:
            if order.palette_id != 0:
                if order.palette_id not in palette_orders:
                    palette_orders[order.palette_id] = []
                palette_orders[order.palette_id].append(order)
            else:
                standalone_orders.append(order)
        
        if palette_orders:
            output += "\n        Palette Fixtures:"
            for palette_id, orders in palette_orders.items():
                if palette_id in lightshow.user_palettes:
                    palette = lightshow.user_palettes[palette_id]
                    patch_ids = sorted({o.patch_id for o in orders})
                    if patch_ids:
                        output += f"\n            {palette.name} (ID:{palette_id}) - {', '.join(map(str, patch_ids))}"
        
        if standalone_orders:
            output += "\n\n        Non-palette Fixtures:" if palette_orders else "\n        Non-palette Fixtures:"
            
            # Group by patch_id
            patch_orders = {}
            for order in standalone_orders:
                if order.patch_id != 0:
                    if order.patch_id not in patch_orders:
                        patch_orders[order.patch_id] = []
                    patch_orders[order.patch_id].append(order)
            
            # Add patch details
            for patch_id, orders in patch_orders.items():
                if patch_id in lightshow.patches:
                    patch = lightshow.patches[patch_id]
                    order_details = []
                    for order in orders:
                        if order.ftype and order.value:
                            # Get model details
                            ftype_desc = order.ftype
                            if patch.model_id in lightshow.models:
                                model = lightshow.models[patch.model_id]
                                for value in model.values:
                                    if str(value.ftype) == str(order.ftype):
                                        ftype_desc = value.description
                                        break
                            order_details.append(f"{ftype_desc}: {order.value}")
                    
                    if order_details:
                        # Format as: Name (ID: X) - Attribute1: Value1 | Attribute2: Value2 | Attribute3: Value3
                        formatted_details = []
                        for detail in order_details:
                            # Split each detail into key and value
                            if ': ' in detail:
                                key, value = detail.split(': ', 1)
                                formatted_details.append(f"{key}: {value}")
                        
                        # Join with | between details
                        details_str = ' | '.join(formatted_details)
                        output += f"\n            {patch.name} (ID:{patch_id}) - {details_str}"
        
        ## FXs ##
        output += "\n\n    FXs:"
        
        # Check if there are any FXs at all
        if not cue.fxs and cue.fx_palette == 0xFF:
            output += "\n        No FXs in this cue"
            
        # Track which patches are in the palette FX (if any)
        palette_patches = set()
        
        # Output FX palette name & id, or the whole FX if no fxpalette
        if cue.fx_palette != 0xFF:
            output += "\n        FX Palettes:"
            fx_palette_id = cue.fx_palette
            if fx_palette_id in lightshow.fxpalettes:
                fx_palette = lightshow.fxpalettes[fx_palette_id]
                patch_ids = []
                for fx in fx_palette.fxs:
                    patch_ids.extend(fx.patches)
                if patch_ids:
                    output += f"\n            {fx_palette.name} ({fx_palette_id}): {', '.join(map(str, sorted(set(patch_ids))))}"
        else:
            if cue.fxs:
                output += "\n        Non-palette FXs:"
                for fx in cue.fxs:
                    output += f"\n            FX {fx.gfxid}:"
                    output += f"\n                Patches: {', '.join(map(str, sorted(fx.patches)))}"
                    output += f"\n                Direction: {fx.direction}"
                    output += f"\n                Speed: {fx.bpm} BPM" if fx.speed_in_bpm and fx.bpm else f"\n                Speed: {fx.speed} ms"
                    output += f"\n                Width: {fx.width/100:.2f}%"
                    output += f"\n                Phase/Spread: {fx.spread * 360 / 1024:.1f}°"
                    output += f"\n                Offset: {fx.phase_offset * 360 / 1024:.1f}°"
                    output += f"\n                Basic: {fx.basic}"

                    # Add advanced FX here if fx.basic is not True
                    if not fx.basic:
                        output += "\n                Layers:"
                        for layer in fx.layers:
                            output += f"\n                Layer {layer.id}:"
                            output += f"\n                    Offset: {layer.phase_offset * 360 / 1024:.1f}°"
                            output += f"\n                    Size: {layer.size/100:.2f}%"
                            output += f"\n                    Blind: {layer.blind}"
                            
                            # Add steps
                            for step in layer.steps:
                                ancho = getattr(step, 'ancho', 0)
                                start_deg = (getattr(step, 'inicio', 0) / 1024) * 360
                                width_deg = (ancho / 1024) * 360
                                end_deg = start_deg + width_deg
                                
                                output += f"\n                    {getattr(step, 'name', 'Step')}:"
                                output += f"\n                        Range: {start_deg:.1f}° to {end_deg:.1f}° (width: {width_deg:.1f}°)"
                                output += f"\n                        Start Limit: {getattr(step, 'start_limit', 0)/100:.2f}%"
                                output += f"\n                        End Limit: {getattr(step, 'end_limit', 0)/100:.2f}%"
                                output += f"\n                        Curve Type: {getattr(step, 'curve_type', 'N/A')}"
                                output += f"\n                        Start Point: {getattr(step, 'inicio', 0) * 360 / 1024:.1f}°"
                                output += f"\n                        In: {getattr(step, 'curve_in', 0)/100:.2f}%"
                                output += f"\n                        Out: {getattr(step, 'curve_out', 0)/100:.2f}%"
                                output += f"\n                        Strength: {getattr(step, 'strength', 0)}"
                                output += f"\n                        Jumps: {getattr(step, 'jumps', 0)}"

    return output


def format_cuelists(lightshow: Lightshow) -> str:
    output = "===== CUELISTS ====="
    
    if not lightshow.cuelists:
        return output + "\n\nNo cuelists found."
    
    for cuelist_id, cuelist in sorted(lightshow.cuelists.items()):
        # Cuelist header
        output += f"\n\n{cuelist.name} (ID:{cuelist_id})"
        
        # Cuelist Settings
        output += "\n    Cuelist Settings:"
        output += f"\n        Deactivate after last cue: {bool(cuelist.at_end_stop)}"
        output += f"\n        Deactivate resets to first cue: {bool(cuelist.autoreset)}"
        output += f"\n        Halt last cue: {bool(cuelist.at_end_pause)}"
        output += f"\n        Block FX: {bool(cuelist.block_fx)}"
        output += f"\n        Deactivate Time: {cuelist.ms_stop_time}ms"
        
        # Chase settings
        if cuelist.chase:
            output += "\n\n    Chase:"
            output += f"\n        Chase Time: {cuelist.ms_chase_time}ms"
            output += f"\n        Chase Speed: {cuelist.bpm_chase} bpm" if cuelist.bpm_chase else ""
            output += f"\n        Crossfade %: {cuelist.pcrossfade}%" if cuelist.pcrossfade else ""
            output += f"\n        Loops: {cuelist.loops}" if cuelist.loops else ""
            
            # Map direction number to human-readable format
            direction_map = {
                0: "Forward",
                1: "Backward",
                2: "Ping Pong",
                3: "Random"
            }
            direction = direction_map.get(cuelist.direction, f"Unknown ({cuelist.direction})")
            output += f"\n        Direction: {direction}"
        
        # Cues
        if cuelist.cuelist_elements:
            output += "\n\n    Cue Order:"
            dottedids = [element.dotted_id for element in cuelist.cuelist_elements]
            for element in cuelist.cuelist_elements:
                if element.cue_id is None:
                    continue

                cue_name = ""
                if element.cue_id in lightshow.cues:
                    cue_name = lightshow.cues[element.cue_id].name or ""
                
                wait_time = "Halt" if element.halt else f"{element.ms_duration}ms"
                
                crossfade = f"{element.ms_crossfade}ms"
                fade_in = f"{element.ms_fadein}ms" 
                fade_out = f"{element.ms_fadeout}ms"
                
                next_cue = str(element.next) if (element.next != 255) and (255 not in dottedids) else "Next"
                
                # Format dotted_id with last 2 digits as decimal part
                formatted_dotted_id = ""
                if element.dotted_id and len(str(element.dotted_id)) > 2:
                    dotted_str = str(element.dotted_id)
                    formatted_dotted_id = f"{dotted_str[:-2]}.{dotted_str[-2:]}"
                
                output += (
                    f"\n        {formatted_dotted_id}: {cue_name} | "
                    f"Wait: {wait_time} | "
                    f"Crossfade: {crossfade} | "
                    f"Fade In: {fade_in} | "
                    f"Fade Out: {fade_out} | "
                    f"Next Cue: {next_cue}"
                )
    
    return output