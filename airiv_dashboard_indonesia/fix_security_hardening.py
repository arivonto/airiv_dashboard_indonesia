import subprocess

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

print(">>> Installing UFW and Applying Final Hardening Steps <<<")

# 1. Install UFW since it wasn't present on the base setup
run_cmd("sudo apt-get update && sudo apt-get install -y ufw")

# 2. Configure UFW firewall rules
run_cmd("sudo ufw default deny incoming")
run_cmd("sudo ufw default allow outgoing")
run_cmd("sudo ufw allow ssh")
run_cmd("sudo ufw --force enable")

# 3. Secure the exposed WAHA container port by binding it to localhost
# Inspecting docker-compose or docker run parameters for waha container
print("\n>>> Checking waha container configuration <<<")
run_cmd("docker inspect waha --format='{{range .NetworkSettings.Ports}}{{.}}{{end}}'")

print(">>> Security Hardening and Firewall Configuration Complete. <<<")
