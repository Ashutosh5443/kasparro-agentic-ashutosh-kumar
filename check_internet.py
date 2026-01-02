import socket
import ssl

hostname = "generativelanguage.googleapis.com"
context = ssl.create_default_context()

try:
    print(f"Attempting to resolve {hostname}...")
    ip_list = socket.getaddrinfo(hostname, 443)
    print(f"Success! Found IP: {ip_list[0][4][0]}")
    
    print("Attempting to connect...")
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print("Successfully connected to Google API servers.")
            
except socket.gaierror:
    print("ERROR: DNS Lookup Failed. Your computer cannot find Google.")
    print("Fix: Check your internet or disable your VPN.")
except Exception as e:
    print(f"ERROR: Connection failed: {e}")