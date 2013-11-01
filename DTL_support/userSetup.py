import os
import sys
import site
import maya.cmds as cmds

site.addsitedir(os.path.join(cmds.internalVar(uad=True), 'scripts'))