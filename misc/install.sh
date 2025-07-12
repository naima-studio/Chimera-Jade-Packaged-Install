#!/bin/bash

# --- Check for root privileges ---
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script with sudo: sudo ./install.sh"
  exit
fi

echo "🚀 Starting Pi Control Hub Installation..."

# --- 1. System Updates and Dependencies ---
echo "⚙️ Updating package lists and installing system dependencies..."
apt-get update
apt-get install -y hostapd dnsmasq git python3-pip

# --- 2. Python Dependencies ---
echo "🐍 Installing Python packages from requirements.txt..."
pip3 install -r requirements.txt

# --- 3. Network Configuration ---
echo "🌐 Configuring Wi-Fi Access Point..."
# Configure static IP for wlan0
echo "" >> /etc/dhcpcd.conf
echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf
echo "nohook wpa_supplicant" >> /etc/dhcpcd.conf

# Copy our custom hostapd and dnsmasq configs
echo "    - Copying hostapd and dnsmasq configurations..."
cp config/hostapd.conf /etc/hostapd/hostapd.conf
cp config/dnsmasq.conf /etc/dnsmasq.conf

# Point the hostapd service to our new config file
echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' > /etc/default/hostapd

# --- 4. Reticulum Configuration ---
echo "⚙️  Setting up Reticulum configuration for LoRa radio..."
mkdir -p /home/pi/.reticulum
cp config/reticulum_config /home/pi/.reticulum/config
chown -R pi:pi /home/pi/.reticulum

# --- 5. Enable Services ---
echo "✨ Enabling and unmasking services..."
systemctl unmask hostapd
systemctl enable hostapd
systemctl enable dnsmasq

# --- 6. Final Steps ---
echo "✅ Installation Complete!"
echo "Please reboot the Raspberry Pi to apply all changes."
echo "After rebooting, run the application with: python3 main_app.py"