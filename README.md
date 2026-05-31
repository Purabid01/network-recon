# Network Suite Utilities

A lightweight, zero-dependency suite of production-ready Python utilities designed to discover local networking telemetry and perform concurrent network reconnaissance.

## Features

### 1. Network Mapper Utility
* **Automated Interface Discovery:** Parses the system `ip addr` subsystem to extract active IPv4 addresses while automatically dropping subnet masks and filtering out IPv6 loops.
* **Upstream Routing Detection:** Dynamically queries the kernel routing table via `ip route` to locate the active default gateway interface.
* **Defensive DNS Parsing:** Gracefully parses local name resolution endpoints from `/etc/resolv.conf` with explicit safeguards handling empty lines, edge configurations, and missing files.
* **Structured Telemetry Aggregation:** Compiles unstructured command-line text output into a standardized, reusable JSON data layer and writes it cleanly to disk.

### 2. Concurrent Port Scanner
* **Multi-Threaded Performance:** Leverages a `ThreadPoolExecutor` to scan multiple ports simultaneously, preventing network I/O blockages from slowing down execution times.
* **Functional Data Separation:** Decouples core socket checking logic from presentation layers by passing structured lists of dictionaries back to the calling scope.
* **Defensive Error Handling:** Utilizes explicit timeouts (`sock.settimeout(1.0)`) and safety catch blocks to ensure firewalled or dropped packets do not cause system hangs.

---

## How It Works

### Utility 1: Network Mapper Core Architecture
The script operates through a sequence of internal discovery stages:

```text
[Linux Kernel Subsystems]
│
├──► ip addr   ──► get_interfaces() ──┐
├──► ip route  ──► get_gateway()    ──┼─► get_network_info() ─► save_file_data() ─► network_info.json
└──► resolv.conf ─► get_dns()        ──┘

```

1. **`get_interfaces()`**: Invokes `ip addr` via a subprocess, checks for matching IPv4 lines (`inet`), strips the CIDR network masks (e.g., `/20`), and aggregates the raw IPs into a clean array.
2. **`get_gateway()`**: Scans the kernel routing table via `ip route` to locate the explicit `default via` target boundary.
3. **`get_dns()`**: Safely accesses `/etc/resolv.conf` inside a `try/except` safety block to pull configured system `nameserver` IPs.
4. **`save_file_data()`**: Bundles the individual components into a single dictionary array and uses `json.dump()` to write it directly to a flat file.

### Utility 2: Concurrent Port Scanner Mechanics

Instead of evaluating ports sequentially, the scanner uses an optimized worker pool mapping pattern to scan the entire target footprint concurrently.

```text
[COMMON_PORTS] ──► ThreadPoolExecutor(max_workers=10) 
                         ├── Worker 1 ──► Scan Port 22  ──┐
                         ├── Worker 2 ──► Scan Port 80  ──┼──► Unpack Tuple Iterator ──► Output Results
                         └── Worker N ──► Scan Port 443 ──┘

```

---

## Reference Matrix: Targeted Network Ports

The concurrent scanner isolates its reconnaissance payload against the following common system endpoints. Here is why these dedicated boundaries are targeted:

| Port | Service | Why it needs that port |
| --- | --- | --- |
| **22** | SSH | It needs a secure, encrypted line to let developers log into a remote server's terminal from home without exposing command strings to the open internet. |
| **80** | HTTP | This is the legacy, unencrypted baseline gateway for web traffic. It handles raw HTML, CSS, and JS data transfers when security certificates aren't present. |
| **443** | HTTPS | The modern evolution of port 80. It wraps web traffic inside an SSL/TLS encryption layer, ensuring passwords, credit cards, and sessions can't be sniffed in transit. |
| **3306** | MySQL | A dedicated highway for relational database communication. Applications need a stable, isolated port to send complex SQL queries and pull back data tables. |
| **5432** | PostgreSQL | Similar to MySQL, this port isolates traffic for enterprise relational database transactions, ensuring Postgres engine requests don't collide with other system processes. |
| **6379** | Redis | Because Redis operates entirely in-memory for lightning-fast caching, it needs an explicit connection endpoint to serve key-value pairs instantly without disk I/O latency. |
| **27017** | MongoDB | As a NoSQL document database, it uses this dedicated port to accept and process JSON-like binary data (BSON documents) from backend microservices. |

---

## How To Run It

### Prerequisites

* **Python Version:** Python 3.6 or higher.
* **Environment:** Linux (Ubuntu, Debian, CentOS, etc.) or Windows Subsystem for Linux (WSL).
* *Note: The Network Mapper utility relies natively on standard Linux networking binaries (`ip`) and will fail safely on native Windows CMD/PowerShell environments. The Port Scanner runs natively across all environments.*

### Execution Steps

#### Running the Network Mapper

1. Open your terminal application and execute the script directly using Python 3:

```bash
python3 network_mapper.py

```

Upon execution, the script will output a success notification indicating the payload has been saved to disk:

```text
[+] Success: Network profile saved to network_info.json

```

#### Running the Concurrent Port Scanner

1. Execute the scanner module via your terminal runner:

```bash
python3 scanner.py

```

2. Enter your desired scan target when prompted by the runtime interface:

```text
Enter target IP address to scan: 127.0.0.1

[*] Commencing concurrent scan on host: 127.0.0.1...

[-] Scan Complete. 7 CLOSED ports identified:
    -> Port 22 (SSH) is CLOSED
    -> Port 80 (HTTP) is CLOSED
    -> Port 443 (HTTPS) is CLOSED
    ...

```

---

## Understanding the Outputs

### Network Mapper Schema (`network_info.json`)

```json
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

```

* **`local_ips`**: An array of all active IPv4 interfaces running on your instance.
* `127.0.0.1`: The standard local system loopback interface (localhost).
* `172.26.72.147`: Your active local machine IP address assigned to the interface communicating with your physical network.
* `172.17.0.1`: The local gateway address reserved for internal container networking (the bridge interface used by Docker).


* **`default_gateways`**: The standard upstream router address your computer sends all outbound web or remote data to when a destination isn't local. It handles your interface's exit path to the internet.
* **`nameserver_ip`**: A list of the upstream DNS (Domain Name System) server IP addresses your computer uses to translate human-readable domain names (like google.com) into computer-routable IP strings.

```