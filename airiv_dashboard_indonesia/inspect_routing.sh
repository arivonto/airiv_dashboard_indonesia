#!/bin/bash
echo ">>> Scanning all active listening ports and Docker containers <<<"
sudo ss -tulpn
echo "--------------------------------------------------------"
docker ps -a
