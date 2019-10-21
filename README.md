# Python Framework for FEMM (currently Windows only)

Work in progress, commands are being added as the wrapper is used,
therefore not all commands have been wrapped.

```python
from wrapper import FEMMSession
# The FEMM window will open when a FEMMSession is instantiated.
femm = FEMMSession()

# Create a new magnetics document. You can use either the
# number code or the more verbose doctype (not case sensitive):
#
#   0 --> 'magnetics'
#   1 --> 'electrostatics'
#   2 --> 'heat'
#   3 --> 'current'
#
# This will automatically setup the FEMMSession to work in the
# magnetics mode by prefixing all commands with 'm'.
femm.new_documemt(0)

# Now we can run preprocessor or postprocessor commands like so:
femm.pre.add_node(5, 5)
femm.post.line_integral('integral_type')
```

All that this wrapper does is make sure to append the correct mode 
prefix to all the commands when calling FEMM. For example `mi_` is the
prefix for any magnetics preprocessor command and `eo_` is the prefix for
any electrostatics postprocessor command.

All command names are the same as shown in the FEMM manual with the
exception of correct Python naming. For example `addnode` becomes `add_node`.
Under the hood the `mlab2femm` command is used so any Python to Matlab syntax
is handled when passing through arguments.
