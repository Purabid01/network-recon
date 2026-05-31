import socket
from concurrent.futures import ThreadPoolExecutor


COMMON_PORTS = {
    22: 'SSH', 80: 'HTTP', 443: 'HTTPS',
    3306: 'MySQL', 5432: 'PostgreSQL',
    6379: 'Redis', 27017: 'MongoDB'
}



def scan_port(host, port):
    """
    Attempts a TCP connection to a specific port.
    Returns True if open, False if closed/timed out.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0) # Prevent hanging on firewalled ports -- # Higher timeout is safe now because we are concurrent
        result = sock.connect_ex((host, port))
        sock.close()
        # Return a clean boolean (True for open, False for closed)
        return result == 0
    except Exception:
        return False
    
    
    # ---------- For testing  ----------------------
    # # Return the string instead of printing it here
    # if result == 0:
    #     return f"Port {port} - OPEN"
        
    # else:
        # return f"Port {port} - CLOSED"
# print(scan_port("127.0.0.1", 80))
# print(scan_port("127.0.0.1", 11434))




# # ------------  BOOTSTRAP --------------------
# def scan_host(host):
#     print(f"Scanning {host} ....")
#     open_ports = []
        
#     # logic: 1 --> using key
#     # for port in COMMON_PORTS.keys():
#     #     result = scan_port(host, port)
        
#     #     if "OPEN" in result:
#     #         service_name = COMMON_PORTS[port]
#     #         open_ports.append(f"Port {port} ({service_name})")
    
    
#     #logic: 2 --> Optimization: Iterate over key-value pairs directly
#     for port, service in COMMON_PORTS.items():
#         if scan_port(host, port):
#             # Optimization: Store data cleanly as a dictionary
#             open_ports.append({
#                 "port": port,
#                 "service": service
#             })
            
#     return open_ports

# # scan_result = scan_host("172.26.64.1")

# # if scan_result:
# #     print("[+] Scan Complete. Open ports open:")
# #     for details in scan_result:
# #         print(details)
        
# # else:
# #     print("[-] Scan Complete. No open ports found on this host.")
    
    
    
def scan_host_fast(host):
    """
    Scans common ports concurrently using a ThreadPoolExecutor.
    Gathers closed ports based on the testing requirement.
    """
    print(f"\n[*] Commencing concurrent scan on host: {host}...")
    open_ports = []
    
    # Spin up a pool of worker threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all port scanning tasks to the pool immediately
        results = executor.map(lambda port: (port, scan_port(host, port)), COMMON_PORTS.keys())
        
        for port, is_open in results:
            # Tracking open ports for verification on silent local interfaces
            if is_open:
                open_ports.append({
                    "port": port,
                    "service": COMMON_PORTS[port]
                })
    
    return open_ports
    
    
    
    
if __name__ == '__main__':
    target = input("Enter target IP: ")
    fast_scan_result = scan_host_fast(target)
    
    if fast_scan_result:
        print(f"\n[-] Scan Complete. {len(fast_scan_result)} open ports identified:")
        for details in fast_scan_result:
            # Pull values out of the dictionaries cleanly
            print(f"    -> Port {details['port']} ({details['service']}) is OPEN") 
    else:
        print("\n[+] Scan Complete. No open ports found.")

