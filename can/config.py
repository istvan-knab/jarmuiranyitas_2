import argparse


class Config:

    def __init__(self):
        self.arguments = argparse.ArgumentParser(prog="4WD Car")
        self.add_arguments()
        self.stored_arguments = self.arguments.parse_args()

    def add_arguments(self):
        self.arguments.add_argument("--interface", "-i", action="store", choices=["socketcan", "kvaser"],
                                    default="socketcan", required=False, type=str)
        self.arguments.add_argument("--channel", "-c", action="store", choices=["0", "can0"], default="can0",
                                    required=False, type=str)
        self.arguments.add_argument("--bitrate", "-b", action="store", choices=[62500, 125000, 250000, 500000, 1000000],
                                    default=500000, required=False, type=int)
        self.arguments.add_argument("--receive_own_messages", "-r", action="store", default=False, required=False,
                                    type=bool)

    def get_interface(self):
        interface = self.stored_arguments.interface

        return str(interface)

    def get_channel(self):
        channel = self.stored_arguments.channel

        return str(channel)

    def get_bitrate(self):
        bitrate = self.stored_arguments.bitrate

        return int(bitrate)

    def get_receive_own_messages(self):
        receive_own_messages = self.stored_arguments.receive_own_messages

        return bool(receive_own_messages)
