from robot_kuka import *

kr16 = RobotKuka()

kr16.start_communication("192.168.10.15", 6008)

kr16.move(x=100)

kr16.stop_communication()
