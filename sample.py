from robot_kuka import *

kr16 = RobotKuka()

kr16.start_communication("192.168.10.15", 6008)

kr16.wait_robot()

# your code goes here

kr16.stop_communication()
