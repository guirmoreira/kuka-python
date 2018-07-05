# Guilherme R. Moreira, 2017
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------


class ImpedanceControl:

    def __init__(self, m, b, k, ts=0.012):
        self.m = m
        self.b = b
        self.k = k
        self.ts = ts


class Integration(ImpedanceControl):

    def __init__(self, m, b, k, ts):
        super(Integration, self).__init__(m, b, k, ts)
        self.x = 0
        self.dx = 0
        self.ddx = 0
        self.x_ant = 0
        self.dx_ant = 0
        self.ddx_ant = 0

    def correction(self, force):

        self.ddx = (force-self.k*self.x-self.b*self.dx)/self.m
        self.dx = (self.ts/(2*(self.ddx+self.ddx_ant)))+self.dx_ant
        self.x = (self.ts/(2*(self.dx+self.dx_ant)))+self.x_ant

        self.x_ant = self.x
        self.dx_ant = self.dx
        self.ddx_ant = self.ddx

        return self.x


class Discretization(ImpedanceControl):

    def __init__(self, m, b, k, ts):
        super(Discretization, self).__init__(m, b, k, ts)
        self.x = 0
        self.x_ant = 0
        self.x_ant2 = 0
        self.force_ant = 0
        self.force_ant2 = 0

    def correction(self, force):

        ts2 = self.ts * self.ts
        den = (4*self.m)+(2*self.ts*self.b)+(ts2*self.k)
        b1 = 2*ts2*self.k-8*self.m
        b2 = 4*self.m-2*self.ts*self.b+ts2*self.k

        self.x = (ts2*force+2*ts2*self.force_ant+ts2*self.force_ant2-b1*self.x_ant-b2*self.x_ant2)/den

        self.x_ant2 = self.x_ant
        self.x_ant = self.x
        self.force_ant2 = self.force_ant
        self.force_ant = force

        return self.x

