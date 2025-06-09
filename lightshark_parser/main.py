import argparse
import logging
import sys
from .parsers import read_file_bytes, parse_file_bytes
from .utils.json_encoder import CompactJSONEncoder

def main():
    parser = argparse.ArgumentParser(description='Read and parse .lshw files')
    parser.add_argument('file', nargs='?', help='Path to the .lshw file to be parsed')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-o', '--output', help='Output JSON file to save the parsed data')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    file_bytes = read_file_bytes(args.file)
    logging.debug(f"Successfully read {len(file_bytes)} bytes from {args.file}")

    lightshow = parse_file_bytes(file_bytes)
    print("Successfully parsed file!")
    
    if args.output:
        try:
            data = lightshow.to_dict()
            json_str = CompactJSONEncoder(indent=2, ensure_ascii=False).encode(data)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            print(f"Successfully saved to {args.output}")
        except Exception as e:
            print(f"Error saving to {args.output}: {e}", file=sys.stderr)