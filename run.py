import os
import time
import importlib
import pywintypes

from wrapper import FEMMSession


class BaseRunner:

    def __init__(self, session=None):
        self.session = session

    def start(self):
        self.session = FEMMSession()

    def pre(self):
        raise NotImplementedError('You need to implement this method.')

    def solve(self):
        raise NotImplementedError('You need to implement this method.')

    def post(self):
        raise NotImplementedError('You need to implement this method.')

    def close(self):
        self.session.pre.close()


def _hold(stop_message):
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        print(stop_message)


def run_pre(hold=False):
    print('Running preprocessor...')
    import model
    runner = model.Runner()
    runner.start()
    runner.pre()
    if hold:
        _hold('Preprocessor stopped.')
    else:
        return runner, model


def hot_reload_pre():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.py')
    most_recent_change = os.path.getmtime(path)
    most_recent_runner, model = run_pre()
    try:
        print('Hot reloading started...')
        while True:
            time.sleep(0.5)
            if os.path.getmtime(path) > most_recent_change:
                print('Change detected. Reloading...')
                # Reload the module to pick up the new code.
                importlib.reload(model)
                # Update the most recent change time to now.
                most_recent_change = os.path.getmtime(path)

                # Create a new test instance but pass through the old session.
                most_recent_test = model.Runner(session=most_recent_runner.session)
                # Close the old document.
                most_recent_test.close()
                # Rebuild the document with the new code.
                try:
                    most_recent_test.pre()
                except pywintypes.com_error as e:
                    print('There was an error with your latest change:', e)
    except KeyboardInterrupt:
        pass
    finally:
        print('Hot reloading stopped.')


def run_solve(pre_runner, hold=False):
    print('Running solver...')
    pre_runner.solve()
    if hold:
        _hold('Solver view closed.')
    else:
        return pre_runner


def run_post(pre_runner, hold=False):
    print('Running postprocessor...')
    pre_runner.post()
    if hold:
        _hold('Postprocessor stopped.')
