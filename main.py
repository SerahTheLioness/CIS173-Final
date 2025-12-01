#!/usr/bin/env python3
"""
Program designed to get information about a device via CLI and export it to a JSON file.
Author: Serah Camacho
License: BSD-3-Clause (see LICENSE file for details)
Version: 1.0.0-dev
Usage: python main.py ### Add usage instructions here later ###
"""

# Setup --------------------------------------------------------------


import argparse
import json
import platform
import socket
import sys


VERSION = "1.0.0-dev"

# Defs --------------------------------------------------------------


def get_args():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Program to get information about a device via CLI and export it to a JSON file." \
        "\n Created for the final project of Data Analysis with Python (CIS173) at Los Angeles Pierce College."
    )

    # Add arguments
    parser.add_argument(
        "-f", "--format",
        type=str,
        help="Output format (e.g., json, xml). Default is json.",
        action="store",
        default="json"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        action="store",
        help="Where to output the data (e.g., filename or directory). By default prints to console.",
        default=None
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        help="Show program's version number and exit.",
        version= VERSION
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode."
    )
    parser.add_argument(
        "positional_output",
        nargs="?",
        help="Positional argument for output file (alternative to -o/--output).",
        default=None
    )
    
    # Parse arguments   
    args = parser.parse_args()
    if args.positional_output and not args.output:
        args.output = args.positional_output.strip()
    if args.format is not None:
        args.format = args.format.lower()
    return args

def debug_mode(args):
    print("Debug mode is enabled.")
    print(f"Arguments: {args}")
    print(f"Format: {args.format}")
    print(f"Output file: {args.output}")
    print(f"Version: {VERSION}")

def get_device_info():
    # gets basic device information
    device_info = {
        "device_name": platform.node(),
        "os_version": platform.system() + " " + platform.release() + " " + platform.version(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }
    return device_info

def export_to_json(data, output_file):
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data exported to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to export data to {output_file}: {e}")

def export_to_xml(data, output_file):
    try:
        with open(output_file, 'w') as xml_file:
            xml_file.write('<device_info>\n')
            for key, value in data.items():
                xml_file.write(f'    <{key}>{value}</{key}>\n')
            xml_file.write('</device_info>\n')
        print(f"Data exported to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to export data to {output_file}: {e}")

# Main function --------------------------------------------------------------


def main():
    args = get_args()

    if args.debug:
        debug_mode(args)

    """if args.quiet:
        print("Quiet mode is enabled. Suppressing output.")
    else:
        print("Collecting data...")
        """
    device_info = get_device_info()
    if args.format == "json":
        if args.output:
            export_to_json(device_info, args.output)
        else:
            print(json.dumps(device_info, indent=4))
    elif args.format == "xml":
        if args.output:
            export_to_xml(device_info, args.output)
        else:
            print("XML output to console is not supported.")
    else:
        print(f"Unsupported format: {args.format}. Supported formats are 'json' and 'xml'.")

# Run and Handle Exceptions --------------------------------------------------------------


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(f"\nProgram interrupted by user: {e}")
    except Exception as e:
        sys.exit(f"\nAn error occurred: {e}")