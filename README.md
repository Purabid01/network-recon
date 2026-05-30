# Network Mapper Utility

A lightweight, zero-dependency Python utility designed to discover, extract, and map local networking telemetry from Linux-based systems. The script parses system network configuration subsystems to assemble a unified profile of active IPv4 addresses, upstream default gateways, and configured DNS name servers.

## Features
* **Automated Interface Discovery:** Parses the system `ip addr` subsystem to extract active IPv4 addresses while automatically dropping subnet masks and filtering out IPv6 loops.
* **Upstream Routing Detection:** Dynamically queries the kernel routing table via `ip route` to locate the active default gateway interface.
* **Defensive DNS Parsing:** Gracefully parses local name resolution endpoints from `/etc/resolv.conf` with explicit safeguards handling empty lines, edge configurations, and missing files.
* **Structured Telemetry Aggregation:** Compiles unstructured command-line text output into a standardized, reusable JSON data layer and writes it cleanly to disk.

---

## How It Works

The script operates through a sequence of internal discovery stages:
[Linux Kernel Subsystems]
│
├──► ip addr   ──► get_interfaces() ──┐
├──► ip route  ──► get_gateway()    ──┼─► get_network_info() ─► save_file_data() ─► network_info.json
└──► resolv.conf ─► get_dns()        ──┘

1.  **`get_interfaces()`**: Invokes `ip addr` via a subprocess, checks for matching IPv4 lines (`inet`), strips the CIDR network masks (e.g., `/20`), and aggregates the raw IPs into a clean array.
2.  **`get_gateway()`**: Scans the kernel routing table via `ip route` to locate the explicit `default via` target boundary.
3.  **`get_dns()`**: Safely accesses `/etc/resolv.conf` inside a `try/except` safety block to pull configured system `nameserver` IPs.
4.  **`save_file_data()`**: Bundles the individual components into a single dictionary array and uses `json.dump()` to write it directly to a flat file.

---

## How To Run It

### Prerequisites
* **Python Version:** Python 3.6 or higher.
* **Environment:** Linux (Ubuntu, Debian, CentOS, etc.) or Windows Subsystem for Linux (WSL). *Note: This script relies natively on standard Linux networking binaries (`ip`) and will fail safely on native Windows CMD/PowerShell environments.*

### Execution Steps
1. Save the script file as `network_mapper.py`.
2. Open your terminal application and execute the script directly using Python 3:

```bash
python3 network_mapper.py
Upon execution, the script will output a success notification indicating the payload has been saved to disk:

Plaintext
[+] Success: Network profile saved to network_info.json
Understanding the Output File
The script generates a file named network_info.json in the same directory where it runs. Below is an example of what the generated data schema means:

JSON
{
    "local_ips": [
        "127.0.0.1",
        "10.255.255.254",
        "172.26.72.147",
        "172.17.0.1"
    ],
    "default_gateways": "172.26.64.1",
    "nameserver_ip": [
        "172.26.64.1"
    ]
}
Element Breakdown
local_ips: An array of all active IPv4 interfaces running on your instance.

127.0.0.1: The standard local system loopback interface (localhost).

172.26.72.147: Your active local machine IP address assigned to the interface communicating with your physical network.

172.17.0.1: The local gateway address reserved for internal container networking (the bridge interface used by Docker).

default_gateways: The standard upstream router address your computer sends all outbound web or remote data to when a destination isn't local. It handles your interface's exit path to the internet.

nameserver_ip: A list of the upstream DNS (Domain Name System) server IP addresses your computer uses to translate human-readable domain names (like google.com) into computer-routable IP strings.