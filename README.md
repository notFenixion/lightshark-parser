# lightshark-parser

lightshark-parser is a Python library for parsing show files used in the [Lightshark](https://lightshark.es/) software (`.lshw`).

## Installation

You can install lightshark-parser using pip:

```bash
pip install lightshark-parser
```


## Features

### Parsing .lshw files

Extracts details from .lshw files into a `Lightshow` object. Also supports :
- Serialising the `Lightshow` object into a .json file
- Summarising important show details into a .txt file

Currently, the following details are extracted:
- Fixture models
- Patched fixtures
- Groups
- Palettes
- Cues
- Cuelists
- Playbacks
- FXs
- Some settings


### Edit without a Lightboard!

Lightshark Parser comes with a set of functions that allow you to edit the show's attributes through code without needing to use the lightboard directly, serving as a sort of offline editor.

Can also be used to create your own custom "macros".

After editing, you can use the `to_bytes()` method to write it back into a .lshw file, following a similar format to the one used by Lightshark.

#### Disclaimers:
- This is not official in any capacity. I reverse-engineered this based off a bunch of files I had, so it is nowhere near 100% accurate to how Lightshark formats their files.
- Some details of the show are currently not supported. The current ones implemented are the most commonly used, so it should work for most purposes.





## Usage

Lightshark Parser can be used both from the command line and using Python code.

### Command line

```bash
lightshark-parser -p/s <input_file> -o <output_file>
```

- `-p` : Parse file
- `-s` : Summarise file

If no output file is provided, output_file will default to `<input_path>.json` or `<input_path>_summarised.txt` depending on the operation selected.

### Code

```python
from lightshark_parser import Lightshow, parse_file_bytes



```

