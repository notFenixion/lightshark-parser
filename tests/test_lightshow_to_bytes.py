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
    output_file = f"{Path(input_file).stem}_converted.lshw"
    
    logger.info(f"Converting {input_file} to bytes...")
    
    try:
        # Parse the input file
        lightshow = parse_file_bytes(input_file)
        logger.info(f"Successfully parsed {input_file}")
        # Convert to bytes
        result = lightshow.to_bytes()
        
        # Write to output file
        with open(output_file, 'wb') as f:
            f.write(result)
            
        logger.info(f"Successfully wrote output to {output_file}")
        
        # Parse both input and output files to JSON for comparison
        logger.info("Parsing both input and output files to compare JSON outputs...")
        
        # Parse input file to dict
        input_lightshow = parse_file_bytes(input_file)
        input_dict = input_lightshow.to_dict()
        
        # Parse output file to dict
        output_lightshow = parse_file_bytes(output_file)
        output_dict = output_lightshow.to_dict()
        
        # Remove file-specific attributes that will differ
        for attr in ['_filepath', '_filename', '_parsed_date']:
            if attr in input_dict:
                del input_dict[attr]
            if attr in output_dict:
                del output_dict[attr]
        
        # Compare the dictionaries
        if input_dict == output_dict:
            logger.info("✅ JSON comparison passed: Input and output file JSON representations match!")
        else:
            # Find differences
            import json
            diff = {}
            all_keys = set(input_dict.keys()) | set(output_dict.keys())
            
            for key in all_keys:
                if key not in input_dict:
                    diff[key] = ("MISSING in input", output_dict[key])
                elif key not in output_dict:
                    diff[key] = (input_dict[key], "MISSING in output")
                elif input_dict[key] != output_dict[key]:
                    # For lists and dicts, do a deeper comparison
                    if isinstance(input_dict[key], (dict, list)) and isinstance(output_dict[key], (dict, list)):
                        if json.dumps(input_dict[key], sort_keys=True) != json.dumps(output_dict[key], sort_keys=True):
                            diff[key] = (input_dict[key], output_dict[key])
                    else:
                        diff[key] = (input_dict[key], output_dict[key])
            
            logger.error("❌ JSON comparison failed: Differences found:")
            for key, (input_val, output_val) in diff.items():
                logger.error(f"  {key}:")
                logger.error(f"    Input:  {input_val}")
                logger.error(f"    Output: {output_val}")
            
            # Write the full dicts to files for debugging
            with open('input_lightshow.json', 'w') as f:
                json.dump(input_dict, f, indent=2, default=str)
            with open('output_lightshow.json', 'w') as f:
                json.dump(output_dict, f, indent=2, default=str)
            logger.error("Full JSON dumps written to input_lightshow.json and output_lightshow.json")
            
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose >= 2)
        sys.exit(1)

if __name__ == "__main__":
    main()
