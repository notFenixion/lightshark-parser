from __future__ import annotations
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime
from lightshark_parser.classes import cuelist
from lightshark_parser.serialisers.attribute_serialisers import *
import copy
from lightshark_parser.classes.fileinfo import FileInfo
from lightshark_parser.classes.model import Model
from lightshark_parser.classes.patch import Patch
from lightshark_parser.classes.group import Group
from lightshark_parser.classes.order import Order
from lightshark_parser.classes.user_palette import UserPalette
from lightshark_parser.classes.cue import Cue
from lightshark_parser.classes.cuelist import Cuelist, CuelistElement
from lightshark_parser.classes.playback import Playback
from lightshark_parser.classes.fx import FX, FXPalette
from lightshark_parser.classes.general import General
from lightshark_parser.utils.json_mappings import get_section_from_ftype
from lightshark_parser.utils.logger import logger


class Lightshow:
    def __init__(
        self,
        # filepath: str = None,
        fileinfo: FileInfo = None,
        models: Dict[int, Model] = None,
        patches: Dict[int, Patch] = None,
        groups: Dict[int, Group] = None,
        user_palettes: Dict[int, UserPalette] = None,
        cues: Dict[int, Cue] = None,
        cuelists: Dict[int, Cuelist] = None,
        playbacks: Dict[str, Playback] = None,
        fxpalettes: Dict[int, FXPalette] = None,
        general: General = None,
    ):  
        # if filepath is not None:
        #     self._filepath = Path(filepath)
        #     if not self._filepath.exists():
        #         raise FileNotFoundError(f"File {filepath} does not exist")
        #     self._filename = self._filepath.name
        #     stats = self._filepath.stat()
        #     created_at = datetime.fromtimestamp(stats.st_ctime)
        #     modified_at = datetime.fromtimestamp(stats.st_mtime)
        #     self._created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        #     self._modified_at = modified_at.strftime("%Y-%m-%d %H:%M:%S")
        # else:
        #     self._filepath = None
        #     self._filename = None
        #     self._created_at = None
        #     self._modified_at = None

        self._parsed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._fileinfo: FileInfo = fileinfo
        self._models: Dict[int, Model] = models or {}
        self._patches: Dict[int, Patch] = patches or {}
        self._groups: Dict[int, Group] = groups or {}
        self._user_palettes: Dict[int, UserPalette] = user_palettes or {}
        self._cues: Dict[int, Cue] = cues or {}
        self._cuelists: Dict[int, Cuelist] = cuelists or {}
        self._playbacks: Dict[str, Playback] = playbacks or {}
        self._fxpalettes: Dict[int, FXPalette] = fxpalettes or {}
        self._general: General = general
        
        # Log initialization summary
        logger.info(f"Lightshow initialized with {len(models or {})} models, "
                   f"{len(patches or {})} patches, {len(user_palettes or {})} palettes, "
                   f"{len(cues or {})} cues, {len(cuelists or {})} cuelists")

    # Getters and setters
    # @property
    # def filepath(self) -> Path:
    #     return self._filepath
        
    # @property
    # def filename(self) -> str:
    #     return self._filename
        
    # @property
    # def parsed_date(self) -> str:
    #     return self._parsed_date
        
    # @property
    # def created_at(self) -> str:
    #     return self._created_at
        
    # @property
    # def modified_at(self) -> str:
    #     return self._modified_at

    # Property getters for section attributes
    @property
    def fileinfo(self) -> FileInfo:
        return self._fileinfo
        
    @fileinfo.setter
    def fileinfo(self, value: FileInfo) -> None:
        self._fileinfo = value
        
    @property
    def models(self) -> Dict[Any, Model]:
        return self._models
        
    @models.setter
    def models(self, value: Dict[Any, Model]) -> None:
        for model in value.values():
            if model.__class__.__name__ != 'Model':
                raise TypeError("All model values must be Model objects")
        self._models = value
        
    @property
    def patches(self) -> Dict[Any, Patch]:
        return self._patches
        
    @patches.setter
    def patches(self, value: Dict[Any, Patch]) -> None:
        for patch in value.values():
            if patch.__class__.__name__ != 'Patch':
                raise TypeError("All patch values must be Patch objects")
        self._patches = value
        
    @property
    def groups(self) -> Dict[Any, Group]:
        return self._groups
        
    @groups.setter
    def groups(self, value: Dict[Any, Group]) -> None:

        for group in value.values():
            if group.__class__.__name__ != 'Group':
                raise TypeError("All group values must be Group objects")
        self._groups = value

    def add_group(self, group: Group) -> None:
        if group.__class__.__name__ != 'Group':
            raise TypeError("Parameter given must be a Group object")
        self._groups[group.group_id] = group
    
        
    @property
    def user_palettes(self) -> Dict[Any, UserPalette]:
        return self._user_palettes
        
    @user_palettes.setter
    def user_palettes(self, value: Dict[Any, UserPalette]) -> None:
        for palette in value.values():
            if palette.__class__.__name__ != 'UserPalette':
                raise TypeError("All user_palette values must be UserPalette objects")
        self._user_palettes = value
        
    @property
    def cues(self) -> Dict[Any, Cue]:
        return self._cues
        
    @cues.setter
    def cues(self, value: Dict[Any, Cue]) -> None:
        for cue in value.values():
            if cue.__class__.__name__ != 'Cue':
                raise TypeError("All cue values must be Cue objects")
        self._cues = value
        
    @property
    def cuelists(self) -> Dict[Any, Cuelist]:
        return self._cuelists
        
    @cuelists.setter
    def cuelists(self, value: Dict[Any, Cuelist]) -> None:
        for cuelist in value.values():
            if cuelist.__class__.__name__ != 'Cuelist':
                raise TypeError("All cuelist values must be Cuelist objects")
        self._cuelists = value
        
    @property
    def playbacks(self) -> Dict[Any, Playback]:
        return self._playbacks
        
    @playbacks.setter
    def playbacks(self, value: Dict[Any, Playback]) -> None:
        for playback in value.values():
            if playback.__class__.__name__ != 'Playback':
                raise TypeError("All playback values must be Playback objects")
        self._playbacks = value
        
    @property
    def fxpalettes(self) -> Dict[Any, FXPalette]:
        return self._fxpalettes
        
    @fxpalettes.setter
    def fxpalettes(self, value: Dict[Any, FXPalette]) -> None:
        for fxpalette in value.values():
            if fxpalette.__class__.__name__ != 'FXPalette':
                raise TypeError("All fxpalette values must be FXPalette objects")
        self._fxpalettes = value
        
    @property
    def general(self) -> General:
        return self._general
        
    @general.setter
    def general(self, value: General) -> None:
        self._general = value


    ### PATCH / FIXTURE FUNCTIONS ###

    def move_patches(self, patch_ids: list[int], new_visual_id: int) -> None:
        """
        Move selected group to new visual IDs, starting with new_visual_id and incrementing by 1 for each group.
        """
        visual_ids = [patch.visual_id for patch in self._patches.values()]
        c = 0

        for patch_id in patch_ids:
            if patch_id not in self._patches:
                raise ValueError(f"Patch with ID {patch_id} does not exist")
            if new_visual_id + c in visual_ids:
                raise ValueError(f"Visual ID {new_visual_id} already exists for another patch. Cannot move patch {patch_id} to this visual ID.")
            c += 1

        for patch_id in patch_ids:
            patch = self._patches[patch_id]
            patch.visual_id = new_visual_id
            new_visual_id += 1
    
    
    ### GROUP FUNCTIONS ###

    def add_new_group(self, visual_id: int, patched_elements_ids: list[int]) -> Group:
        """
        Group implementation already handles the grid, steps, etc. as optional attributes.
        Only group_id, visual_id, and patched_elements_ids are compulsory.
        """
        group_id = max(self._groups.keys(), default=0) + 1
        if not isinstance(patched_elements_ids, list):
            raise TypeError("patched_elements_ids must be a list of integers")
        if not all(isinstance(id, int) for id in patched_elements_ids):
            raise TypeError("All elements in patched_elements_ids must be integers")
        group = Group(
            patched_elements_ids=patched_elements_ids,
            group_id=group_id,
            visual_id=visual_id,
        )
        self._groups[group_id] = group
        return group

    def update_group(self, group_id: int, patched_elements_ids: Optional[list[int]] = None, visual_id: Optional[int] = None) -> None:
        """
        Updates an existing group with new patched_elements_ids and/or visual_id.
        This handles both REC overriding a group and moving a group to a different grid position (diff visual_id).
        """
        if group_id not in self._groups:
            raise ValueError(f"Group with ID {group_id} does not exist")
        
        group = self._groups[group_id]
        
        if patched_elements_ids is not None:
            if not isinstance(patched_elements_ids, list):
                raise TypeError("patched_elements_ids must be a list of integers")
            if not all(isinstance(id, int) for id in patched_elements_ids):
                raise TypeError("All elements in patched_elements_ids must be integers")
            group.patched_elements_ids = patched_elements_ids

            # Set grid and steps to default
            # NOTE: For future implementation, allow update_group to update grid and steps as well. For now, leave that to the user irl
            grid = {}
            for i, fixture_id in enumerate(patched_elements_ids, start=0):
                grid[fixture_id] = [0, i]

            steps = {}
            for fixture_id in patched_elements_ids:
                steps[fixture_id] = 0

        
        if visual_id is not None:
            group.visual_id = visual_id


    def delete_group(self, group_id: int) -> None:
        if group_id not in self._groups:
            raise ValueError(f"Group with ID {group_id} does not exist")
        del self._groups[group_id]


    def copy_group(self, copied_group_id: int, new_visual_id: int) -> None:
        group = self._groups.get(copied_group_id)
        if group is None:
            raise ValueError(f"Group with ID {copied_group_id} does not exist")
        new_group_id = max(self._groups.keys(), default=0) + 1
        new_group = copy.deepcopy(group)
        new_group.group_id = new_group_id
        new_group.visual_id = new_visual_id
        self._groups[new_group_id] = new_group

    def move_groups(self, group_ids: list[int], new_visual_id: int) -> None:
        """
        Move selected group to new visual IDs, starting with new_visual_id and incrementing by 1 for each group.
        """
        visual_ids = [grp.visual_id for grp in self._groups.values()]
        c = 0

        for group_id in group_ids:
            if group_id not in self._groups:
                raise ValueError(f"Group with ID {group_id} does not exist")
            if new_visual_id + c in visual_ids:
                raise ValueError(f"Visual ID {new_visual_id} already exists for another group. Cannot move group {group_id} to this visual ID.")
            c += 1

        for group_id in group_ids:
            group = self._groups[group_id]
            group.visual_id = new_visual_id
            new_visual_id += 1
    
    ### ORDER FUNCTIONS ###

    def add_new_order(self, palette_id, patch_id, ftype, value) -> Order:
        patch = self._patches.get(patch_id)
        model = self._models.get(patch.model_id)
        universe = patch.universe
        if ftype == 516 and model.use_virtual_dimmer:
            universe = 9

        channel = patch.index
        for modelvalue in model.values:
            if modelvalue.ftype == ftype:
                channel += modelvalue.index
                break

        
        order = Order(
            palette_id=palette_id,
            patch_id=patch_id,
            ftype=ftype,
            value=value,
            universe=universe,
            section=get_section_from_ftype(ftype),
            receptor_type=1 if ftype == 516 else 0,
            channel=channel,
        )
        logger.debug(f"Creatined order: patch_id={patch_id}, ftype={ftype}, value={value}, palette_id={palette_id}")
        return order


    def _get_or_create_order(self, patch_id: int, ftype: int, value: int, palette_id: int) -> Order:
        """
        Modular function to either:
        - Create a new standalone order (if palette_id == 0)
        - Return reference to existing palette order (if palette_id != 0)
        
        This handles the common pattern of "create new order or reference palette order depending on palette_id"
        """
        if palette_id == 0:
            # Create standalone order
            logger.debug(f"Creating standalone order for patch_id={patch_id}, ftype={ftype}")
            return self.add_new_order(
                palette_id=0,
                patch_id=patch_id,
                ftype=ftype,
                value=value
            )
        else:
            # Reference palette order
            logger.debug(f"Referencing palette order: palette_id={palette_id}, patch_id={patch_id}, ftype={ftype}")
            palette = self._user_palettes.get(palette_id)
            if palette is None:
                raise ValueError(f"Palette with ID {palette_id} does not exist")
            
            if (patch_id not in palette.orders or 
                ftype not in palette.orders[patch_id]):
                raise ValueError(f"Order for patch_id={patch_id}, ftype={ftype} does not exist in palette {palette_id}")
            
            return palette.orders[patch_id][ftype]

    def _copy_order_to_referencing_cues(self, order_to_copy: Order, patch_id: int, ftype: int) -> None:
        """
        Helper method to copy an Order object to all cues that currently reference it.
        This prevents breaking cues when removing orders from palettes.
        """
        # Find all cues that reference this specific order object
        for cue in self._cues.values():
            if (cue.orders and 
                patch_id in cue.orders and 
                ftype in cue.orders[patch_id] and
                cue.orders[patch_id][ftype] is order_to_copy):
                
                # Create an independent copy of the order for this cue
                cue.orders[patch_id][ftype] = Order(
                    palette_id=0,  # Mark as cue-specific (no longer from palette)
                    patch_id=order_to_copy.patch_id,
                    ftype=order_to_copy.ftype,
                    value=order_to_copy.value,
                    universe=order_to_copy.universe,
                    section=order_to_copy.section,
                    receptor_type=order_to_copy.receptor_type,
                    channel=order_to_copy.channel,
                )

    ### PALETTE FUNCTIONS ###

    def update_palette_orders(self, palette_id: int, new_orders: dict[int, dict[int, int]]) -> None:
        """
        Takes in a dict of {patch_id: {ftype: value}} and updates Orders accordingly.
        If Order already exists, value is simply updated.
        If Order does not exist, a new Order is created. For non-specified attributes, the following schema is used to generate the Order:
        - patch_id: take from dict
        - channel: patch.index + index of the model.values entry corresponding to the ftype
        - universe: universe of the patch. For virtual dimmers (ftype=516 + model uses virtual dimmer), universe is set to 9. [NOTE: unconfirmed]
        - section: ftyped is mapped to a section [NOTE: mapping is not fully complete]
        - receptor_type: if ftype=516, set to 1 [NOTE: unconfirmed]
        
        Orders that exist in the palette but are not specified in new_orders will be removed from the palette.
        If those orders are shared with cues, the cues will get independent copies to prevent breaking.
        """
        logger.info(f"Updating palette {palette_id} with {sum(len(ftypes) for ftypes in new_orders.values())} orders")
        
        if not isinstance(new_orders, dict):
            raise TypeError("new_orders must be a dictionary")
        
        palette = self._user_palettes.get(palette_id)
        if palette is None:
            raise ValueError(f"Palette with ID {palette_id} does not exist")
        
        # First, handle orders that will be removed - copy them to cues that reference them
        for patch_id in list(palette.orders.keys()):
            if patch_id in new_orders:
                # Check ftypes that will be removed for this patch
                for ftype in list(palette.orders[patch_id].keys()):
                    if ftype not in new_orders[patch_id]:
                        order_to_remove = palette.orders[patch_id][ftype]
                        self._copy_order_to_referencing_cues(order_to_remove, patch_id, ftype)
                        del palette.orders[patch_id][ftype]
                # Remove empty patch dict if no ftypes remain
                if not palette.orders[patch_id]:
                    del palette.orders[patch_id]
            else:
                # All orders for this patch will be removed - copy them all to cues
                for ftype, order_to_remove in palette.orders[patch_id].items():
                    self._copy_order_to_referencing_cues(order_to_remove, patch_id, ftype)
                del palette.orders[patch_id]
        
        # Then, update/create orders based on new_orders
        for patch_id, ftype_orders in new_orders.items():
            # Initialize patch_id dict if it doesn't exist
            if patch_id not in palette.orders:
                palette.orders[patch_id] = {}
                
            for ftype, value in ftype_orders.items():
                if ftype not in palette.orders[patch_id]:
                    # Create a new Order if it doesn't exist
                    logger.debug(f"Creating new order in palette {palette_id}: patch_id={patch_id}, ftype={ftype}, value={value}")
                    palette.orders[patch_id][ftype] = self.add_new_order(
                        palette_id=palette_id,
                        patch_id=patch_id,
                        ftype=ftype,
                        value=value
                    )
                else:
                    # Update the existing Order's value
                    logger.debug(f"Updating existing order in palette {palette_id}: patch_id={patch_id}, ftype={ftype}, value={value}")
                    palette.orders[patch_id][ftype].value = value
        


    def add_new_palette(self, orders: dict[int, dict[int, int]]) -> UserPalette:

        palette_id = max(self._user_palettes.keys(), default=0) + 1
        palette = UserPalette(
            user_palette_id=palette_id,
            name=f"Palette {palette_id}",
            orders={patch_id: {} for patch_id in orders.keys()} if orders else {},
        )
        self._user_palettes[palette_id] = palette
        self.update_palette_orders(palette_id=palette_id, new_orders=orders)
        palette.section = palette.orders[next(iter(orders))][next(iter(orders[next(iter(orders))]))].section 
        return palette 


    def delete_palette(self, palette_id: int) -> None:
        if palette_id not in self._user_palettes:
            raise ValueError(f"Palette with ID {palette_id} does not exist")
        del self._user_palettes[palette_id]

    ### CUE FUNCTIONS ###


    def add_new_cue(self, cuelist_id: int, orders: dict[int, dict[int, List[int, int]]], fxs: List[FX]=None, fx_palette: Union[int, str] = "N/A") -> Cue:
        """
        orders is {patch_id: {ftype: [value, palette_id]}}
        palette_id is optional, set to 0 if None (same as how file stores)
        if a palette_id is provided, it will use that palette's Order instead. else create new Order     

        i think fx_palette = "N/A" shld be handled alr???

        NOTE: 
        THIS ALSO RUNS add_cue_to_cuelist, so it will automatically add the cue to the cuelist on init.
        Cues *must* be assigned to exactly 1 cuelist.
        """
        logger.info(f"Adding new cue to cuelist {cuelist_id}.")
        
        cuelist = self._cuelists.get(cuelist_id)
        
        # Find the highest dotted_id in cuelist elements and calculate next visual_id
        if cuelist.cuelist_elements:
            # Get the maximum dotted_id from the CuelistElement objects (not the keys)
            max_dotted_id = max(element.dotted_id for element in cuelist.cuelist_elements.values())
            visual_id = ((max_dotted_id // 100) + 1) * 100
        else:
            # Empty cuelist, start at 1.00
            visual_id = 100

        if fxs == [] or fxs == None:
            fxs_channels = [0 for _ in range(16)]
        else:
            # TO BE IMPLEMENTED :(
            pass

        cue_id = max(self._cues.keys(), default=0) + 1

        # Process orders and create/get Order objects
        processed_orders = {}
        for patch_id, ftype_orders in orders.items():
            processed_orders[patch_id] = {}
            for ftype, order_values in ftype_orders.items():
                value, palette_id = order_values
                # Use modular function to handle order creation/referencing
                order = self._get_or_create_order(patch_id, ftype, value, palette_id)
                processed_orders[patch_id][ftype] = order

        cue = Cue(
            cue_id=cue_id,
            visual_id=visual_id,
            orders=processed_orders,
            fxs=fxs,
            fx_palette=fx_palette,
            fxs_channels=fxs_channels,
            name = f"Cue {cue_id}"
        )
        self._cues[cue_id] = cue
        self._add_cue_to_cuelist(cue_id, cuelist_id)
        
        logger.info(f"Successfully created cue {cue_id} with visual_id {visual_id} in cuelist {cuelist_id}")
        return cue


    def update_cue(self, cue_id: int, updated_values: Dict[str, Any]) -> None:
        """
        Ignore FX for now, will be implemented later
        Updatable values:
        - fxs, fx_palette, fxs_channels, orders, description, name
        """
        cue = self._cues.get(cue_id)
        if cue is None:
            raise ValueError(f"Cue with ID {cue_id} does not exist")

        for key, value in updated_values.items():
            if key == "orders":
                self.update_cue_orders(cue_id, value)
            elif hasattr(cue, key) and key in ['fxs', 'fx_palette', 'fxs_channels', 'description', 'name']:
                setattr(cue, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}' for Cue")
    
    def update_cue_orders(self, cue_id: int, new_orders: dict[int, dict[int, (int, int)]]) -> None:
        """
        Takes in a dict of {patch_id: {ftype: (value, palette_id)}} and updates Orders accordingly for a specific cue.
        If new Order given has palette_id != 0, Order is set to reference the palette's corresponding Order.
        Otherwise, follow the same logic as in update_palette_orders:
        - If order doesn't exist yet, create it
        - If order exists already, update value directly
        
        Orders that exist in the cue but are not specified in new_orders will be removed from the cue.
        For palette-referenced orders (palette_id != 0), only the reference is removed (Order stays in palette).
        For cue-specific orders (palette_id == 0), the Order object is deleted since only this cue uses it.
        """
        logger.info(f"Updating orders for cue {cue_id} with {sum(len(ftypes) for ftypes in new_orders.values())} orders")
        
        if not isinstance(new_orders, dict):
            raise TypeError("new_orders must be a dictionary")
        
        cue = self._cues.get(cue_id)
        if cue is None:
            raise ValueError(f"Cue with ID {cue_id} does not exist")
        
        # Initialize cue.orders if it's None
        if cue.orders is None:
            cue.orders = {}
        
        # First, remove orders that are not in new_orders
        for patch_id in list(cue.orders.keys()):
            if patch_id in new_orders:
                # Remove ftypes that are not in new_orders for this patch
                for ftype in list(cue.orders[patch_id].keys()):
                    if ftype not in new_orders[patch_id]:
                        order_to_remove = cue.orders[patch_id][ftype]
                        # Only delete the reference, not the Order object itself
                        # The Order object will be garbage collected only if this was the last reference
                        # (which happens automatically for cue-specific orders with palette_id=0)
                        del cue.orders[patch_id][ftype]
                # Remove empty patch dict if no ftypes remain
                if not cue.orders[patch_id]:
                    del cue.orders[patch_id]
            else:
                # Remove entire patch if not in new_orders
                for ftype in cue.orders[patch_id]:
                    # Same logic - just remove references, let garbage collection handle the rest
                    pass
                del cue.orders[patch_id]
            
        # Then, update/create orders based on new_orders
        for patch_id, ftype_orders in new_orders.items():
            # Initialize patch_id dict if it doesn't exist
            if patch_id not in cue.orders:
                cue.orders[patch_id] = {}
                
            for ftype, (value, palette_id) in ftype_orders.items():
                # Check if we're replacing an existing order
                existing_order = cue.orders[patch_id].get(ftype)
                
                if existing_order is not None:
                    # Case 1: patch_id, ftype pair is already taken
                    if existing_order.palette_id == 0:
                        # Case 1a: old order has palette_id == 0 -> delete order, replace with new
                        logger.debug(f"Case 1a: Replacing cue-specific order (patch_id={patch_id}, ftype={ftype}) with {'palette reference' if palette_id != 0 else 'new cue-specific order'}")
                        pass  # The reference will be overwritten below
                    else:
                        # Case 1b: old order has palette_id != 0 -> don't delete order, just replace reference
                        logger.debug(f"Case 1b: Replacing palette reference (patch_id={patch_id}, ftype={ftype}) with {'new palette reference' if palette_id != 0 else 'cue-specific order'}")
                        pass  # The reference will be overwritten below
                    
                    # In both cases, replace with new order/reference
                    cue.orders[patch_id][ftype] = self._get_or_create_order(patch_id, ftype, value, palette_id)
                else:
                    # Case 2: pair is not taken -> create new order or reference
                    logger.debug(f"Case 2: Creating new {'palette reference' if palette_id != 0 else 'cue-specific order'} (patch_id={patch_id}, ftype={ftype})")
                    cue.orders[patch_id][ftype] = self._get_or_create_order(patch_id, ftype, value, palette_id)


    def delete_cue(self, cuelist_id: int, cue_id: int) -> None:
        # Deletes the cuelist_elements as well
        logger.info(f"Deleting cue {cue_id} from cuelist {cuelist_id}")
        
        cuelist = self._cuelists.get(cuelist_id)
        dotted_id = self._cues[cue_id].visual_id
        if cuelist is None:
            raise ValueError(f"Cuelist with ID {cuelist_id} does not exist")
        if dotted_id not in cuelist.cuelist_elements:
            raise ValueError(f"Cuelist element with dotted_id {dotted_id} does not exist in cuelist {cuelist_id}")

        del cuelist.cuelist_elements[dotted_id]
        del self._cues[cue_id]
        logger.info(f"Successfully deleted cue {cue_id} and its cuelist element")

    ### CUELIST FUNCTIONS ###

    def add_new_cuelist(self) -> Cuelist:
        logger.info("Creating new cuelist")
        
        cuelist_id = max(self._cuelists.keys(), default=0) + 1
        visual_id = max((cuelist.visual_id for cuelist in self._cuelists.values()), default=0) + 1
        # rest of the attributes will use the default init
        cuelist = Cuelist(
            cuelist_id=cuelist_id,
            visual_id=visual_id
        )
        self._cuelists[cuelist_id] = cuelist
        
        logger.info(f"Created cuelist {cuelist_id} with visual_id {visual_id}")
        return cuelist

    def _add_cue_to_cuelist(self, cue_id: int, cuelist_id: int) -> None:
        logger.debug(f"Adding cue {cue_id} to cuelist {cuelist_id}")
        
        cue = self._cues.get(cue_id)
        if cue is None:
            raise ValueError(f"Cue with ID {cue_id} does not exist")

        cuelist_element = CuelistElement(
            ms_crossfade=0,
            ms_delay=0,
            ms_fadein=0,
            ms_fadeout=0,
            ms_duration=2000,
            halt=True,
            cue_id=cue_id,
            dotted_id=cue.visual_id,
            next="Next"
        )

        self._cuelists[cuelist_id].cuelist_elements[cue.visual_id] = cuelist_element
        logger.debug(f"Successfully added cue {cue_id} to cuelist {cuelist_id} with dotted_id {cue.visual_id}")

    def update_cuelist_element(self,
        cuelist_id: int,
        curr_dotted_id: int,
        updated_values: Dict[str, Any]   
    ):
        logger.debug(f"Updating cuelist element with cuelist_id={cuelist_id}, dotted_id={curr_dotted_id}: {updated_values}")

        cuelist = self._cuelists.get(cuelist_id)
        if cuelist is None:
            raise ValueError(f"Cuelist with ID {cuelist_id} does not exist")
        if curr_dotted_id not in cuelist.cuelist_elements:
            raise ValueError(f"Cuelist element with dotted_id {curr_dotted_id} does not exist in cuelist {cuelist_id}")

        element = cuelist.cuelist_elements[curr_dotted_id]
        existing_dotted_ids = set(cuelist.cuelist_elements.keys())
        
        for key, value in updated_values.items():
            if hasattr(element, key):
                if key == 'dotted_id':
                    # Ignore dotted_id values <= 100 cuz IDs start from 1.00
                    if value <= 100:
                        continue
                    if value in existing_dotted_ids:
                        logger.debug(f"Dotted ID {value} already exists in cuelist {cuelist_id}. Finding next available dotted_id.")
                        value = self._find_next_dottedid(value, existing_dotted_ids)
                    
                    # Update the dotted_id on the element object
                    setattr(element, key, value)
                    
                    # If dotted_id actually changed, update the dictionary key
                    if value != curr_dotted_id:
                        cuelist.cuelist_elements[value] = cuelist.cuelist_elements.pop(curr_dotted_id)
                        
                        # Update visual_id of the cue as well
                        cue = self._cues[element.cue_id]
                        cue.visual_id = value

                elif key == 'next':
                    if isinstance(value, int):
                        if value not in existing_dotted_ids:
                            value = "Next"
                    else:
                        # Invalid type for next
                        raise ValueError(f"Invalid value for 'next': {value}. Must be an integer dotted_id or 'Next'")
                    
                    setattr(element, key, value)

                elif key == 'ms_duration':
                    element.halt = (value == 0)
                    setattr(element, key, value)
                
                else:
                    setattr(element, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}' for CuelistElement")
    

    def delete_cuelist(self, cuelist_id: int) -> None:
        logger.info(f"Deleting cuelist {cuelist_id}")
        
        if cuelist_id not in self._cuelists:
            raise ValueError(f"Cuelist with ID {cuelist_id} does not exist")
        
        # Check if cuelist is assigned to a playback currently
        for playback in self._playbacks.values():
            if playback.cuelist == cuelist_id:
                raise ValueError(f"Cuelist with ID {cuelist_id} is currently assigned to playback {playback.combined_id}. Unable to delete.")

        # Delete all cues and cuelistelements associated with this cuelist
        cue_count = len(self._cuelists[cuelist_id].cuelist_elements)
        logger.debug(f"Deleting {cue_count} cues from cuelist {cuelist_id}")
        
        for cuelist_element in self._cuelists[cuelist_id].cuelist_elements.values():
            del self._cues[cuelist_element.cue_id]
            del cuelist_element

        del self._cuelists[cuelist_id]
        logger.info(f"Successfully deleted cuelist {cuelist_id} and {cue_count} associated cues")

    def _find_next_dottedid(self, value: int, existing_dotted_ids: set) -> int:
        """
        Find the next available dotted_id using the specified logic:
        1. Round up to next multiple of 10 within the same hundred (620, 630, etc.)
        2. If all multiples of 10 in that hundred are taken, increment by 1 (611, 612, etc.)
        3. Raise error if no space is available
        """
        if value not in existing_dotted_ids:
            return value
        
        # Get the base hundred (610 -> 600, 1250 -> 1200)
        base_hundred = (value // 100) * 100
        
        # Phase 1: Try multiples of 10 within the same hundred
        # Start from the next multiple of 10 after the current value
        next_multiple_of_10 = base_hundred + 10
        
        for candidate in range(next_multiple_of_10, base_hundred + 100, 10):
            if candidate == value or candidate not in existing_dotted_ids:
                return candidate
        
        # Phase 2: Try incrementing by 1 from the original value
        for candidate in range(value + 1, base_hundred + 100):
            if candidate == value or candidate not in existing_dotted_ids:
                return candidate
        
        # If we reach here, the entire hundred block is full
        raise ValueError(f"No available dotted_id found in the range {base_hundred}-{base_hundred + 99}. All positions are occupied.")

        


    ### PLAYBACK FUNCTIONS ###

    def assign_playback(self, page: int, index: int, cuelist_id: int):
        # Assign cuelist to blank playback.
        # Can't assign to a taken playback cuz that would just record cue to cuelist
        
        combined_id = f"{page}.{index}"
        if combined_id in self._playbacks:
            raise ValueError(f"Playback with page {page} and index {index} already exists")
        playback = Playback(page=page, index=index, cuelist=cuelist_id)
        self._playbacks[combined_id] = playback

        logger.info(f"Assigned cuelist {cuelist_id} to playback {combined_id}")


    def unassign_playback(self, page: int, index: int):
        # Unassign playback by removing it from the playbacks dict.
        combined_id = f"{page}.{index}"
        if combined_id not in self._playbacks:
            raise ValueError(f"Playback with page {page} and index {index} does not exist")
        del self._playbacks[combined_id]

        logger.info(f"Unassigned playback {combined_id}")



    def __repr__(self):
        return (
            f"Lightshow(fileinfo={self._fileinfo!r}, models={self._models!r}, "
            f"patches={self._patches!r}, groups={self._groups!r}, "
            f"user_palettes={self._user_palettes!r}, cues={self._cues!r}, "
            f"cuelists={self._cuelists!r}, playbacks={self._playbacks!r}, "
            f"fxpalettes={self._fxpalettes!r}, general={self._general!r})"
        )




    ### MISC ###

    def to_dict(self) -> Dict:
        def to_dict_recursive(obj):
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                return obj.to_dict()
            elif hasattr(obj, "__dict__"):
                return {k: to_dict_recursive(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, (list, tuple)):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): to_dict_recursive(v) for k, v in obj.items()}
            return obj

        return {
            # "filepath": str(self._filepath) if self._filepath else None,
            # "filename": self._filename,
            # "parsed_date": self._parsed_date,
            # "created_at": self._created_at,
            # "modified_at": self._modified_at,
            "fileinfo": to_dict_recursive(self._fileinfo),
            "models": {str(k): to_dict_recursive(v) for k, v in self._models.items()} if self._models else {},
            "patches": {str(k): to_dict_recursive(v) for k, v in self._patches.items()} if self._patches else {},
            "groups": {str(k): to_dict_recursive(v) for k, v in self._groups.items()} if self._groups else {},
            "user_palettes": {str(k): to_dict_recursive(v) for k, v in self._user_palettes.items()} if self._user_palettes else {},
            "cues": {str(k): to_dict_recursive(v) for k, v in self._cues.items()} if self._cues else {},
            "cuelists": {str(k): to_dict_recursive(v) for k, v in self._cuelists.items()} if self._cuelists else {},
            "playbacks": {str(k): to_dict_recursive(v) for k, v in self._playbacks.items()} if self._playbacks else {},
            "fxpalettes": {str(k): to_dict_recursive(v) for k, v in self._fxpalettes.items()} if self._fxpalettes else {},
            "general": to_dict_recursive(self._general),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lightshow":
        fileinfo = FileInfo.from_dict(data.get("fileinfo"))
        models = {int(k): Model.from_dict(v) for k, v in data.get("models", {}).items()}
        patches = {int(k): Patch.from_dict(v) for k, v in data.get("patches", {}).items()}
        groups = {int(k): Group.from_dict(v) for k, v in data.get("groups", {}).items()}
        user_palettes = {int(k): UserPalette.from_dict(v) for k, v in data.get("user_palettes", {}).items()}
        cues = {int(k): Cue.from_dict(v) for k, v in data.get("cues", {}).items()}
        cuelists = {int(k): Cuelist.from_dict(v) for k, v in data.get("cuelists", {}).items()}
        playbacks = {str(k): Playback.from_dict(v) for k, v in data.get("playbacks", {}).items()}
        fxpalettes = {int(k): FXPalette.from_dict(v) for k, v in data.get("fxpalettes", {}).items()}
        general = General.from_dict(data.get("general"))
        return cls(
            fileinfo=fileinfo,
            models=models,
            patches=patches,
            groups=groups,
            user_palettes=user_palettes,
            cues=cues,
            cuelists=cuelists,
            playbacks=playbacks,
            fxpalettes=fxpalettes,
            general=general,
        )

    def summarise(self):
        from lightshark_parser.summariser import format_lightshow
        return format_lightshow(self)
    
    def save_summary(self, filepath: Union[str, Path]) -> None:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        
        logger.debug(f"Saving Lightshow summary to {filepath}")
        with open(filepath, "w") as f:
            f.write(self.summarise())
        logger.info(f"Lightshow summary saved to {filepath}")
    
    def save_lightshow(self, filepath: Union[str, Path]) -> None:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.suffix == ".lshw":
            raise ValueError("Filepath must have .lshw extension")
        
        logger.debug(f"Saving Lightshow to {filepath}")
        with open(filepath, "wb") as f:
            f.write(self.to_bytes())
        logger.info(f"Lightshow saved to {filepath}")


    def to_bytes(self) -> bytes:
        logger.debug(f"Starting serialization of Lightshow object")
        bytestr = bytearray()
        if self._fileinfo is not None:
            bytestr.extend(self._fileinfo.to_bytes())

        bytestr.extend(serialise_section_header("#models#"))
        if self._models is not None:
            for model in self._models.values():
                bytestr.extend(model.to_bytes()) 

        bytestr.extend(serialise_section_header("#patching#"))
        if self._patches is not None:
            for patch in self._patches.values():
                bytestr.extend(patch.to_bytes())
        if self._groups is not None:
            for group in self._groups.values():
                bytestr.extend(group.to_bytes())
        
        bytestr.extend(serialise_section_header("#user_palettes#"))
        if self._user_palettes is not None:
            for palette in self._user_palettes.values():
                bytestr.extend(palette.to_bytes())

        bytestr.extend(serialise_section_header("#cues#"))
        if self._cues is not None:
            for cue in self._cues.values():
                bytestr.extend(cue.to_bytes())
        
        bytestr.extend(serialise_section_header("#cuelists#"))
        if self._cuelists is not None:
            for cuelist in self._cuelists.values():
                bytestr.extend(cuelist.to_bytes())
        
        bytestr.extend(serialise_section_header("#playbacks#"))
        if self._playbacks is not None:
            for playback in self._playbacks.values():
                bytestr.extend(playback.to_bytes())

        if self._general is not None:
            bytestr.extend(self._general.to_bytes())

        bytestr.extend(serialise_section_header("#fxpalettes#"))
        if self._fxpalettes is not None:
            for fxpalette in self._fxpalettes.values():
                bytestr.extend(fxpalette.to_bytes())
        
        bytestr.extend(serialise_section_header("#end#"))
        
        result = bytes(bytestr)
        
        return result