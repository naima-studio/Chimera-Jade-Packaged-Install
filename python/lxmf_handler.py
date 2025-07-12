import LXMF
import RNS
from lora_handler import LoraHandler

class LXMFHandler():

    def __init__(self):
        # Create LoRa handler
        self.lora_handler = LoraHandler()
        
        # Setup LXMF routing data
        self.rns = RNS.Reticulum()
        self.router = LXMF.LXMRouter(storagepath="./lxmf_storage")
        self.identity = RNS.Identity()
        # Add lxmf routing edge 
        self.lxmf_destination = self.router.register_delivery_identity(self.identity, display_name="PiControlHub")
        self.LXMF_ADDRESS = RNS.prettyhexrep(self.lxmf_destination.hash)  # Assigned once here
        # Register callback functions
        self.router.register_delivery_callback(self.delivery_callback)
        self.router.announce(self.lxmf_destination.hash)

        

    def delivery_callback(self, message):
        message_data = {
            "source_hash": RNS.prettyhexrep(message.source_hash),
            "source_name": f"Node-{RNS.prettyhexrep(message.source_hash)[:6]}",
            "title": message.title_as_string(),
            "content": message.content_as_string(),
            "timestamp": message.timestamp,
        }
        print(f'Received messsage: {message_data}')
        # TODO update front end with new message
        # socketio.emit('new_message', message_data)
