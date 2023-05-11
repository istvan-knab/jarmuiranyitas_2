from jarmuiranyitas_2.measurement.measure_distribution import MeasureTorque
from jarmuiranyitas_2.measurement.measure_steering_angle import MeasureAngle
class StartMeasurement:
    def __init__(self, mode:str, frequency:int) -> None:

        if mode == "distribution":
            measure = MeasureTorque()
        elif mode == "steering":
            measure = MeasureAngle()
        else:
            raise Exception("Invalid measurement mode")
    def active(self):

        while True:
            pass


start= StartMeasurement("distribution", 1200)
