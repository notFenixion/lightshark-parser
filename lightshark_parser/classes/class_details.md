# LightShark Parser Class Details

This document provides a comprehensive overview of all classes in the LightShark Parser, including their attributes, types, and relationships.

## Table of Contents

- [LightShark Parser Class Details](#lightshark-parser-class-details)
  - [Table of Contents](#table-of-contents)
  - [Version](#version)
  - [FileInfo](#fileinfo)
  - [ModelPalette](#modelpalette)
  - [ModelHardware](#modelhardware)
  - [MacroStep](#macrostep)
  - [Macro](#macro)
  - [ModelValueStep](#modelvaluestep)
  - [ModelValue](#modelvalue)
  - [Model](#model)
  - [Patch](#patch)
  - [Group](#group)
  - [Order](#order)
  - [UserPalette](#userpalette)
  - [Cue](#cue)
  - [Cuelist](#cuelist)
  - [CuelistElement](#cuelistelement)
  - [Playback](#playback)
  - [FX](#fx)
  - [FXLayer](#fxlayer)
  - [FXLayerStep](#fxlayerstep)
  - [FXPalette](#fxpalette)
  - [Config](#config)
  - [General](#general)
  - [Action](#action)
  - [Lightshow](#lightshow)
  - [Relationships and Hierarchies](#relationships-and-hierarchies)
    - [Primary Containers](#primary-containers)
    - [Model Hierarchy](#model-hierarchy)
    - [Patch and Groups](#patch-and-groups)
    - [Palettes and Cues](#palettes-and-cues)
    - [FX System](#fx-system)
    - [Playback System](#playback-system)
    - [Cross-References](#cross-references)
  - [Implementation Notes](#implementation-notes)

---

## Version

**File:** `fileinfo.py`  
**Type:** `@dataclass`

| Attribute    | Type   | Default | Description                     |
| ------------ | ------ | ------- | ------------------------------- |
| `subversion` | `int`  | `None`  | Software subversion number      |
| `version`    | `int`  | `None`  | Software version number         |
| `autoload`   | `bool` | `None`  | Whether to autoload the version |
| `software`   | `str`  | `None`  | Software name/identifier        |

---

## FileInfo

**File:** `fileinfo.py`  
**Type:** Regular class

| Attribute | Type                | Default     | Description                      |
| --------- | ------------------- | ----------- | -------------------------------- |
| `version` | `Optional[Version]` | `Version()` | Version information for the file |

---

## ModelPalette

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute | Type                       | Default | Description                           |
| --------- | -------------------------- | ------- | ------------------------------------- |
| `color`   | `Optional[str]`            | `None`  | Color representation                  |
| `icon`    | `Optional[str]`            | `None`  | Icon identifier                       |
| `values`  | `Optional[dict[int, int]]` | `None`  | Dictionary of ftype to value mappings |
| `name`    | `Optional[str]`            | `None`  | Palette name                          |
| `type_id` | `Optional[str]`            | `None`  | Type identifier                       |

---

## ModelHardware

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute   | Type            | Default | Description               |
| ----------- | --------------- | ------- | ------------------------- |
| `width`     | `Optional[str]` | `None`  | Hardware width            |
| `depth`     | `Optional[str]` | `None`  | Hardware depth            |
| `max_power` | `Optional[str]` | `None`  | Maximum power consumption |
| `weight`    | `Optional[str]` | `None`  | Hardware weight           |
| `height`    | `Optional[str]` | `None`  | Hardware height           |

---

## MacroStep

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute | Type                  | Default | Description               |
| --------- | --------------------- | ------- | ------------------------- |
| `ms_wait` | `Optional[int]`       | `None`  | Wait time in milliseconds |
| `values`  | `Optional[List[Any]]` | `[]`    | List of macro step values |

---

## Macro

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute    | Type                        | Default | Description         |
| ------------ | --------------------------- | ------- | ------------------- |
| `macro_type` | `Optional[str]`             | `None`  | Type of macro       |
| `steps`      | `Optional[List[MacroStep]]` | `[]`    | List of macro steps |
| `name`       | `Optional[str]`             | `None`  | Macro name          |

---

## ModelValueStep

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute    | Type            | Default | Description                   |
| ------------ | --------------- | ------- | ----------------------------- |
| `step_name`  | `Optional[str]` | `None`  | Name of the step              |
| `step_value` | `Optional[int]` | `None`  | Numerical value of the step   |
| `min_str`    | `Optional[str]` | `None`  | Minimum string representation |
| `max_str`    | `Optional[str]` | `None`  | Maximum string representation |
| `symbol`     | `Optional[str]` | `None`  | Symbol representation         |

---

## ModelValue

**File:** `model.py`  
**Type:** `@dataclass`

| Attribute     | Type                                  | Default | Description               |
| ------------- | ------------------------------------- | ------- | ------------------------- |
| `index`       | `Optional[int]`                       | `None`  | Channel index             |
| `inverse`     | `Optional[bool]`                      | `None`  | Whether value is inverted |
| `instant`     | `Optional[bool]`                      | `None`  | Whether value is instant  |
| `description` | `Optional[str]`                       | `None`  | Value description         |
| `ftype`       | `Optional[int]`                       | `None`  | Feature type identifier   |
| `steps`       | `Optional[dict[int, ModelValueStep]]` | `{}`    | Dictionary of steps       |
| `htp`         | `Optional[bool]`                      | `None`  | Highest Takes Precedence  |
| `size`        | `Optional[int]`                       | `None`  | Size of the value         |

---

## Model

**File:** `model.py`  
**Type:** Regular class

| Attribute                 | Type                                | Default | Description                   |
| ------------------------- | ----------------------------------- | ------- | ----------------------------- |
| `model_id`                | `Optional[int]`                     | `None`  | Unique model identifier       |
| `palette`                 | `Optional[Dict[int, ModelPalette]]` | `None`  | Model palettes dictionary     |
| `name`                    | `Optional[str]`                     | `None`  | Model name                    |
| `short_name`              | `Optional[str]`                     | `None`  | Short model name              |
| `default_inverted_pan`    | `Optional[bool]`                    | `None`  | Default pan inversion         |
| `brand`                   | `Optional[str]`                     | `None`  | Model brand                   |
| `hardware`                | `Optional[ModelHardware]`           | `None`  | Hardware specifications       |
| `macros`                  | `Optional[Dict[str, Macro]]`        | `None`  | Model macros                  |
| `use_virtual_dimmer`      | `Optional[bool]`                    | `None`  | Whether to use virtual dimmer |
| `default_inverted_tilt`   | `Optional[bool]`                    | `None`  | Default tilt inversion        |
| `values`                  | `Optional[List[ModelValue]]`        | `None`  | List of model values          |
| `mode_name`               | `Optional[str]`                     | `None`  | Mode name                     |
| `virtual_dimmer_channels` | `Optional[List[int]]`               | `None`  | Virtual dimmer channels       |
| `size`                    | `Optional[int]`                     | `None`  | Model size                    |

---

## Patch

**File:** `patch.py`  
**Type:** Regular class

| Attribute        | Type             | Default | Description                       |
| ---------------- | ---------------- | ------- | --------------------------------- |
| `model_id`       | `Optional[int]`  | `None`  | Reference to model                |
| `inverse_tilt`   | `Optional[bool]` | `None`  | Tilt inversion setting            |
| `name`           | `Optional[str]`  | `None`  | Patch name                        |
| `channels_ftype` | `List[int]`      | `None`  | Channel feature types             |
| `index`          | `Optional[int]`  | `None`  | DMX start address                 |
| `universe`       | `Optional[int]`  | `None`  | DMX universe                      |
| `description`    | `Optional[str]`  | `None`  | Patch description                 |
| `inverse_pan`    | `Optional[bool]` | `None`  | Pan inversion setting             |
| `visual_id`      | `Optional[int]`  | `None`  | Visual grid position              |
| `parked`         | `Optional[bool]` | `None`  | Whether patch is parked           |
| `color_mark`     | `Optional[int]`  | `None`  | Color marking                     |
| `dimmer`         | `List[int]`      | `None`  | Dimmer configuration (8 elements) |
| `swap_pan_tilt`  | `Optional[bool]` | `None`  | Pan/Tilt axis swap                |
| `virtual_dimmer` | `List[int]`      | `None`  | Virtual dimmer configuration      |
| `id`             | `Optional[int]`  | `None`  | Unique patch identifier           |
| `size`           | `Optional[int]`  | `None`  | Patch size                        |
| `frozen`         | `Optional[int]`  | `None`  | Frozen state                      |

---

## Group

**File:** `group.py`  
**Type:** Regular class

| Attribute              | Type                             | Default               | Description                |
| ---------------------- | -------------------------------- | --------------------- | -------------------------- |
| `patched_elements_ids` | `List[int]`                      | Required              | List of patch IDs in group |
| `description`          | `Optional[str]`                  | `f"Group {group_id}"` | Group description          |
| `color_mark`           | `int`                            | `0`                   | Color marking              |
| `visual_id`            | `Optional[int]`                  | `None`                | Visual grid position       |
| `grid`                 | `Optional[Dict[int, List[int]]]` | Linear layout         | Grid positioning           |
| `steps`                | `Optional[Dict[int, int]]`       | All `0`               | Step priorities            |
| `automatico`           | `bool`                           | `False`               | Automatic mode             |
| `group_id`             | `Optional[int]`                  | `None`                | Unique group identifier    |

---

## Order

**File:** `order.py`  
**Type:** Regular class with `@dataclass` decorator

| Attribute       | Type  | Default | Description          |
| --------------- | ----- | ------- | -------------------- |
| `palette_id`    | `int` | `None`  | Reference to palette |
| `universe`      | `int` | `None`  | DMX universe         |
| `section`       | `int` | `None`  | Section identifier   |
| `receptor_type` | `int` | `None`  | Receptor type        |
| `patch_id`      | `int` | `None`  | Reference to patch   |
| `ftype`         | `int` | `None`  | Feature type         |
| `value`         | `int` | `None`  | Control value        |
| `channel`       | `int` | `None`  | DMX channel          |

---

## UserPalette

**File:** `user_palette.py`  
**Type:** Regular class

| Attribute         | Type                                    | Default | Description                      |
| ----------------- | --------------------------------------- | ------- | -------------------------------- |
| `section`         | `int`                                   | `None`  | Palette section                  |
| `user_palette_id` | `int`                                   | `None`  | Unique palette identifier        |
| `name`            | `str`                                   | `None`  | Palette name                     |
| `icon`            | `str`                                   | `None`  | Palette icon                     |
| `orders`          | `Optional[dict[int, dict[int, Order]]]` | `None`  | Nested orders by patch and ftype |

---

## Cue

**File:** `cue.py`  
**Type:** Regular class

| Attribute      | Type                                    | Default | Description                      |
| -------------- | --------------------------------------- | ------- | -------------------------------- |
| `fx_palette`   | `Optional[int\|str]`                    | `None`  | FX palette reference             |
| `cue_id`       | `Optional[int]`                         | `None`  | Unique cue identifier            |
| `description`  | `Optional[str]`                         | `None`  | Cue description                  |
| `visual_id`    | `Optional[int]`                         | `None`  | Visual grid position             |
| `fxs`          | `Optional[List[FX]]`                    | `[]`    | List of FX objects               |
| `fxs_channels` | `Optional[List[List[Union[int, str]]]]` | `None`  | FX channel configurations        |
| `orders`       | `Optional[dict[int, dict[int, Order]]]` | `None`  | Nested orders by patch and ftype |
| `actions`      | `Optional[List[Action]]`                | `None`  | List of actions                  |
| `name`         | `Optional[str]`                         | `None`  | Cue name                         |

---

## Cuelist

**File:** `cuelist.py`  
**Type:** Regular class

| Attribute          | Type                                  | Default                   | Description                                 |
| ------------------ | ------------------------------------- | ------------------------- | ------------------------------------------- |
| `ms_flash_attack`  | `Optional[int]`                       | `2000`                    | Flash attack time (ms)                      |
| `autoreset`        | `Optional[bool]`                      | `True`                    | Auto-reset setting                          |
| `at_end_pause`     | `Optional[bool]`                      | `False`                   | Pause at end                                |
| `loops`            | `Optional[int]`                       | `1`                       | Number of loops                             |
| `chase`            | `Optional[bool]`                      | `False`                   | Chase mode enabled                          |
| `ms_chase_time`    | `Optional[int]`                       | `2000`                    | Chase time (ms)                             |
| `visual_id`        | `Optional[int]`                       | `None`                    | Visual grid position                        |
| `bpm_chase`        | `Optional[int]`                       | `30000`                   | Chase BPM                                   |
| `ms_flash_decay`   | `Optional[int]`                       | `2000`                    | Flash decay time (ms)                       |
| `pcrossfade`       | `Optional[int]`                       | `100000`                  | Crossfade percentage                        |
| `ms_fadeout`       | `Optional[int]`                       | `2000`                    | Fade out time (ms)                          |
| `direction`        | `Optional[int]`                       | `0`                       | Chase direction                             |
| `at_end_stop`      | `Optional[bool]`                      | `False`                   | Stop at end                                 |
| `flash_mode`       | `Optional[int]`                       | `0`                       | Flash mode                                  |
| `cuelist_id`       | `Optional[int]`                       | `None`                    | Unique cuelist identifier                   |
| `ms_fadein`        | `Optional[int]`                       | `2000`                    | Fade in time (ms)                           |
| `ms_crossfade`     | `Optional[int]`                       | `2000`                    | Crossfade time (ms)                         |
| `no_first_fade`    | `Optional[bool]`                      | `False`                   | Skip first fade                             |
| `name`             | `Optional[str]`                       | `f"Cuelist {cuelist_id}"` | Cuelist name                                |
| `block_fx`         | `Optional[bool]`                      | `False`                   | Block FX                                    |
| `cuelist_elements` | `Optional[Dict[int, CuelistElement]]` | `{}`                      | Dictionary of cuelist elements by dotted_id |
| `ms_flash_hold`    | `Optional[int]`                       | `2000`                    | Flash hold time (ms)                        |
| `ms_stop_time`     | `Optional[int]`                       | `2000`                    | Stop time (ms)                              |

---

## CuelistElement

**File:** `cuelist.py`  
**Type:** Regular class

| Attribute      | Type             | Default | Description            |
| -------------- | ---------------- | ------- | ---------------------- |
| `ms_fadeout`   | `Optional[int]`  | `None`  | Fade out time (ms)     |
| `cue_id`       | `Optional[int]`  | `None`  | Reference to cue       |
| `ms_delay`     | `Optional[int]`  | `None`  | Delay time (ms)        |
| `next`         | `Optional[int]`  | `None`  | Next element reference |
| `dotted_id`    | `Optional[int]`  | `None`  | Dotted identifier      |
| `ms_fadein`    | `Optional[int]`  | `None`  | Fade in time (ms)      |
| `ms_crossfade` | `Optional[int]`  | `None`  | Crossfade time (ms)    |
| `ms_duration`  | `Optional[int]`  | `None`  | Duration time (ms)     |
| `halt`         | `Optional[bool]` | `None`  | Halt flag              |

---

## Playback

**File:** `playback.py`  
**Type:** Regular class

| Attribute             | Type                   | Default | Description            |
| --------------------- | ---------------------- | ------- | ---------------------- |
| `fader_value`         | `Optional[int]`        | `None`  | Current fader value    |
| `on_load_play`        | `Optional[bool]`       | `None`  | Play on load           |
| `fader_mode`          | `Optional[int]`        | `None`  | Fader mode             |
| `chase`               | `Optional[bool]`       | `None`  | Chase enabled          |
| `index`               | `Optional[int]`        | `None`  | Playback index         |
| `ms_chase_time`       | `Optional[int]`        | `None`  | Chase time (ms)        |
| `fader_up_play`       | `Optional[bool]`       | `None`  | Play on fader up       |
| `priority`            | `Optional[int]`        | `None`  | Playback priority      |
| `bpm_chase`           | `Optional[int]`        | `None`  | Chase BPM              |
| `on_page_stop`        | `Optional[bool]`       | `None`  | Stop on page change    |
| `trigger_level`       | `Optional[int]`        | `None`  | Trigger level          |
| `is_executor`         | `Optional[bool]`       | `None`  | Is executor            |
| `pcrossfade`          | `Optional[int]`        | `None`  | Crossfade percentage   |
| `ms_fadeout`          | `Optional[int]`        | `None`  | Fade out time (ms)     |
| `fader_down_stop`     | `Optional[bool]`       | `None`  | Stop on fader down     |
| `ignore_swap`         | `Optional[bool]`       | `None`  | Ignore swap            |
| `swap_always`         | `Optional[bool]`       | `None`  | Always swap            |
| `ms_fadein`           | `Optional[int]`        | `None`  | Fade in time (ms)      |
| `ms_crossfade`        | `Optional[int]`        | `None`  | Crossfade time (ms)    |
| `on_page_play`        | `Optional[bool]`       | `None`  | Play on page change    |
| `xct_color`           | `Optional[List[int]]`  | `None`  | Executor colors        |
| `cuelist`             | `Optional[int]`        | `None`  | Reference to cuelist   |
| `xct_push_mode`       | `Optional[List[bool]]` | `None`  | Executor push modes    |
| `docked`              | `Optional[bool]`       | `None`  | Docked status          |
| `used_in_alarm`       | `Optional[bool]`       | `None`  | Used in alarm          |
| `xct_cuelist`         | `Optional[List[int]]`  | `None`  | Executor cuelists      |
| `page`                | `Optional[int]`        | `None`  | Page number            |
| `ignore_grand_master` | `Optional[bool]`       | `None`  | Ignore grand master    |
| `xct_swap`            | `Optional[List[bool]]` | `None`  | Executor swap settings |

**Properties:**

- `combined_id`: Returns `f"{page}.{index}"` for unique identification

---

## FX

**File:** `fx.py`  
**Type:** Regular class

| Attribute        | Type            | Default | Description       |
| ---------------- | --------------- | ------- | ----------------- |
| `cyclos`         | `int`           | `None`  | Number of cycles  |
| `direction`      | `int`           | `None`  | FX direction      |
| `speed`          | `int`           | `None`  | FX speed          |
| `group_steps`    | `int`           | `None`  | Group steps       |
| `size`           | `int`           | `None`  | FX size           |
| `layers`         | `List[FXLayer]` | `None`  | FX layers         |
| `patches`        | `List[int]`     | `None`  | Patch references  |
| `speed_in_bpm`   | `bool`          | `None`  | Speed in BPM      |
| `width`          | `int`           | `None`  | FX width          |
| `spread`         | `int`           | `None`  | FX spread         |
| `basic`          | `bool`          | `None`  | Basic mode        |
| `gfxid`          | `int`           | `None`  | Graphics ID       |
| `internal_speed` | `int`           | `None`  | Internal speed    |
| `fx_ref`         | `int`           | `None`  | FX reference      |
| `splits`         | `int`           | `None`  | Number of splits  |
| `groups`         | `List[int]`     | `None`  | Group references  |
| `rect_width`     | `int`           | `None`  | Rectangle width   |
| `name`           | `str`           | `None`  | FX name           |
| `phase_offset`   | `int`           | `None`  | Phase offset      |
| `bpm`            | `int`           | `None`  | BPM value         |
| `render_id`      | `int`           | `None`  | Render ID         |
| `mode`           | `int`           | `None`  | FX mode           |
| `repeats`        | `int`           | `None`  | Number of repeats |
| `rect_height`    | `int`           | `None`  | Rectangle height  |

---

## FXLayer

**File:** `fx.py`  
**Type:** Regular class

| Attribute      | Type                | Default | Description   |
| -------------- | ------------------- | ------- | ------------- |
| `blind`        | `bool`              | `None`  | Blind mode    |
| `phase_offset` | `int`               | `None`  | Phase offset  |
| `section`      | `int`               | `None`  | Section ID    |
| `curve`        | `int`               | `None`  | Curve type    |
| `steps`        | `List[FXLayerStep]` | `None`  | Layer steps   |
| `ftypes`       | `List[int]`         | `None`  | Feature types |
| `id`           | `int`               | `None`  | Layer ID      |
| `size`         | `int`               | `None`  | Layer size    |

---

## FXLayerStep

**File:** `fx.py`  
**Type:** Regular class

| Attribute       | Type  | Default | Description     |
| --------------- | ----- | ------- | --------------- |
| `start_limit`   | `int` | `None`  | Start limit     |
| `palette_type`  | `int` | `None`  | Palette type    |
| `name`          | `str` | `None`  | Step name       |
| `ancho`         | `int` | `None`  | Width value     |
| `curve_in`      | `int` | `None`  | Curve in        |
| `curve_out`     | `int` | `None`  | Curve out       |
| `strength`      | `int` | `None`  | Step strength   |
| `curve_type`    | `int` | `None`  | Curve type      |
| `palette_value` | `Any` | `None`  | Palette value   |
| `inicio`        | `int` | `None`  | Start value     |
| `end_limit`     | `int` | `None`  | End limit       |
| `jumps`         | `int` | `None`  | Number of jumps |

---

## FXPalette

**File:** `fx.py`  
**Type:** Regular class

| Attribute      | Type                                    | Default | Description                      |
| -------------- | --------------------------------------- | ------- | -------------------------------- |
| `fx_palette`   | `Optional[int]`                         | `None`  | FX palette ID                    |
| `cue_id`       | `Optional[int]`                         | `None`  | Cue ID reference                 |
| `description`  | `Optional[str]`                         | `None`  | Palette description              |
| `visual_id`    | `Optional[int]`                         | `None`  | Visual grid position             |
| `fxs`          | `Optional[List[FX]]`                    | `None`  | List of FX objects               |
| `fxs_channels` | `Optional[List[List[Union[int, str]]]]` | `None`  | FX channel configurations        |
| `orders`       | `Optional[dict[int, dict[int, Order]]]` | `None`  | Nested orders by patch and ftype |
| `actions`      | `Optional[List[Action]]`                | `None`  | List of actions                  |
| `name`         | `Optional[str]`                         | `None`  | Palette name                     |

---

## Config

**File:** `general.py`  
**Type:** Regular class

| Attribute                  | Type             | Default | Description               |
| -------------------------- | ---------------- | ------- | ------------------------- |
| `update_mode`              | `Optional[int]`  | `None`  | Update mode setting       |
| `executors_exclusive_mode` | `Optional[bool]` | `None`  | Executor exclusive mode   |
| `remove_non_empty_cuelist` | `Optional[bool]` | `None`  | Remove non-empty cuelists |
| `clear_ltp`                | `Optional[bool]` | `None`  | Clear LTP setting         |
| `bpm_mode`                 | `Optional[bool]` | `None`  | BPM mode enabled          |
| `show_password`            | `Optional[str]`  | `None`  | Show password             |
| `show_password_enabled`    | `Optional[bool]` | `None`  | Show password enabled     |

---

## General

**File:** `general.py`  
**Type:** Regular class

| Attribute | Type               | Default | Description            |
| --------- | ------------------ | ------- | ---------------------- |
| `config`  | `Optional[Config]` | `None`  | Configuration settings |

---

## Action

**File:** `action.py`  
**Type:** Regular class

**Note:** This class is not implemented yet and serves as a placeholder.

---

## Lightshow

**File:** `lightshow.py`  
**Type:** Regular class (Main container)

| Attribute        | Type                     | Default           | Description              |
| ---------------- | ------------------------ | ----------------- | ------------------------ |
| `_parsed_date`   | `str`                    | Current timestamp | When the show was parsed |
| `_fileinfo`      | `FileInfo`               | `None`            | File information         |
| `_models`        | `Dict[int, Model]`       | `None`            | Model definitions        |
| `_patches`       | `Dict[int, Patch]`       | `None`            | Patch configurations     |
| `_groups`        | `Dict[int, Group]`       | `None`            | Group definitions        |
| `_user_palettes` | `Dict[int, UserPalette]` | `None`            | User palettes            |
| `_cues`          | `Dict[int, Cue]`         | `None`            | Cue definitions          |
| `_cuelists`      | `Dict[int, Cuelist]`     | `None`            | Cuelist definitions      |
| `_playbacks`     | `Dict[str, Playback]`    | `None`            | Playback configurations  |
| `_fxpalettes`    | `Dict[int, FXPalette]`   | `None`            | FX palettes              |
| `_general`       | `General`                | `None`            | General settings         |

**Key Methods:**

- `add_new_group()`: Add a new group
- `update_group()`: Update existing group
- `delete_group()`: Delete a group
- `copy_group()`: Copy a group
- `move_groups()`: Move groups to new positions
- `move_patches()`: Move patches to new positions
- `update_palette_orders()`: Update palette orders
- `add_new_palette()`: Add a new palette
- `delete_palette()`: Delete a palette
- `to_dict()`: Convert to dictionary
- `from_dict()`: Create from dictionary
- `to_bytes()`: Serialize to bytes
- `save_lightshow()`: Save to .lshw file
- `save_summary()`: Save text summary
- `summarise()`: Generate text summary

---

## Relationships and Hierarchies

### Primary Containers

- **Lightshow**: Root container for all other objects
- **FileInfo**: Contains Version information
- **General**: Contains Config information

### Model Hierarchy

- **Model**: Contains ModelPalette, ModelHardware, Macro, ModelValue
- **Macro**: Contains MacroStep
- **ModelValue**: Contains ModelValueStep

### Patch and Groups

- **Patch**: References Model via model_id
- **Group**: Contains list of Patch IDs

### Palettes and Cues

- **UserPalette**: Contains Orders
- **Cue**: Contains FX objects, Orders, and Actions
- **FXPalette**: Similar structure to Cue

### FX System

- **FX**: Contains FXLayer objects
- **FXLayer**: Contains FXLayerStep objects

### Playback System

- **Cuelist**: Contains CuelistElement objects
- **CuelistElement**: References Cue via cue_id
- **Playback**: References Cuelist via cuelist

### Cross-References

- Most objects use integer IDs for cross-referencing
- Playback uses combined "page.index" string IDs
- Orders link patches to palettes via patch_id and palette_id
- Groups reference patches via patched_elements_ids list

---

## Implementation Notes

1. **from_dict Methods**: All classes implement `from_dict` classmethods for deserialization
2. **to_dict Methods**: All classes implement `to_dict` methods for serialization
3. **to_bytes Methods**: Most classes implement `to_bytes` for binary serialization
4. **Validation**: Some classes include validation logic (e.g., Group, Order)
5. **Default Values**: Many attributes have sensible defaults, especially timing values
6. **Type Safety**: Extensive use of Optional types and type hints throughout
