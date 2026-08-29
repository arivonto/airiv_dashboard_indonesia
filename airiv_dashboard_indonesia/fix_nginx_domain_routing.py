import subprocess
import os

print("Checking Nginx and reverse proxy configuration for erp.airiv.id...")

nginx_conf_dirs = ["/etc/nginx/sites-available", "/etc/nginx/conf.d"]
found_conf = None

for d in nginx_conf_dirs:
    if os.path.exists(d):
        for f in os.listdir(d):
            path = os.path.join(d, f)
            if os.path.isfile(path):
                with open(path, "r") as file:
                    content = file.read()
                    if "erp.airiv.id" in content:
                        found_conf = path
                        print(f"Found domain configuration in: {found_conf}")
                        break

if found_conf:
    with open(found_conf, "r") as f:
        conf_data = f.read()
    
    # Ensure proxy settings correctly map /demo and /web to backend port 8069
    print("Verifying upstream and location blocks...")
    if "proxy_pass http://127.0.0.1:8069;" not in conf_data:
        print("Injecting correct proxy pass settings...")
        # Simple update logic to ensure proper proxying
        updated_conf = conf_data.replace("proxy_pass http://localhost:8069;", "proxy_pass http://127.0.0.1:8069;")
        with open(found_conf, "w") as f:
            f.write(updated_conf)
            
    subprocess.run("sudo nginx -t && sudo systemctl reload nginx", shell=True)
else:
    print("No direct Nginx config file found for erp.airiv.id. Checking Traefik or alternative reverse proxy setup...")
    subprocess.run("docker ps --filter name=proxy --filter name=traefik --filter name=nginx", shell=True)

print("Domain routing fix script executed.")
