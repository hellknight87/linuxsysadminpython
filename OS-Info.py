import platform

os_info = {
    "OS Name": platform.system(),
    "OS Version": platform.release(),
    "Full Version": platform.version(),
    "Architecture": platform.architecture()[0],
    "Kernel": platform.uname().release
}

for key, value in os_info.items():
    print(f"{key}: {value}")