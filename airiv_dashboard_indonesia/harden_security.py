import subprocess

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

print(">>> Applying Ubuntu Workstation Security Hardening <<<")

# 1. Enable UFW and set default policies
run_cmd("sudo ufw default deny incoming")
run_cmd("sudo ufw default allow outgoing")
run_cmd("sudo ufw allow ssh")
run_cmd("sudo ufw --force enable")

# 2. Enforce Key-Only SSH Authentication and disable password logins
sshd_snippet = """
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin prohibit-password
"""
run_cmd("sudo mkdir -p /etc/ssh/sshd_config.d")
with open("/tmp/hardening.conf", "w") as f:
    f.write(sshd_snippet)
run_cmd("sudo mv /tmp/hardening.conf /etc/ssh/sshd_config.d/99-hardening.conf")
run_cmd("sudo systemctl restart ssh")

print(">>> Hardening Applied Successfully. Review Docker bindings manually for 'waha'. <<<")
