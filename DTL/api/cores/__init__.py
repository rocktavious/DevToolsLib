"""
Selects the appropreate core for the environment you are running in
"""

Core = None

# initialize the system for Maya
try:
	from .maya.core import MayaCore as Core
except:
	print "Maya Core Failed"
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
if not Core:
	from .external import Core

Core.instance()