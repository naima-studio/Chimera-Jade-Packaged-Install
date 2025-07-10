import RNS
import LXMF
import time
import board
import busio
import threading
from digitalio import DigitalInOut, Direction, Pull
import Adafruit_SSD1306
import adafruit_rfm69
from flask import Flask, render_template
from flask_socketio import SocketIO

# --- GLOBAL CONFIG & STATE ---
PI_IP_ADDRESS = "192.168.4.1"
LXMF_ADDRESS = ""

# --- HARDWARE & DISPLAY THREAD ---
def hardware_thread_func():
    global LXMF_ADDRESS
    btnA = DigitalInOut(board.D5)
    btnA.direction = Direction.INPUT
    btnA.pull = Pull.UP
    i2c = busio.I2C(board.SCL, board.SDA)
    reset_pin = DigitalInOut(board.D4)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
    display.fill(0)
    display.show()
    time.sleep(1)
    CS = DigitalInOut(board.CE0)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    while True:
        display.fill(0)
        try:
            rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
            display.text('RFM69: OK', 0, 0, 1)
        except RuntimeError:
            display.text('RFM69: ERROR', 0, 0, 1)
        if LXMF_ADDRESS:
            display.text(f"Addr: {LXMF_ADDRESS[:10]}...", 0, 10, 1)
        if not btnA.value:
            display.fill(0)
            display.text('Web Interface URL:', 0, 0, 1)
            display.text(f"http://{PI_IP_ADDRESS}:8000", 0, 12, 1)
        display.show()
        time.sleep(0.1)

# --- RETICULUM, LXMF, and FLASK SETUP ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pi-control-hub-secret!'
socketio = SocketIO(app)
rns = RNS.Reticulum()
router = LXMF.LXMRouter(storagepath="./lxmf_storage")
identity = RNS.Identity()
lxmf_destination = router.register_delivery_identity(identity, display_name="PiControlHub")
LXMF_ADDRESS = RNS.prettyhexrep(lxmf_destination.hash)

def delivery_callback(message):
    message_data = {
        "source_hash": RNS.prettyhexrep(message.source_hash),
        "source_name": f"Node-{RNS.prettyhexrep(message.source_hash)[:6]}",
        "title": message.title_as_string(),
        "content": message.content_as_string(),
        "timestamp": message.timestamp,
    }
    socketio.emit('new_message', message_data)

router.register_delivery_callback(delivery_callback)

@app.route('/')
def index():
    return render_template('interface.html')

@socketio.on('send_message')
def handle_send_message(json_data):
    recipient_hexhash = json_data['recipient']
    message_content = json_data['content']
    try:
        recipient_hash = bytes.fromhex(recipient_hexhash)
        if not RNS.Transport.has_path(recipient_hash):
            RNS.Transport.request_path(recipient_hash)
            time.sleep(2)
        dest_identity = RNS.Identity.recall(recipient_hash)
        dest = RNS.Destination(dest_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery")
        lxm = LXMF.LXMessage(dest, lxmf_destination, message_content.encode("utf-8"), title="Message from Hub")
        router.handle_outbound(lxm)
    except Exception as e:
        print(f"Error sending LXMF message: {e}")

if __name__ == '__main__':
    try:
        router.announce(lxmf_destination.hash)
        hw_thread = threading.Thread(target=hardware_thread_func)
        hw_thread.daemon = True
        hw_thread.start()
        socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        RNS.Transport.exit_handler()
        exit()