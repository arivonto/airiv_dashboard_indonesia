import subprocess
import os

print(">>> Fixing WAHA Container Localhost Binding <<<")

# Check if docker-compose file exists in current or parent directories
compose_files = [f for f in os.listdir(".") if "compose" in f or f.endswith(".yml")]

if compose_files:
    print(f"Found compose file(s): {compose_files}")
    # Read and inspect compose file for waha port 3000 mapping
    for cf in compose_files:
        with open(cf, "r") as f:
            content = f.read()
        if "3000" in content:
            print(f"Found port 3000 mapping in {cf}")
            # Ensure it is bound to 127.0.0.1:3000:3000 instead of 3000:3000
            updated = content.replace('"3000:3000"', '"127.0.0.1:3000:3000"').replace('3000:3000', '127.0.0.1:3000:3000')
            if updated != content:
                with open(cf, "w") as f:
                    f.write(updated)
                print(f"Updated {cf} to bind WAHA strictly to localhost (127.0.0.1).")
                print("Restarting docker-compose stack...")
                subprocess.run(f"docker compose -f {cf} down && docker compose -f {cf} up -d", shell=True)
                break
else:
    print("No docker-compose file found in current directory. Re-creating waha container with localhost binding...")
    subprocess.run("docker stop waha && docker rm waha", shell=True)
    # Recreate container binding port strictly to localhost
    run_recreate = "docker run -d --name waha -p 127.0.0.1:3000:3000 devlikeapro/waha"
    subprocess.run(run_recreate, shell=True)

print(">>> WAHA Port Binding Remediation Complete. <<<")
