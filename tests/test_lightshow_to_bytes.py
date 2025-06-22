#!/usr/bin/env python3
"""
Convert Lightshow LSHW file to bytes and save to output file.
"""
import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path to import lightshark_parser
sys.path.insert(0, str(Path(__file__).parent.parent))

from lightshark_parser import parse_file_bytes

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert Lightshow LSHW file to bytes and save to output file.')
    parser.add_argument('input_file', help='Input LSHW file')
    parser.add_argument('output_file', nargs='?', help='Output LSHW file (default: <input_stem>_converted.lshw)')
    parser.add_argument('-v', '--verbose', action='count', default=0, 
                      help='Increase verbosity (use -v for INFO, -vv for DEBUG)')
    return parser.parse_args()

def setup_logging(verbosity):
    """Set up logging based on verbosity level."""
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Set root logger level as well
    logging.getLogger().setLevel(level)

def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    
    input_file = args.input_file
    output_file = args.output_file or f"{Path(input_file).stem}_converted.lshw"
    
    logger.info(f"Converting {input_file} to bytes...")
    
    try:
        # Parse the input file
        lightshow = parse_file_bytes(input_file)
        
        # Convert to bytes
        result = lightshow.to_bytes()
        
        # Write to output file
        with open(output_file, 'wb') as f:
            f.write(result)
            
        logger.info(f"Successfully wrote output to {output_file}")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose >= 2)
        sys.exit(1)

if __name__ == "__main__":
    main()
