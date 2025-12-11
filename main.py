#!/usr/bin/env python3

"""
Device Information CLI Tool
===========================

Collects system information (timestamps, device name, OS version, FQDN, IP address, disk usage)
and exports it to JSON, JSONL, or XML formats. Supports debug mode and continuous monitoring for disk free/used.
Created for the final project of Data Analysis with Python (CIS173) at Los Angeles Pierce College.

Author
------
Serah Camacho

License
-------
BSD-3-Clause (see LICENSE file for details)

Version
-------
1.2.1

Usage
-----
Run the program from the command line with the desired options:

    python main.py -f json -o info.json
    python main.py -f xml -o info.xml
    python main.py -c -o metrics.jsonl
    python main.py --debug

Examples
--------
Export basic device info to JSON:

    python main.py -f json -o device.json

Enable continuous monitoring and log to JSONL:

    python main.py -c -o monitor.jsonl
"""

# Setup --------------------------------------------------------------


import argparse
import json
import platform
import shutil
import socket
import sys
import time



VERSION = "1.2.1"

# Args --------------------------------------------------------------


def get_args():
    """
    Parse command-line arguments for the device information CLI tool.

    This function sets up the argument parser, defines supported flags and options,
    and applies post-processing logic to normalize format and output behavior.
    It supports JSON, JSONL, and XML formats, debug mode, continuous monitoring,
    and optional extended device information.

    Returns
    -------
    argparse.Namespace
        Parsed and post-processed command-line arguments.

    Examples
    --------
    >>> args = get_args()
    >>> print(args.format)
    'json'
    >>> print(args.output)
    'device_info.json'
    """

    parser = argparse.ArgumentParser(
        description="Collects system information (timestamps, device name, OS version, FQDN, IP address, disk usage) and exports it to JSON, JSONL, or XML formats. Supports debug mode and continuous monitoring for disk free/used." \
        "\n Created for the final project of Data Analysis with Python (CIS173) at Los Angeles Pierce College."
    )

    # Arguments
    parser.add_argument(
        "-f", "--format",
        type=str.lower,
        help="Output format (e.g., json, xml). Default is json.",
        action="store",
        choices=["jsonl","json","xml"],
        default="json"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        action="store",
        help="Where to output the data. By default prints to console.",
        default=None
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        help="Show program's version number and exit.",
        version= VERSION
    )


    parser.add_argument(
        "-x", "--extra",
        help="Extra information to include in the output.",
        action="store_true",
        default=False
    )

    xgroup = parser.add_mutually_exclusive_group()
    xgroup.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Outputs debug info to debug_output.json.",
        default=False
    )
    xgroup.add_argument(
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
    #FIXME: #2 add variable timing to continuous data collection.
    """
    Reads disk stats and time.

    This function runs a check every 5 seconds and logs disk usage.
    On the first run, full extended device info is written. On subsequent runs,
    only disk metrics are appended.

    Parameters
    ----------
    args : obj
        Arguments post-processed, to be passed to other funcs.

    Returns
    -------
    None

    Raises
    ------
    KeyboardInterrupt
        Raised when the user presses Ctrl+C to terminate monitoring.

    Examples
    --------
    >>> continuous_monitoring(args)
    """

    first_run = True
    while True:
        try:
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
            print("Monitoring... (Press Ctrl+C to stop)")
            time.sleep(5)  # Sleep for 5 seconds before next update
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break
        except OSError as e:
            print(f"Disk access error: {e}")
            break



def debug_mode(args):
    """
    Prints the args and version of the program for debug purposes.

    Parameters
    ----------
    args : obj
        Arguments post-processed, to be passed to other funcs.

    Returns
    -------
    None

    Examples
    --------
    >>> debug_mode(args)
    Debug mode is enabled.
    Arguments: Namespace(format='json', output=None, extra=False, debug=True, continuous=False, positional_output=None)
    Format: json
    Output file: None
    Continuous monitoring: False
    Version: RC2-1.2.0
    Data exported to debug_output.json successfully.
    """

    print("Debug mode is enabled.")
    print(f"Arguments: {args}")
    print(f"Format: {args.format}")
    print(f"Output file: {args.output}")
    print(f"Continuous monitoring: {args.continuous}")
    print(f"Version: {VERSION}")

def get_device_info():
    """
    Collect basic device information.

    This function gets device info including  timestamps, device name, OS version, FQDN, and IP address. Attempts to resolve the device's hostname to an IP address. If resolution fails
    or returns a loopback address, it falls back to 127.0.0.1.

    Returns
    -------
    dict
        Dictionary with timestamps, device name, OS version, FQDN, and IP address.

    Examples
    --------
    >>> info = get_device_info()
    >>> print(info["device_name"])
    DESKTOP-12345    
    """
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        # If resolution gives loopback, fallback to 127.0.0.1 explicitly
        if ip_address.startswith("127."):
            ip_address = "127.0.0.1"
    except Exception:
        ip_address = "127.0.0.1"

    device_info = {
        "timestamp_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "device_name": platform.node(),
        "os_version": f"{platform.system()} {platform.release()} {platform.version()}",
        "FQDN": socket.getfqdn(),
        "ip_address": ip_address
    }
    return device_info


def get_device_info_extended():
    """
    Collect extended device information.

    This function calls `get_device_info()` and adds the folwing: disk usage statistics,
    machine architecture, processor details, and the Python version.

    Returns
    -------
    dict
        Dictionary with basic device info (timestamps, device name, OS version, FQDN, IP address)
        as well as disk usage, machine type, processor, and Python version.

    Examples
    --------
    >>> info = get_device_info_extended()
    >>> print(info["processor"])
    Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz
    """

    device_info = get_device_info()
    device_info.update(get_disk_usage(device_info["os_version"]))
    device_info.update({

        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()

    })
    return device_info

def get_disk_usage(os):
    """
    Get disk usage statistics for the system.

    This function checks the operating system string and selects the appropriate
    root path for disk usage. On Windows, it uses the C:\\ drive. On other systems,
    it uses the root directory (/).

    Parameters
    ----------
    os : str
        Operating system version string used to determine which root path to query.

    Returns
    -------
    dict
        Dictionary containing total, used, and free disk space in bytes.

    Examples
    --------
    >>> usage = get_disk_usage("Windows 10")
    >>> print(usage["free_disk_space"])
    1234567890
    """

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
    """
    Export device information to a JSON file.

    Parameters
    ----------
    data : dict
        Device information dictionary to be written.
    output_file : str
        Path to the output file.
    mode : str
        File mode.

    Returns
    -------
    None

    Examples
    --------
    >>> export_to_json({"device_name": "DESKTOP-12345"}, "info.json", "w")
    Data exported to info.json successfully.
    """

    try:
        with open(output_file, mode, encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data exported to {output_file} successfully.")
    except OSError as e:
        print(f"Error writing {output_file}: {e}")



def export_to_jsonl(data, output_file, mode='a'):
    """
    Export device information to a JSON Lines (JSONL) file.

    JSONL is a format that is ingested by many data analysis products, hence it's inclusion.

    Parameters
    ----------
    data : dict
        Device information dictionary to be written.
    output_file : str
        Path to the output file.
    mode : str, optional
        File mode, default is 'a' (append).

    Returns
    -------
    None

    Examples
    --------
    >>> export_to_jsonl({"device_name": "DESKTOP-12345"}, "info.jsonl")
    Appended entry to info.jsonl
    """

    if output_file:
        try:
            with open(output_file, mode, encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
            print(f"Appended entry to {output_file}")
        except Exception as e:
            print(f"Failed to export data: {e}")
    else:
        print(json.dumps(data))

def export_to_xml(data, output_file, mode):
    """
    Export device information to an XML file.

    Parameters
    ----------
    data : dict
        Device information dictionary to be written.
    output_file : str
        Path to the output file.
    mode : str
        File mode.

    Returns
    -------
    None

    Examples
    --------
    >>> export_to_xml({"device_name": "DESKTOP-12345"}, "info.xml", "w")
    Data exported to info.xml successfully.
    """

    try:
        with open(output_file, mode, encoding="utf-8") as xml_file:
            xml_file.write('<device_info>\n')
            for key, value in data.items():
                xml_file.write(f'    <{key}>{value}</{key}>\n')
            xml_file.write('</device_info>\n')
        print(f"Data exported to {output_file} successfully.")
    except Exception as e:
        print(f"Failed to export data to {output_file}: {e}")



def output_to_file(args, device_info, mode='w'):
    """
    Dispatch device information to the appropriate export function.

    This function checks the requested output format and either writes the data
    to a file or prints it to the console. Supported formats are JSON, XML, and JSONL.
    Includes a fallback for graceful handling just in case args.format gets modified somewhere.

    Parameters
    ----------
    args : obj
        Parsed command-line arguments including format and output file path.
    device_info : dict
        Device information dictionary to be exported.
    mode : str, optional
        File mode, default is 'w'.

    Returns
    -------
    None

    Examples
    --------
    >>> output_to_file(args, {"device_name": "DESKTOP-12345"})
    {
        "device_name": "DESKTOP-12345"
    }
    """

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
            export_to_jsonl(device_info, args.output, mode)
    else:
        # fallback, should never execute!
        print(f"Unsupported format: {args.format}. Supported formats are 'json', 'jsonl', and 'xml'.")



# Main function ------------------------------------------------------------


def main():
    """
    Main entry point of the program.

    Parses command-line arguments, collects device information, and dispatches
    output based on the selected mode (debug, extra info, continuous monitoring, or single run).

    Returns
    -------
    None
    """

    args = get_args()

    if args.debug:
        debug_mode(args)
        args.output = "debug_output.json"
        args.format = "json"

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
        sys.exit(f"\nAn error occurred of type: {e}")
