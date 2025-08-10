import argparse
import logging
import os
import sys
import orjson
from pathlib import Path

from lightshark_parser.classes import Lightshow
from lightshark_parser.parsers.section_parsers import *
from lightshark_parser.utils.custom_errors import MarkerNotFoundError
from lightshark_parser.parsers.file_parser import parse_file_bytes
from lightshark_parser.utils.logger import logger


def print_dash_line():
    try:
        logger.info("-" * (os.get_terminal_size().columns - 5))
    except:
        logger.info("-" * 80)




def setup_logging(verbosity=0):
    """
    0=WARNING (only outputs end result and any warnings/errors)
    1=INFO (logs when objects are found)
    2=DEBUG (logs when attributes and objects are found)
    """
    log_level = logging.WARNING
    if verbosity == 1:
        log_level = logging.INFO
    elif verbosity >= 2:
        log_level = logging.DEBUG

    # Create named logger for the library
    logger = logging.getLogger('lightshark_parser')
    logger.setLevel(log_level)
    
    # Prevent propagation to root logger to avoid double logging
    logger.propagate = False
    
    # Only add handler if none exists (prevents duplicate handlers)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter("%(levelname)s:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        # Update existing handler level
        for handler in logger.handlers:
            handler.setLevel(log_level)
    
    # Configure root logger only for other libraries/modules that might use it
    logging.basicConfig(level=log_level, format="%(levelname)s:%(message)s", stream=sys.stderr)
    
    return logger


def main():
    parser = argparse.ArgumentParser(description="Process LightShark show files (.lshw)")

    # Main actions (parse/summmarise)
    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument("-p", "--parse", action="store_true", help="Parse show file to JSON format")
    action_group.add_argument("-s", "--summarise", action="store_true", help="Generate a summary of the show file")

    # Common arguments
    parser.add_argument("input_file", nargs="?", help="Path to the .lshw file to process")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -v for basic info, -vv for detailed debug)",
    )
    parser.add_argument("-o", "--output", metavar="output_file", help="Output file path. If not specified, defaults to <input_file>.json or <input_file>_summary.txt")

    # If no arguments or action specified, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not (args.parse or args.summarise) or not args.input_file:
        parser.print_help()
        sys.exit(0)

    setup_logging(args.verbose)

    try:
        if args.parse:
            output_file = args.output or f"{os.path.splitext(args.input_file)[0]}.json"
            with open(args.input_file, "rb") as f:
                file_bytes = f.read()
            lightshow = parse_file_bytes(file_bytes, filepath=args.input_file, output_file=output_file)

            if not args.output and not args.verbose:
                print(f"No output file specified. Output saved to: {output_file}")
            else:
                print(f"Output saved to: {output_file}")

        elif args.summarise:
            output_file = args.output or f"{os.path.splitext(args.input_file)[0]}_summary.txt"
            with open(args.input_file, "rb") as f:
                file_bytes = f.read()
            lightshow = parse_file_bytes(file_bytes, filepath=args.input_file)  # Parse but don't output JSON
            summary = lightshow.summarise()

            # Write summary to file
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(summary)
                if not args.output and not args.verbose:
                    print(f"No output file specified. Summary saved to: {output_file}")
                else:
                    print(f"Summary saved to: {output_file}")
            except Exception as e:
                logger.error("Error saving summary to %s: %s", output_file, str(e))
                sys.exit(1)

    except Exception as e:
        logger.error("Error processing file: %s", str(e), exc_info=args.verbose > 0)
        sys.exit(1)


if __name__ == "__main__":
    main()
