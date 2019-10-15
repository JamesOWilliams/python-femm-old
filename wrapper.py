import os
import win32com.client

DOCTYPE_MAPPING = {
    'magnetics': 1,
    'electrostatics': 2,
    'heat': 3,
    'current': 4,
}

DOCTYPE_PREFIX_MAPPING = {
    0: 'm',
    'magnetics': 'm',
    1: 'e',
    'electrostatics': 'e',
    2: 'h',
    'heat': 'h',
    3: 'c',
    'current': 'c',
}

PREFIX_DOCTYPE_MAPPING = {
    'm': 'magnetics',
    'e': 'electrostatics',
    'h': 'heat',
    'c': 'current',
}


class FEMMSession:
    """A simple wrapper around FEMM 4.2."""

    doctype_prefix = None

    def __init__(self):
        self.__to_femm = win32com.client.Dispatch('femm.ActiveFEMM')
        self.set_current_directory()
        self.pre = PreprocessorAPI(self)
        self.post = PostProcessorAPI(self)

    def _add_doctype_prefix(self, string):
        return self.doctype_prefix + string

    def call_femm(self, string):
        """Call a given command string using ``mlab2femm``."""

        res = self.__to_femm.mlab2femm(string)
        if len(res) == 0:
            res = []
        elif res[0] == 'e':
            raise Exception(res)
        else:
            res = eval(res)
        if len(res) == 1:
            res = res[0]
        return res

    def call_femm_noeval(self, string):
        """Call a given command string using ``mlab2femm`` without eval."""

        self.__to_femm(string)

    def call_femm_with_args(self, command, *args, add_doctype_prefix=True):
        """Call a given command string using ``mlab2femm`` and parse the args."""

        if add_doctype_prefix:
            return self.call_femm(self._add_doctype_prefix(command) + self._parse_args(args))
        return self.call_femm(command + self._parse_args(args))

    @staticmethod
    def _fix_path(path):
        """Replace \\ and // with a single forward slash."""

        return path.replace('\\', '/').replace('//', '/')

    @staticmethod
    def _parse_args(args):
        """Convert each argument into a string and then join them by commas."""

        args_string = ', '.join(map(lambda arg: f'"{arg}"' if isinstance(arg, str) else str(arg), args))
        return f'({args_string})'

    @staticmethod
    def _quote(string):
        return f'"{string}"'

    def set_current_directory(self):
        """Set the current working directory using ``os.getcmd()``."""

        path_of_current_directory = self._fix_path(os.getcwd())
        self.call_femm(f'setcurrentdirectory({self._quote(path_of_current_directory)})')

    def new_document(self, doctype):
        """Creates a new preprocessor document and opens up a new preprocessor window. Specify doctype
        to be 0 for a magnetics problem, 1 for an electrostatics problem, 2 for a heat flow problem,
        or 3 for a current flow problem. An alternative syntax for this command is create(doctype)."""

        mode = DOCTYPE_MAPPING[doctype] if isinstance(doctype, str) else doctype
        self.call_femm(f'newdocument({mode})')
        self.set_mode(mode)

    def close(self):
        """Close all documents and exit the the Interactive Shell at the end of
        the currently executing Lua script."""

        self.call_femm('quit()')

    def set_mode(self, doctype):
        self.doctype_prefix = DOCTYPE_PREFIX_MAPPING[doctype]

    @property
    def mode(self):
        return PREFIX_DOCTYPE_MAPPING[self.doctype_prefix]


class BaseAPI:

    mode_prefix = None

    def __init__(self, session):
        self.session = session

    def _add_mode_prefix(self, string):
        return f'{self.mode_prefix}_{string}'

    def _call_femm(self, string):
        return self.session.call_femm(self._add_mode_prefix(string))

    def _call_femm_with_args(self, string, *args):
        return self.session.call_femm_with_args(self._add_mode_prefix(string), *args)


class PreprocessorAPI(BaseAPI):
    """Preprocessor API"""

    mode_prefix = 'i'

    def add_node(self, x, y):
        """Add a new node at x, y."""

        self._call_femm_with_args('addnode', x, y)

    def add_segment(self, x1, y1, x2, y2):
        """Add a new line segment from node closest to (x1, y1) to node closest to (x2, y2)."""

        self._call_femm_with_args('addsegment', x1, y1, x2, y2)

    def add_block_label(self, x, y):
        """Add a new block label at (x, y)."""

        self._call_femm_with_args('addblocklabel', x, y)

    def add_arc(self, x1, y1, x2, y2, angle, max_seg):
        """Add a new arc segment from the nearest node to (x1, y1) to the nearest node to
        (x2, y2) with angle ‘angle’ divided into ‘max_seg’ segments"""

        self._call_femm_with_args('add_arc', x1, y1, x2, y2, angle, max_seg)

    def delete_selected(self):
        """Delete all selected objects."""

        self._call_femm('deleteselected')

    def delete_selected_nodes(self):
        """Delete selected nodes."""

        self._call_femm('deleteselectednodes')

    def delete_selected_labels(self):
        """Delete selected labels."""

        self._call_femm('deleteselectedlabels')

    def delete_selected_segments(self):
        """Delete selected segments."""

        self._call_femm('deleteselectedsegments')

    def delete_selected_arc_segments(self):
        """Delete selected arc segments."""

        self._call_femm('deleteselectedarcsegments')


class PostProcessorAPI(BaseAPI):
    """Postprocessor API"""

    mode_prefix = 'o'

    def line_integral(self, integral_type):
        """Calculate the line integral for the defined contour. Returns typically two (possibly
        complex) values as results. For force and torque results, the 2× results are only relevant
        for problems where ω 6= 0. The 1× results are only relevant for incremental permeability
        AC problems. The 1× results represent the force and torque interactions between the
        steady-state and the incremental AC solution"""

        self._call_femm_with_args('lineintegral', integral_type)

    def block_integral(self, integral_type):
        """Calculate a block integral for the selected blocks. This function returns one
        (possibly complex) value, e.g.: volume = mo blockintegral(10)."""

        self._call_femm_with_args('blockintegral', integral_type)

    def get_point_values(self, x, y):
        """Get the values associated with the point at x,y return values in order"""

        self._call_femm_with_args('getpointvalues', x, y)
