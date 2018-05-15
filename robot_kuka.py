# Guilherme R. Moreira, 2017
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------

import logging
import time
import math
from multiprocessing import Queue
from threading import Thread, Event
from models import DigitalOutput
from xml_modifiers import *
from collections import deque
from itertools import islice
from impedance_control import *


MAX_BYTES = 65535  # defines the max amount of bytes in the UDP datagram
CYCLE_TIME = 0.012  # defines the time (seconds) of a robot communication cycle


def wait_move_finished(func):
    def wrapper(self, *arg, **kwargs):
        time.sleep(CYCLE_TIME * 0.8)
        self.move_event.wait()
        res = func(self, *arg, **kwargs)
        return res
    return wrapper


class RobotKuka:

    def __init__(self):
        self.communication_thread = None
        self.move_queue = Queue()
        self.wait_robot_event = Event()
        self.stop_communication_event = Event()
        self.data_received_event = Event()
        self.move_event = Event()
        self.data_deque = deque()
        self.data_collect_flags = {}
        self.dig_out = DigitalOutput()
        self.impedance_control_x = None
        self.impedance_control_y = None
        self.impedance_control_z = None
        self.lost_packages = 0

    # ==================================================================================================================
    # Functions related with connection between robot and pc -----------------------------------------------------------

    def start_communication(self, pc_ip, pc_port):
        def start_thread():
            try:
                self.communication_thread = Thread(target=self.connection, name='communication', args=(pc_ip, pc_port))
                self.communication_thread.start()
                print('The communication has been established.')
            except Exception as error:
                print('Start communication has failed: {}'.format(error))

        if self.communication_thread is None:
            start_thread()
        else:
            if not self.communication_thread.is_alive():
                start_thread()
            else:
                print('The communication is already running.')

    def stop_communication(self):
        print('Pacotes perdidos: {}'.format(self.lost_packages))

        def terminate_thread():
            while not self.move_queue.empty():
                time.sleep(CYCLE_TIME)
            try:
                self.stop_communication_event.set()
                print('Communication has been closed.')
            except Exception as error:
                print('Stop communication has failed: {}'.format(error))

        if self.communication_thread is not None:
            if self.communication_thread.is_alive():
                terminate_thread()
            else:
                print('There is no communication to stop.')
        else:
            print('There is no communication to stop.')

    def connection(self, server_ip, server_port):
        import socket
        # inner functions of connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((server_ip, server_port))
        print('Listening at', sock.getsockname())  # Starts listening at client (robot)
        i = 0

        while 1:
            # start_time = time.time()

            if self.stop_communication_event.is_set():
                self.stop_communication_event.clear()
                break
            data, address = sock.recvfrom(MAX_BYTES)
            if i > 0:
                self.wait_robot_event.set()

            xml_send_string = data.decode('ascii')  # xml_send is the xml file sent from Kuka to PC
            xml_send = Xml.fromstring(xml_send_string)

            # get sensor data - feed the queue
            if i == 0:  # first received xml from pc only contains ipoc value
                ipoc = xml_send.find('IPOC').text
                data = Data()
                i += 1
            else:
                data = get_data_from_send_xml(xml_send)
                ipoc = str(data.ipoc)
                if data.delay > 0:
                    self.lost_packages += 1

            try:
                self.data_deque.append(data)
            except Exception as error:
                self.data_deque.append(Data())
                print('Sensor data queue received null data object: '.join(str(error)))

            # xml_receive is the xml file sent from PC to Kuka
            if self.move_queue.empty():
                if ~self.move_event.is_set():
                    self.move_event.set()
                position = Coordinates()
            else:
                if self.move_event.is_set():
                    self.move_event.clear()
                position = self.move_queue.get()
                if data.delay > 0:
                    self.move_queue.put(position)

            if self.impedance_control_x is not None and self.impedance_control_y is not None and self.impedance_control_z is not None:
                position.x += self.impedance_control_x.correction(data.ftc.x)
                position.y += self.impedance_control_y.correction(data.ftc.y)
                position.z += self.impedance_control_z.correction(-(-30-data.ftc.z))

                '''
                print('Fx: %.4f -> Cx: %.6f | Fy: %.4f -> Cy: %.6f | Fz: %.4f -> Cz: %.6f | ' %
                      (data.ftc.x, self.impedance_control_x.correction(data.ftc.x),
                       data.ftc.y, self.impedance_control_y.correction(data.ftc.y),
                       data.ftc.z, self.impedance_control_z.correction(data.ftc.z)))
                       '''

            xml_receive = generate_receive_xml(position, self.dig_out, ipoc)
            sock.sendto(xml_receive, address)
            # print("---Delay: %d --- Move: %s ---" % (data.delay, str(self.move_event.is_set()), ))

    def wait_robot(self):
        self.wait_robot_event.wait()

    # ==================================================================================================================
    # Functions related with robots movement ---------------------------------------------------------------------------

    def move(self, x=0, y=0, z=0, a=0, b=0, c=0, li_speed=200, an_speed=6):  # li_speed in mm/s & an_speed in deg/s

        def split_position(position, li_s, an_s):  # returns positions deque
            n_li = math.ceil(math.sqrt(math.pow(position.x, 2) + math.pow(position.y, 2) + math.pow(position.z, 2))
                             / (li_s * CYCLE_TIME))
            n_an = math.ceil(math.sqrt(math.pow(position.a, 2) + math.pow(position.b, 2) + math.pow(position.c, 2))
                             / (an_s * CYCLE_TIME))
            n_p = max([n_li, n_an])
            splitted_position = Coordinates(x=position.x / n_p, y=position.y / n_p, z=position.z / n_p,
                                            a=position.a / n_p, b=position.b / n_p, c=position.c / n_p)
            return [splitted_position, n_p]

        split_position, n = split_position(Coordinates(x, y, z, a, b, c), li_speed, an_speed) # config for normal home

        def f(q):  # auxiliary function required for the target of the process
            positions = [split_position]*n
            for position in positions:
                q.put(position)

        put_queue_thread = Thread(target=f, args=(self.move_queue,))  # process to insert into the queue
        put_queue_thread.start()  # starts the process
        put_queue_thread.join()  # hold the parent process until the method is finished

    @wait_move_finished
    def go_to(self, position, li_speed=200, an_speed=6):
        current_position = self.get_current_position()
        print(str(position.x-current_position.x)+'|'+str(position.y-current_position.y)+'|'+str(position.z-current_position.z)+'|'+str(position.a-current_position.a)+'|'+str(position.b-current_position.b)+'|'+str(position.c-current_position.c))
        print(str(current_position.a))
        print(str(current_position.b))
        print(str(current_position.c))
        self.move(x=-(position.x-current_position.x), y=-(position.y-current_position.y), z=-(position.z-current_position.z),
                  a=0, b=0, c=0, li_speed=li_speed, an_speed=an_speed)  # TODO angles movement

    # This function is to provide a piece of time in which the robot is at rest, just like time.sleep() in Python.
    # time.sleep() is not safe to use because it does not wait until a robot motion is finalized, since the motion
    # commands are operated by separate threads.
    @wait_move_finished
    def sleep(self, t):
        def f():  # auxiliary function required for the target of the process
            time.sleep(t)  # calls the conventional time.sleep() function

        thread = Thread(target=f, args=())  # thread used just to hold the parent thread
        thread.start()  # starts the thread
        thread.join()  # hold the parent thread until the method is finished

    # ==================================================================================================================
    # Functions to collect data and save into files --------------------------------------------------------------------

    @wait_move_finished
    def start_collect(self, output):
        self.data_collect_flags[output] = len(self.data_deque) - 1

    @wait_move_finished
    def stop_collect(self, output, file=False):

        if file:
            def f(fn):  # auxiliary function required for the target of the process
                self.generate_data_file(fn)

            put_queue_process = Thread(target=f, args=(output,))
            put_queue_process.start()  # starts the process
            put_queue_process.join()  # hold the process until the method is finished

        del self.data_collect_flags[output]

    def get_collected_array(self, output):

        first_index = int(self.data_collect_flags[output])
        last_index = len(self.data_deque)

        data_list = list(islice(self.data_deque, first_index, last_index))

        fx = []
        fy = []
        fz = []
        mx = []
        my = []
        mz = []

        for data in data_list:
            fx.append(data.ftc.x)
            fy.append(data.ftc.y)
            fz.append(data.ftc.z)
            mx.append(data.ftc.c)
            my.append(data.ftc.b)
            mz.append(data.ftc.a)

        return fx, fy, fz, mx, my, mz

    @wait_move_finished
    def generate_data_file(self, output):
        first_index = int(self.data_collect_flags[output])
        last_index = len(self.data_deque)

        data_list = list(islice(self.data_deque, first_index, last_index))

        first_ipoc = data_list[0].ipoc

        file = open(output, 'a')

        first_line = 'time,x,y,z,rotx,roty,rotz,fx,fy,fz,mx,my,mz,\n'
        file.write(first_line)

        def write_line(d):
            instant = (d.ipoc - first_ipoc)*2/1000
            row = ','.join([str(instant), str(d.r_ist.x), str(d.r_ist.y), str(d.r_ist.z), str(d.r_ist.a),
                            str(d.r_ist.b), str(d.r_ist.c), str(d.ftc.x), str(d.ftc.y), str(d.ftc.z),
                            str(d.ftc.c), str(d.ftc.b), str(d.ftc.a), '\n']) # antes estava a, b, c
            file.write(row)

        for data in data_list:
            write_line(data)

        file.close()

    # ==================================================================================================================
    # Functions to read data from robot in real time -------------------------------------------------------------------

    @wait_move_finished
    def read(self, index=0):  # index defines how far from the end of the list the data is returned [negative values]
        if index <= 0:
            return self.data_deque[len(self.data_deque)+index-1]  # returns a Data type object
        else:
            logging.warning('Index of function read must be not positive (default=0). Value passed: %d', index)
            return Data()

    @wait_move_finished
    def get_current_position(self):
        current_data = self.data_deque[len(self.data_deque) - 1]
        current_position = Coordinates(x=current_data.r_ist.x, y=current_data.r_ist.y, z=current_data.r_ist.z,
                                       a=current_data.r_ist.a, b=current_data.r_ist.b, c=current_data.r_ist.c)
        return current_position

    @wait_move_finished
    def get_current_forces(self):
        current_data = self.data_deque[len(self.data_deque) - 1]
        current_forces = Coordinates(x=current_data.ftc.x, y=current_data.ftc.y, z=current_data.ftc.z,
                                     a=current_data.ftc.a, b=current_data.ftc.b, c=current_data.ftc.c)
        return current_forces

    # ==================================================================================================================
    # Functions to send digital outputs to robot -----------------------------------------------------------------------

    @wait_move_finished
    def digital_output(self, o1=0, o2=0, o3=0):
        self.dig_out.o1 = o1
        self.dig_out.o2 = o2
        self.dig_out.o3 = o3

    def reset_grip(self):
        self.digital_output(o1=0, o2=0)

    def open_grip(self):
        self.reset_grip()
        self.digital_output(o1=1, o2=0)

    def close_grip(self):
        self.reset_grip()
        self.digital_output(o1=0, o2=1)



    # ==================================================================================================================
    # Functions related to impedance control ---------------------------------------------------------------------------

    # Function that chooses between the two implementation methods of impedance control and initiates it
    # 'i' := integration
    # 'd' := discretization
    @wait_move_finished
    def activate_impedance_control_x(self, m=0, b=0, k=0, mode='d'):

        def integration():
            self.impedance_control_x = Integration(m=m, b=b, k=k, ts=CYCLE_TIME)

        def discretization():
            self.impedance_control_x = Discretization(m=m, b=b, k=k, ts=CYCLE_TIME)

        def error():
            logging.warning('You must choose a valid impedance control method: -- i (integration) or d '
                            '(discretization/default) --. Given: %s', mode)

        switcher = {
            'i': integration,
            'd': discretization,
        }
        # Get the function from switcher dictionary
        func = switcher.get(mode, error)
        # Execute the function
        return func()

    @wait_move_finished
    def activate_impedance_control_y(self, m=0, b=0, k=0, mode='d'):

        def integration():
            self.impedance_control_y = Integration(m=m, b=b, k=k, ts=CYCLE_TIME)

        def discretization():
            self.impedance_control_y = Discretization(m=m, b=b, k=k, ts=CYCLE_TIME)

        def error():
            logging.warning('You must choose a valid impedance control method: -- i (integration) or d '
                            '(discretization/default) --. Given: %s', mode)

        switcher = {
            'i': integration,
            'd': discretization,
        }
        # Get the function from switcher dictionary
        func = switcher.get(mode, error)
        # Execute the function
        return func()

    @wait_move_finished
    def activate_impedance_control_z(self, m=0, b=0, k=0, mode='d'):

        def integration():
            self.impedance_control_z = Integration(m=m, b=b, k=k, ts=CYCLE_TIME)

        def discretization():
            self.impedance_control_z = Discretization(m=m, b=b, k=k, ts=CYCLE_TIME)

        def error():
            logging.warning('You must choose a valid impedance control method: -- i (integration) or d '
                            '(discretization/default) --. Given: %s', mode)

        switcher = {
            'i': integration,
            'd': discretization,
        }
        # Get the function from switcher dictionary
        func = switcher.get(mode, error)
        # Execute the function
        return func()

    # Function that deactivates the current impedance control method set
    @wait_move_finished
    def deactivate_impedance_control(self):
        self.impedance_control_x = None
        self.impedance_control_y = None
        self.impedance_control_z = None
