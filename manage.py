import sys

from run import run_pre, run_solve, hot_reload_pre, run_post
from scenes import BaseSceneRunner, ForceYScene

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        raise ValueError('Must provide a command name.')
    if not len(args) == 2:
        raise ValueError('Must provide only one argument.')
    _, command_name = args
    if command_name == 'dev':
        hot_reload_pre()
    elif command_name == 'pre':
        run_pre(hold=True)
    elif command_name == 'solve':
        pre_runner, _ = run_pre()
        run_solve(pre_runner, hold=True)
    elif command_name == 'post':
        pre_runner, _ = run_pre()
        pre_runner = run_solve(pre_runner)
        run_post(pre_runner, hold=True)
    elif command_name == 'scene':
        scene_runner = BaseSceneRunner(scene_class=ForceYScene)
        scene_runner.start()
    else:
        raise ValueError('No matching command.')
