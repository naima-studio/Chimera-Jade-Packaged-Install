# This file contains the logic to interface with the LoRa board
import time
import RNS
import board
import threading
from digitalio import DigitalInOut, Direction, Pull
import busio
import adafruit_ssd1306
import adafruit_rfm69
from constants import WEB_APP_HOST_IP, WEB_APP_PORT


class LoraHandler():

    def __init__(self):
        # Device IP
        self.PI_IP_ADDRESS = "192.168.4.1"
        self.lora_running = False
        # Initialize the LoRa hardware
        successful = self.initialize_hardware()
        print(f'LoRa board sucessfully started: {successful}')
        if successful:
            self.start_lora()
        else:
            # TODO figure out what this is for
            RNS.Transport.exit_handler()



    def initialize_hardware(self) -> bool:
        btnA = DigitalInOut(board.D5)
        self.btnA = btnA

        btnA.direction = Direction.INPUT
        btnA.pull = Pull.UP

        i2c = busio.I2C(board.SCL, board.SDA)
        reset_pin = DigitalInOut(board.D4)

        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        self.display = display

        display.fill(0)
        display.show()

        CS = DigitalInOut(board.CE0)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

        try:
            self.rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
            return True
        except RuntimeError as e:
            print(e)
            return False

        

  
    def start_lora(self):
        if self.lora_running:
            return "LoRa board has already been enabled!"
        
        self.lora_thread = threading.Thread(target=self.lora_thread_runner)
        self.lora_thread.daemon = True
        self.lora_thread.start()
        self.lora_running = True
        self.display


    def lora_thread_runner(self):
        # Get all constants
        display = self.display
        btnA = self.btnA

        while True:
            display.fill(0)
            display.text('RFM69: OK', 0, 0, 1)

            # if LXMF_ADDRESS:
            #     display.text(f"Addr: {LXMF_ADDRESS[:10]}...", 0, 10, 1)

            if not btnA.value:
                display.fill(0)
                display.text('Web Interface URL:', 0, 0, 1)
                display.text(f"http://{WEB_APP_HOST_IP}:{WEB_APP_PORT}", 0, 12, 1)

            display.show()
            time.sleep(0.1)



        
