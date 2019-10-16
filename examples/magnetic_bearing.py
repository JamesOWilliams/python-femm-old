from pyfemm_test.run import BaseRunner


class Runner(BaseRunner):

    def pre(self):
        self.session.new_document(0)

        # Define dimensions.
        center = [60, 60]
        poles = 4
        pole_length = 22
        pole_width = 20
        stator_diameter = 120
        stator_width = 8
        smoothing = 1.4
        angle = (360 / poles) / smoothing
        rotor_diameter = 55
        rotor_bore = 10

        # Draw the bearing stator.
        self.session.pre.draw_circle(*center, stator_diameter, 60)
        stator_points = self.session.pre.draw_polyline_pattern([
            [center[0] - (pole_width / 2), stator_diameter - stator_width],
            [center[0] - (pole_width / 2), stator_diameter - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), stator_diameter - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), stator_diameter - stator_width],
        ], center=center, repeat=poles)
        self.session.pre.draw_arc_pattern(*stator_points[0][0], *stator_points[1][::-1][0], angle, 60, center=center,
                                          repeat=poles)

        # Draw the bearing rotor.
        self.session.pre.draw_annulus(*center, inner_radius=rotor_bore, outer_radius=rotor_diameter, max_seg=60)

        # Refit the view window.
        self.session.pre.zoom_natural()

    def post(self):
        pass
