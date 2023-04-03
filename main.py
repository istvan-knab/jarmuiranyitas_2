from jarmuiranyitas_2.can.run import CAN


def main():
    can_comm = CAN()

    can_comm.start_communication()


if __name__ == "__main__":
    main()
