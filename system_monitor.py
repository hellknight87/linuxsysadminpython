import psutil
import socket

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def get_hostname():
    return socket.gethostname()

def get_all_ip_addresses():
    ip_addresses = {}
    for interface, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET: # For ipv4 addresses only
                ip_addresses[interface] = addr.address
    return ip_addresses

if __name__ == "__main__":
    print(f"Hostname: {get_hostname()}")
    print("IP Addresses:")
    for interface, ip in get_all_ip_addresses().items():
        print(f"  {interface}: {ip}")

    print(f"CPU Usage: {get_cpu_usage()}%")
    print(f"Memory Usage: {get_memory_usage()}%")
    print(f"Disk Usage: {get_disk_usage()}%")