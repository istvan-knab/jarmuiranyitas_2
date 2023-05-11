from time import sleep

from jarmuiranyitas_2.measurement.measure_distribution import MeasureTorque
from jarmuiranyitas_2.measurement.measure_steering_angle import MeasureAngle
class StartMeasurement:
    def __init__(self, mode:str, frequency:int) -> None:
        self.frequency = frequency
        if mode == "distribution":
            self.measure = MeasureTorque()
        elif mode == "steering":
            self.measure = MeasureAngle()
        else:
            raise Exception("Invalid measurement mode")
    def active(self):
        counter = 0
        while True:
            counter += 1
            sleep(1 / self.frequency)
            self.measure.update_state_dict()
            if counter == 5:
                self.measure.write_file()
                counter = 0


start= StartMeasurement("distribution", 1200)
start.active()