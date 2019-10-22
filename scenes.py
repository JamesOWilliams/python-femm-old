import multiprocessing as mp
import _winapi
import time

import matplotlib.pyplot as plt
import numpy as np

from model import Runner


class BaseSceneRunner:

    def __init__(self, scene_class=None):
        self.scene_class = scene_class()

    def start(self):
        print(f'Running scene with {len(self.scene_class.values)} instances, on {mp.cpu_count()} processes...')
        mp.set_executable(_winapi.GetModuleFileName(0))
        start_time = time.perf_counter()
        with mp.Pool(mp.cpu_count()) as pool:
            self.results = pool.map(self.scene_class.run_scene, self.scene_class.values)
        end_time = time.perf_counter()
        print(f'Finished in {np.round(end_time - start_time)} seconds.')
        self.end()

    def end(self):
        print(f'Displaying results...')
        self.scene_class.display_results(self.results)


class ForceYScene:

    values = np.linspace(60, 61, 10)

    @staticmethod
    def run_scene(value):
        runner = Runner()
        runner.start()
        runner.pre(process_id=mp.current_process(), rotor_center=[60, value])
        runner.solve()
        force_y = runner.post()
        return force_y

    def display_results(self, results):
        plt.plot(self.values, results)
        plt.show()
