import dns.resolver
import sys


def resolve_domain(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        
        for rdata in answers:
            print(f"{record_type} Record: {rdata}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
# resolve_domain("netflix.com", "A")
# resolve_domain("google.com", "MX")


def full_dns_lookup(domain):
    # Step 1: Define a list of record types you want to scan
    record_types = ["A", "AAAA", "MX", "NS"]
    
    # Step 2: Loop through each record type in the list
    for current_type in record_types:
        
        # Step 3: Print the separator banner (e.g., --- A Records ---)
        print(f"\n--- {current_type} Records ---")
        
        # Step 4: Call your original function using the current domain and record type
        resolve_domain(domain, current_type)
        
# Test the full lookup
# full_dns_lookup("google.com")




if __name__ == '__main__':
    # --- Command Line Argument Logic ---
    # Check if the user forgot to type a domain name
    if len(sys.argv) < 2:
        print("Usage: python3 dns_tool.py <domain>")
        
    else:
        # 1. Grab the domain from the correct index of sys.argv
        target_domain = sys.argv[1]
        
        # 2. Call your full_dns_lookup function using that target_domain
        full_dns_lookup(target_domain)