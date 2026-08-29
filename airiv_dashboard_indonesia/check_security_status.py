import subprocess
import os

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print(">>> Checking Ubuntu Workstation Security Posture <<<")

# 1. Check UFW Firewall Status
ufw_status = run_cmd("sudo ufw status")
print(f"\n[1] UFW Firewall Status:\n{ufw_status}")

# 2. Check SSH Key-Only Authentication and Password Setting
sshd_config_path = "/etc/ssh/sshd_config"
pubkey_auth = "Unknown"
password_auth = "Unknown"

if os.path.exists(sshd_config_path):
    with open(sshd_config_path, "r") as f:
        content = f.read()
        for line in content.splitlines():
            if "PubkeyAuthentication" in line and not line.strip().startswith("#"):
                pubkey_auth = line.strip()
            if "PasswordAuthentication" in line and not line.strip().startswith("#"):
                password_auth = line.strip()

print(f"\n[2] SSH Configuration Check:")
print(f"   PubkeyAuthentication: {pubkey_auth}")
print(f"   PasswordAuthentication: {password_auth}")

# 3. Check Docker Container Socket Exposure & Active Ports
docker_ports = run_cmd("docker ps --format 'table {{.Names}}\t{{.Ports}}'")
print(f"\n[3] Docker Container Port Bindings:\n{docker_ports}")

print("\n>>> Security Verification Complete. <<<")
