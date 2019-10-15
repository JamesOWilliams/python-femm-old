from pyfemm_test.run import BaseRunner


class Runner(BaseRunner):

    def pre(self):
        self.session.new_document(0)

        # Draw the bearing stator
        self.session.pre.draw_polygon([
            [0, 0],
            [1, 1],
            [1, 2],
            [2, 1],
        ])

    def post(self):
        pass
