from flask import Flask, app, render_template, request

from constants import WEB_APP_HOST_IP, WEB_APP_PORT

class UserWebApp():

    def __init__(self):
        #TODO Update this
        self.app = Flask("Update this")
        #TODO Update this
        self.app.config['SECRET_KEY'] = 'pi-control-hub-secret!'
        self.app.run(app, host=WEB_APP_HOST_IP, port=WEB_APP_PORT, allow_unsafe_werkzeug=True)



    @app.route('/')
    def index():
        return render_template('interface.html')
    
    
    @app.route('/send_message', methods=['POST'])
    def handle_send_message():
        message = request.form['message']
        # TODO Send this to lxmf handler
        return f"Received message: '{message}'"
        

    # @socketio.on('send_message')
    # def handle_send_message(json_data):
    #     recipient_hexhash = json_data['recipient']
    #     message_content = json_data['content']
    #     try:
    #         recipient_hash = bytes.fromhex(recipient_hexhash)
    #         if not RNS.Transport.has_path(recipient_hash):
    #             RNS.Transport.request_path(recipient_hash)
    #             time.sleep(2)
    #         dest_identity = RNS.Identity.recall(recipient_hash)
    #         dest = RNS.Destination(dest_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery")
    #         lxm = LXMF.LXMessage(dest, lxmf_destination, message_content.encode("utf-8"), title="Message from Hub")
    #         router.handle_outbound(lxm)
    #     except Exception as e:
    #         print(f"Error sending LXMF message: {e}")