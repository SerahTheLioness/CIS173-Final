#!/usr/bin/env python3
"""
Program designed to get information about a device via CLI and export it to a JSON file.
Author: Serah Camacho
License: BSD-3-Clause (see LICENSE file for details)
Version: 1.0.0-dev
Usage: python main.py ### Add usage instructions here later ###
"""

import argparse
import json
import platform
import socket
import sys

def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Program to get information about a device via CLI and export it to a JSON file.\n Created for the final project of Data Analysis with Python (CIS173) at Los Angeles Pierce College."
    )

    # Add arguments
    parser.add_argument(
        "-f", "--format",
        type=str,
        help="Output format (e.g., json, xml). Default is json.",
        default="json"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Where to output the data (e.g., filename or directory). Default is output.json",
    )

    # Parse arguments
    args = parser.parse_args()
    print(f"Format: {args.format}")
    print(f"Output file: {args.output}")

    print("Getting device information...")
    print(get_device_info())

    # add logic to get device information (os apis? cli calls?) and export to specified format (simple, or at least should be...)

def get_device_info():
    # gets basic device information
    device_info = {
        "device_name": platform.node(),
        "os_version": platform.system() + " " + platform.release() + " " + platform.version(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }
    return device_info

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(f"\nProgram interrupted by user: {e}")
    except Exception as e:
        sys.exit(f"\nAn error occurred: {e}")