import paramiko
import subprocess
import os
import datetime

# Variables
DATE = datetime.datetime.now().strftime("%Y%m%d")
IP_LIST_FILE = "/root/enc-pass/ip-list.txt"
REPORT_DIR = "/root/enc-pass/reports"
TEMP_DIR = f"{REPORT_DIR}/temp"
REPORT_FILE = f"{REPORT_DIR}/{DATE}-system-report.html"
RECIPIENT = "tarun.brari@vmipl.in"
SUBJECT = f"System Information Report of Revamp BMG servers for {DATE}"
ALERT_RECIPIENT = "alert@example.com"
ALERT_SUBJECT = f"Alert: /home Partition Breached 90% Usage on {DATE}"

# Ensure directories exist
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to execute SSH command
def run_ssh_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode().strip() or "N/A"

# Function to collect system data
def collect_data(ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username="root", timeout=5)

        hostname = run_ssh_command(client, "hostname")
        uptime = run_ssh_command(client, "uptime | awk '{print $3, $4}' | tr -d ','")
        ram_available = run_ssh_command(client, "free -h | awk '/Mem:/ {print $7}'")
        var_usage = run_ssh_command(client, "df -h /var/log | awk 'NR==2 {print $5}'")
        home_usage = run_ssh_command(client, "df -h /home | awk 'NR==2 {print $5}' | tr -d '%'")

        client.close()
        
        # Send alert if /home usage exceeds 90%
        if home_usage.isdigit() and int(home_usage) > 90:
            subprocess.run(["mail", "-s", ALERT_SUBJECT, ALERT_RECIPIENT], input=f"ALERT: /home partition on {ip} exceeded 90% usage ({home_usage}%)".encode())

        return hostname, ip, uptime, ram_available, var_usage, home_usage
    except Exception as e:
        return f"FAILED-{ip}", ip, "N/A", "N/A", "N/A", "N/A"

# Read IPs
with open(IP_LIST_FILE) as f:
    clients = [line.strip() for line in f if line.strip()]

# Collect data
report_data = [collect_data(ip) for ip in clients]

# Generate HTML report
with open(REPORT_FILE, "w") as f:
    f.write("<html><body>")
    f.write("<h1>System Information Report</h1>")
    f.write("<table border='1'>")
    f.write("<tr><th>S.No</th><th>Hostname</th><th>IP</th><th>Uptime</th><th>RAM Available</th><th>/var/log Usage (%)</th><th>/home Usage (%)</th></tr>")
    
    for idx, (hostname, ip, uptime, ram, var_usage, home_usage) in enumerate(report_data, 1):
        f.write(f"<tr><td>{idx}</td><td>{hostname}</td><td>{ip}</td><td>{uptime}</td><td>{ram}</td><td>{var_usage}</td><td>{home_usage}</td></tr>")
    
    f.write("</table>")
    f.write("</body></html>")

# Send email report using Mutt
subprocess.run(["mutt", "-e", "set content_type=text/html", "-s", SUBJECT, RECIPIENT], input=open(REPORT_FILE, "rb").read())

