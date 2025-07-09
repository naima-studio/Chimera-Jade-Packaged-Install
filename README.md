# JemOS

This repository contains all the software needed to turn a Raspberry Pi Zero 2 W into the Chimera Jade: a gateway LoRa messaging device. The device hosts its own Wi-Fi access point and provides a web interface for sending and receiving messages over the Reticulum Network Stack.

***
## Features

* **Standalone:** Creates its own Wi-Fi network for configuration and use, no external internet connection required.
* **Web Interface:** A simple and clean web UI for sending messages to other nodes on the network.
* **Hardware Feedback:** Uses an attached OLED display for status information, such as radio status and the web UI address.
* **Automated Setup:** Includes a simple installation script to configure the device from a fresh OS install.

***
## Hardware Requirements

* Raspberry Pi Zero 2 W
* RFM69 Radio Module
* 128x32 SSD1306 I2C OLED Display
* Tactile Push-buttons
* MicroSD Card and Power Supply
* Battery controll unit with lithium ion battery

***
## Installation

This process will configure your Raspberry Pi to become a dedicated access point. It is recommended to start with a fresh install of Raspberry Pi OS Lite.

1.  **Clone the Repository**
    Log into your Pi via SSH and clone this repository.
    ```bash
    git clone (https://github.com/naima-studio/Chimera-Jade-Packaged-Install.git)
    cd Chimera-Jade-Packaged-Install
    ```

2.  **Run the Installer**
    The installation script will handle all dependencies, network configuration, and setup automatically.
    ```bash
    sudo ./install.sh
    ```

3.  **Reboot the Pi**
    When the script is finished, reboot the device to apply all changes.
    ```bash
    sudo reboot
    ```
***
## Usage

After rebooting, the Pi is no longer on your home Wi-Fi. It is now broadcasting its own network.

1.  **Connect to the Hub**
    On your phone or laptop, connect to the Wi-Fi network named **`PiControlHub`** (password: `raspberry`).

2.  **Log In and Run the App**
    SSH into the Pi using its new static IP address and start the main application.
    ```bash
    # Connect to the Pi over its new network
    ssh pi@192.168.4.1

    # Navigate to the project folder
    cd PiControlHub

    # Run the main application
    python3 main_app.py
    ```

3.  **Access the Web Interface**
    Check the OLED display on the Pi. Press the first button to see the URL for the web interface, then open that address (e.g., `http://192.168.4.1:8000`) in the browser of your connected device.
