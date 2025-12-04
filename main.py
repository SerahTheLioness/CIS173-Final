#!/usr/bin/env python3
"""
Program designed to get information about a device via CLI and export it to a JSON file.
Author: Serah Camacho
License: BSD-3-Clause (see LICENSE file for details)
Version: RC1-1.1.0
Usage: python main.py ### Add usage instructions here later ###
"""

# Setup --------------------------------------------------------------


import argparse
import json
import platform
import shutil
import socket
import sys
import time



VERSION = "RC1-1.1.0"

# Args --------------------------------------------------------------


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
        help="Enable debug mode. Forces output to debug_output.json in json format.",
        default=False
    )

    parser.add_argument(
        "-x", "--extra",
        help="Extra information to include in the output.",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "-c", "--continuous",
        help="Continuously monitor and update disk metrics at regular intervals. Forces jsonl (json lines) format.", 
        action="store_true",
        default=False
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
    if args.continuous:
        args.format = "jsonl"
    if args.format is not None:
        args.format = args.format.lower()
    return args


# Functions --------------------------------------------------------------

def continuous_monitoring(args):
    # continuous monitoring functionality
    first_run = True
    while True:
        try:
            print("Monitoring... (Press Ctrl+C to stop)")
            live_info = get_device_info_extended()
            if first_run:
                
                output_to_file(args, live_info, mode='w')
                first_run = False
            else:
                live_info = {
                    "timestamp_local": live_info["timestamp_local"],
                    "timestamp_utc": live_info["timestamp_utc"],
                    "used_disk_space": live_info["used_disk_space"],
                    "free_disk_space": live_info["free_disk_space"],
                    "total_disk_space": live_info["total_disk_space"]
                }
                output_to_file(args, live_info, mode='a')

            time.sleep(5)  # Sleep for 5 seconds before next update
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break
        



def debug_mode(args):
    print("Debug mode is enabled.")
    print(f"Arguments: {args}")
    print(f"Format: {args.format}")
    print(f"Output file: {args.output}")
    print(f"Continuous monitoring: {args.continuous}")
    print(f"Version: {VERSION}")

def get_device_info():
    # gets basic device information
    device_info = {
        "timestamp_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "device_name": platform.node(),
        "os_version": platform.system() + " " + platform.release() + " " + platform.version(),
        "ip_address": socket.gethostbyname(socket.getfqdn())
    }
    return device_info

def get_device_info_extended():
    # gets extended device information
    device_info = get_device_info()
    device_info.update(get_disk_usage(device_info["os_version"]))
    device_info.update({

        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
        
    })

    return device_info

def get_disk_usage(os):
    if "Windows" in os:
        usage = shutil.disk_usage("C:\\")
    else:
        usage = shutil.disk_usage("/")
    disk_usage = {
        "total_disk_space": usage.total,
        "used_disk_space": usage.used,
        "free_disk_space": usage.free,
    }
    return disk_usage

def export_to_json(data, output_file, mode):
    try:
        with open(output_file, mode) as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data exported to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to export data to {output_file}: {e}")

def export_to_jsonl(data, output_file, mode='a'):
    try:
        with open(output_file, mode) as f:
            f.write(json.dumps(data) + "\n")
        print(f"Appended entry to {output_file}")
    except Exception as e:
        print(f"Failed to export data: {e}")

def export_to_xml(data, output_file, mode):
    try:
        with open(output_file, mode) as xml_file:
            xml_file.write('<device_info>\n')
            for key, value in data.items():
                xml_file.write(f'    <{key}>{value}</{key}>\n')
            xml_file.write('</device_info>\n')
        print(f"Data exported to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to export data to {output_file}: {e}")

def convert_jsonl_to_json(jsonl_file, json_file):
    try:
        with open(jsonl_file, 'r') as jl_file:
            lines = jl_file.readlines()
        
        data = [json.loads(line) for line in lines]
        
        with open(json_file, 'w') as j_file:
            json.dump(data, j_file, indent=4)
        
        print(f"Converted {jsonl_file} to {json_file} successfully.")
    except Exception as e:
        print(f"Failed to convert {jsonl_file} to {json_file}: {e}")

def output_to_file(args, device_info, mode='w'):
    if args.format == "json":
        if args.output:
            export_to_json(device_info, args.output, mode)
        else:
            print(json.dumps(device_info, indent=4))
    elif args.format == "xml":
        if args.output:
            export_to_xml(device_info, args.output, mode)
        else:
            print("XML output to console is not supported.")
    elif args.format == "jsonl":
        if args.output:
            export_to_jsonl(device_info, args.output, mode)
        else:
            print("JSONL output to console is not supported.")
    else:
        print(f"Unsupported format: {args.format}. Supported formats are 'json', 'jsonl', and 'xml'.")


# Main function --------------------------------------------------------------


def main():
    args = get_args()

    if args.debug:
        debug_mode(args)
        args.output = "debug_output.jsonl"
        args.format = "jsonl"

    if args.extra:
        device_info = get_device_info_extended()
    else:
        device_info = get_device_info()

    if args.continuous:
        continuous_monitoring(args)
    else: 
        output_to_file(args, device_info)


# Run and Handle Exceptions --------------------------------------------------------------


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(f"\nProgram interrupted by user: {e}")
    except Exception as e:
        sys.exit(f"\nAn error occurred: {e}")
