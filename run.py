import os
import time
import importlib
import pywintypes

from pyfemm_test.wrapper import FEMMSession


class BaseRunner:

    def __init__(self, session=None):
        self.session = session

    def start(self):
        self.session = FEMMSession()

    def pre(self):
        raise NotImplementedError('You need to implement this method.')

    def post(self):
        raise NotImplementedError('You need to implement this method.')

    def close(self):
        self.session.pre.close()


if __name__ == '__main__':
    import pyfemm_test.examples.magnetic_bearing
    path = 'C:/Users/mail/pyfemm_test/examples/magnetic_bearing.py'
    most_recent_change = os.path.getmtime(path)
    most_recent_runner = pyfemm_test.examples.magnetic_bearing.Runner()
    most_recent_runner.start()
    most_recent_runner.pre()
    try:
        print('Hot reloading started...')
        while True:
            time.sleep(0.5)
            if os.path.getmtime(path) > most_recent_change:
                print('Change detected. Reloading...')
                # Reload the module to pick up the new code.
                importlib.reload(pyfemm_test.examples.magnetic_bearing)
                # Update the most recent change time to now.
                most_recent_change = os.path.getmtime(path)

                # Create a new test instance but pass through the old session.
                most_recent_test = pyfemm_test.examples.magnetic_bearing.Runner(session=most_recent_runner.session)
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
