from abc import ABC

class Model:
    """
    This class is the abstraction of the models, which describes the physical
    behaviour of the car
    """
    def __init__(self) -> None:
        pass
    def update(self) -> tuple:
        pass
    def transfer_function(self):
        pass