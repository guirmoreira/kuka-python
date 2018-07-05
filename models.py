# Guilherme R. Moreira, 2017
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------


class Coordinates:

    def __init__(self, x=0, y=0, z=0, a=0, b=0, c=0):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    def plot(self):
        print('x: '+str(self.x)+'|y: '+str(self.y)+'|z: '+str(self.z)+'|a: '+str(self.a)+'|b: '+str(self.b)+'|c: '+str(self.c))


class Axes:

    def __init__(self, a1=0, a2=0, a3=0, a4=0, a5=0, a6=0):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.a6 = a6


class Move:

    def __init__(self, coordinates=Coordinates(), axes=Axes()):
        self.coordinates = coordinates
        self.axes = axes


class DigitalOutput:

    def __init__(self, o1=0, o2=0, o3=0):
        self.o1 = o1
        self.o2 = o2
        self.o3 = o3


class Data:
    # TODO: explain the data names from xml-send
    def __init__(self, r_ist=Coordinates(), r_sol=Coordinates(), ai_pos=Axes(), as_pos=Axes(), ei_pos=Axes(),
                 es_pos=Axes(), ma_cur=Axes(), me_cur=Axes(), delay=0, ftc=Coordinates(), ipoc=0):
        self.r_ist = r_ist
        self.r_sol = r_sol
        self.ai_pos = ai_pos
        self.as_pos = as_pos
        self.ei_pos = ei_pos
        self.es_pos = es_pos
        self.ma_cur = ma_cur
        self.me_cur = me_cur
        self.delay = delay
        self.ftc = ftc
        self.ipoc = ipoc