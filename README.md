# Device Information CLI Tool

Collects system information (timestamps, device name, OS version, FQDN, IP address, disk usage) and exports it to JSON, JSONL, or XML formats. Supports debug mode and continuous monitoring for disk metrics.

*This software is licensed under the BSD 3‑Clause License.*

---

## Features
- Export device info to **JSON**, **JSONL**, or **XML**
- **Debug mode**: prints arguments and saves to debug_output.json
- **Continuous monitoring**: logs disk usage every 5 seconds until stopped
- **Extra mode**: includes processor, architecture, Python version, and disk stats

---

## Installation
Clone the repository and ensure Python 3.8+ is installed:

    git clone https://github.com/yourusername/device-info-cli.git
    cd device-info-cli

---

## Usage
Run the program from the command line with the desired options:

    python main.py -f json -o info.json
    python main.py -f xml -o info.xml
    python main.py -c -o metrics.jsonl
    python main.py --debug

### Examples
Export basic device info to JSON:

    python main.py -f json -o device.json

Enable continuous monitoring and log to JSONL:

    python main.py -c -o monitor.jsonl

---

## Roadmap / TODO
- Add more system metrics (CPU load, memory usage, network stats)
- Generate dynamic titles based on timestamp
- Polish CLI help text and examples