import multiprocessing as mp

import numpy as np

from model import Runner


def run(rotor_center_y_value):
    runner = Runner()
    runner.start()
    runner.pre(rotor_center=[60, rotor_center_y_value])
    runner.solve()
    force_y = runner.post()
    return force_y


def scene():
    rotor_center_y_values = np.linspace(60, 61.5, 5)
    pool = mp.Pool(processes=2)
    res = pool.map(run, rotor_center_y_values)
    # pool.close()
    print(res)
