import subprocess
import json

def get_interfaces():
    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    
#     print(lines)
    
# get_interfaces()

    ip_addresses = []
    
    for line in lines:
        if "inet" in line and "inet6" not in line:
            ipv4_address = line.split()
            raw_ip = ipv4_address[1]
            # to remove the mask use second split
            subnet_split = raw_ip.split('/')
            only_ip = subnet_split[0]
            ip_addresses.append(only_ip)
    
    return ip_addresses


# print(get_interfaces())

# pass the list into json.dumps()
# json_output = json.dumps(get_interfaces(), indent=4)
# print(json_output)






#get gateway function - ip route

def get_gateway():
    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
    lines = result.stdout.split("\n")
    
    for line in lines:
        if "default via" in line:
            parts = line.split()
            
            default_gateway_ip = parts[2]
            return default_gateway_ip
      
    return None
    
# print(get_gateway())




#get dns
def get_dns():
    try:
        with open('/etc/resolv.conf', 'r') as f:
            content = f.read()
            lines = content.split("\n")
            
            nameserver_ips = []
            
            for line in lines:
                if "nameserver" in line:
                    parts = line.split()
                    # Ensure the line isn't just the word 'nameserver' with no IP
                    if len(parts) > 1:
                        nameserver_ips.append(parts[1])
                
            return nameserver_ips if nameserver_ips else None
    
    except FileNotFoundError:
        return None  
# print(get_dns())





#get network info
def get_network_info():
    network_profile = {
        "local_ips": get_interfaces(),
        "default_gateways":  get_gateway(),
        "nameserver_ip": get_dns()
    }
    return network_profile
    
# profile = get_network_info()
# print(json.dumps(profile, indent=4))





# new function to save data
def save_file_data(data, filename="network_info.json"):
    with open(filename, 'w') as file:
        # json.dump writes the dictionary directly into the open file object
        json.dump(data, file, indent=4)
    print(f"[+] Success: Network profile saved to {filename}")
    
    



# --- Execution Gatekeeper ---
if __name__ == "__main__":
    # 1. Gather all data into our dictionary
    profile = get_network_info()
    
    # 2. Print it out to the terminal screen using our string dumper
    print("--- Current Network Profile ---")
    print(json.dumps(profile, indent=4))
    
    # 3. Save it to disk using our new function
    save_file_data(profile)





    
