from pyfemm_test.run import BaseRunner


class Runner(BaseRunner):

    def pre(self):
        self.session.new_document(0)

        # Define dimensions.
        center = [60, 60]
        poles = 4
        pole_length = 25
        pole_width = 20
        stator_radius = 60
        stator_width = 10
        smoothing = 1.3
        angle = (360 / poles) / smoothing
        rotor_radius = 25
        rotor_bore = 6
        coil_width = 8
        coil_length = 16
        coil_angle = 45
        coil_gap = 0.5

        # Draw the stator.
        stator_points = [
            [center[0] - (pole_width / 2), (stator_radius * 2) - stator_width],
            [center[0] - (pole_width / 2), (stator_radius * 2) - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), (stator_radius * 2) - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), (stator_radius * 2) - stator_width],
        ]
        self.session.pre.draw_circle(points=[center], radius=stator_radius, group=1)
        stator_pattern_points = self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_line, {
                'points': [stator_points[0], stator_points[1]],
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[2], stator_points[1]],
                'angle': coil_angle,
                'max_seg': 60,
                'group': 1,
            }],
            [self.session.pre.draw_line, {'points': [stator_points[2], stator_points[3]]}],
        ], center=center, repeat=poles)
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_arc, {
                'points': [stator_pattern_points[0][0][0], stator_pattern_points[2][1][1]],
                'angle': angle,
                'max_seg': 60,
                'group': 1,
            }],
        ], center=center, repeat=poles)
        self.session.pre.add_block_label(points=[[60, 115]])
        self.session.pre.select_label(points=[[60, 115]])
        self.session.pre.get_material('Air')
        self.session.pre.set_block_prop(
            block_name='Air',
            group=1,
        )
        self.session.pre.clear_selected()

        # Draw the coils.
        positive_coil_points = [
            [center[0] - (pole_width / 2) - coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) + (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_width - coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] - (pole_width / 2) - coil_width - coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) + (coil_length / 2))],
        ]
        negative_coil_points = [
            [center[0] + (pole_width / 2) + coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) + (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_width + coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) - (coil_length / 2))],
            [center[0] + (pole_width / 2) + coil_width + coil_gap, (stator_radius * 2) - (stator_width + (pole_length / 2) + (coil_length / 2))],
        ]
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_polygon, {'points': positive_coil_points}],
            [self.session.pre.draw_polygon, {'points': negative_coil_points}],
        ], center=center, repeat=poles)

        # Draw the bearing rotor.
        self.session.pre.draw_annulus(points=[center], inner_radius=rotor_bore, outer_radius=rotor_radius, max_seg=60)

        # Set the properties of the rotor.
        self.session.pre.add_block_label(points=[[60, 75]])
        self.session.pre.select_label(points=[[60, 75]])
        # self.session.pre.delete_selected_labels()
        self.session.pre.set_block_prop(
            block_name='Air',
            auto_mesh=True,
            mesh_size=1,
            in_circuit=None,
            mag_direction=0,
            group=1,
            turns=100,
        )
        self.session.pre.clear_selected()

        self.session.pre.save_as('test.fem')
        # self.session.pre.create_mesh()
        # self.session.pre.show_mesh()

        self.session.pre.make_abc()

        # Refit the view window.
        self.session.pre.zoom_natural()

    def post(self):
        pass
