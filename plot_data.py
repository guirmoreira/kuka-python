import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Process

path = '/home/guilherme/Drive/research/Iniciação Científica/Codes/kuka_comunication/connection/robot'


def f(i=1):

    data_size = 1715

    file = ''.join([path, '/data/data_adjust-', str(i), '.csv'])
    data = pd.read_csv(file)

    t = data.iloc[:data_size, 0].values
    x = data.iloc[:data_size, 1].values
    y = data.iloc[:data_size, 2].values
    z = data.iloc[:data_size, 3].values
    rx = data.iloc[:data_size, 4].values
    ry = data.iloc[:data_size, 5].values
    rz = data.iloc[:data_size, 6].values
    fx = data.iloc[:data_size, 7].values
    fy = data.iloc[:data_size, 8].values
    fz = data.iloc[:data_size, 9].values
    mz = data.iloc[:data_size, 10].values
    my = data.iloc[:data_size, 11].values
    mx = data.iloc[:data_size, 12].values

    plt.subplot(2, 2, 1)
    plt.plot(t, fx, label='Fx')
    plt.plot(t, fy, label='Fy')
    plt.plot(t, fz, label='Fz')
    plt.title('Adjust: forces')
    plt.xlabel('time (s)')
    plt.ylabel('force (N)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)

    plt.subplot(2, 2, 2)
    plt.plot(t, mx, label='Mx')
    plt.plot(t, my, label='My')
    plt.plot(t, mz, label='Mz')
    plt.title('Adjust: moment')
    plt.xlabel('time (s)')
    plt.ylabel('moment (N.m)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)

    file = ''.join([path, '/data/data_threading-', str(i), '.csv'])
    data = pd.read_csv(file)

    t = data.iloc[:data_size, 0].values
    x = data.iloc[:data_size, 1].values
    y = data.iloc[:data_size, 2].values
    z = data.iloc[:data_size, 3].values
    rx = data.iloc[:data_size, 4].values
    ry = data.iloc[:data_size, 5].values
    rz = data.iloc[:data_size, 6].values
    fx = data.iloc[:data_size, 7].values
    fy = data.iloc[:data_size, 8].values
    fz = data.iloc[:data_size, 9].values
    mz = data.iloc[:data_size, 10].values
    my = data.iloc[:data_size, 11].values
    mx = data.iloc[:data_size, 12].values

    plt.subplot(2, 2, 3)
    plt.plot(t, fx, label='Fx')
    plt.plot(t, fy, label='Fy')
    plt.plot(t, fz, label='Fz')
    plt.title('Threading: forces')
    plt.xlabel('time (s)')
    plt.ylabel('force (N)')

    plt.subplot(2, 2, 4)
    plt.plot(t, mx, label='Mx')
    plt.plot(t, my, label='My')
    plt.plot(t, mz, label='Mz')
    plt.title('Threadind: moment')
    plt.xlabel('time (s)')
    plt.ylabel('moment (N.m)')
    plt.show()


def plot(i):
    p = Process(target=f, args=(i,))
    p.start()