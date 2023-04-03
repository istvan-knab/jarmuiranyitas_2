from can import Message

from jarmuiranyitas_2.can.listeners.listener import Listener


class UDPListener(Listener):
    def __init__(self):
        super(UDPListener, self).__init__()

    def on_message_recieved(self, msg: Message) -> None:
        pass

    def on_error(self):
        pass

    def enable_drive(self) -> bool:
        pass
