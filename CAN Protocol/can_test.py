from can_protocol import Can
from time import sleep

can = Can()
can.start_motors()
can.drive()
