#!/bin/bash

echo "Downloading the latest Google Chrome package..."
wget -q --show-progress -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

echo "Installing the downloaded package..."
sudo apt install -y /tmp/google-chrome-stable_current_amd64.deb

echo "Cleaning up temporary files..."
rm /tmp/google-chrome-stable_current_amd64.deb

echo "Update complete. New version:"
google-chrome-stable --version
