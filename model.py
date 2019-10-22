from run import BaseRunner


class Runner(BaseRunner):

    def pre(self, rotor_center=None):
        self.session.new_document(0)

        # Define the problem.
        self.session.pre.problem_definition(
            frequency=0,
            units='millimeters',
            problem_type='planar',
            precision=1e-8,
            depth=20,
        )

        # Define/get materials.
        self.session.pre.add_material('Somaloy', material_data={
            'mu_x': 430,
            'h_c': 210,
            'number_of_strands': 1,
            'c_duct': (1 / 300e-8)
        })
        self.session.pre.get_material('1006 Steel')
        self.session.pre.get_material('Air')
        self.session.pre.get_material('1mm')

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
        rotor_center = rotor_center or center
        coil_width = 5
        coil_length = 16
        coil_angle = 45
        coil_gap = 0.5

        # Set the air regions.
        self.session.pre.add_block_label(points=[[60, 130]])
        self.session.pre.select_label(points=[[60, 130]])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        self.session.pre.add_block_label(points=[center])
        self.session.pre.select_label(points=[center])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        self.session.pre.add_block_label(points=[[40, 100]])
        self.session.pre.select_label(points=[[40, 100]])
        self.session.pre.set_block_prop(block_name='Air', group=1)
        self.session.pre.clear_selected()

        # Draw the stator.
        stator_points = [
            [center[0] - (pole_width / 2), (stator_radius * 2) - stator_width],
            [center[0] - (pole_width / 2), (stator_radius * 2) - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), (stator_radius * 2) - (stator_width + pole_length)],
            [center[0] + (pole_width / 2), (stator_radius * 2) - stator_width],
        ]
        self.session.pre.draw_circle(points=[center], radius=stator_radius, max_seg=1, group=1)
        stator_pattern_points = self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_line, {
                'points': [stator_points[0], stator_points[1]],
                'group': 1,
            }],
            [self.session.pre.draw_arc, {
                'points': [stator_points[2], stator_points[1]],
                'angle': coil_angle,
                'max_seg': 1,
                'group': 1,
            }],
            [self.session.pre.draw_line, {
                'points': [stator_points[2], stator_points[3]],
            }],
        ], center=center, repeat=poles)
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.draw_arc, {
                'points': [stator_pattern_points[0][0][0], stator_pattern_points[2][1][1]],
                'angle': angle,
                'max_seg': 1,
                'group': 1,
            }],
        ], center=center, repeat=poles)
        self.session.pre.add_block_label(points=[[60, 115]])
        self.session.pre.select_label(points=[[60, 115]])
        self.session.pre.set_block_prop(
            block_name='1006 Steel',
            auto_mesh=True,
            mesh_size=1,
            in_circuit=None,
            mag_direction=0,
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
        self.session.pre.draw_pattern(commands=[
            [self.session.pre.add_block_label, {
                'points': [[45, 95]],
                'block_name': '1mm',
                'in_circuit': 'winding_{i}',
                'turns': 100,
            }],
            [self.session.pre.add_block_label, {
                'points': [[75, 95]],
                'block_name': '1mm',
                'in_circuit': 'winding_{i}',
                'turns': -100,
            }],
        ], center=center, repeat=poles)

        # Draw the bearing rotor.
        self.session.pre.draw_annulus(points=[rotor_center], inner_radius=rotor_bore, outer_radius=rotor_radius,
                                      max_seg=1, group=2)

        # Set the properties of the rotor.
        self.session.pre.add_block_label(points=[[60, 75]])
        self.session.pre.select_label(points=[[60, 75]])
        self.session.pre.set_block_prop(
            block_name='1006 Steel',
            auto_mesh=True,
            mesh_size=1,
            in_circuit=None,
            mag_direction=0,
            group=2,
        )
        self.session.pre.clear_selected()

        # Set winding currents.
        self.session.pre.add_circuit_prop(circuit_name='winding_1', current=10, circuit_type='series')
        for i in range(poles - 1):
            self.session.pre.add_circuit_prop(circuit_name=f'winding_{i+2}', current=0, circuit_type='series')

        self.session.pre.save_as('test.fem')
        self.session.pre.make_abc()
        self.session.pre.create_mesh()

        # Refit the view window.
        self.session.pre.zoom_natural()

    def solve(self):
        self.session.pre.analyze()
        self.session.pre.zoom_natural()
        self.session.pre.load_solution()
        self.session.post.show_density_plot(plot_type='bmag')

    def post(self):
        self.session.post.group_select_block(group='2')
        force_y = self.session.post.block_integral(19)
        return force_y
