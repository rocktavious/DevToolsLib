Core = None

# initialize the system for Maya
try:
	from .maya import Core
except:
	pass

# initialize the system for 3d Studio Max
try:
	from .studiomax import Core
except:
	pass

# initialize the system for Motion Builder
try:
	from .motionbuilder import Core
except:
	pass

# initialize the system for Standalone
if ( not Core ):
	from .external import Core

Core.instance()