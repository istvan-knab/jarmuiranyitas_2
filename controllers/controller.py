from abc import ABC, abstractmethod


class Controller(ABC):

    @abstractmethod
    def control(self, input_vector: list):
        output_vector = None

        return output_vector
