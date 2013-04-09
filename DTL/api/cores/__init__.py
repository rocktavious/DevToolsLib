"""
Selects the appropreate core for the environment you are running in
"""
Core = None

# initialize the system for Maya
try:
	from .maya.core import MayaCore as Core
except:
	pass

# initialize the system for 3d Studio Max
try:
	from .studiomax.core import StudioMaxCore as Core
except:
	pass

# initialize the system for Motion Builder
try:
	from .motionbuilder.core import MotionBuilderCore as Core
except:
	pass

# initialize the system for Standalone
if Core is None:
	from .external import Core
