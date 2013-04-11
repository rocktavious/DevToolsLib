commands = {}
aliases = {}

def command(meth):
    global commands, aliases
    assert meth.__doc__, "Command {0} needs properly formatted docstrings.".format(meth)
    if hasattr(meth, 'im_func'): # bound method, if we ever have one
        meth = meth.im_func
    commands[meth.func_name] = meth
    meth_aliases = [unicode(alias) for alias in aliases.iterkeys() if aliases[alias].func_name == meth.func_name]
    if meth_aliases:
        meth.__doc__ += u"\nAliases: %s" % ",".join(meth_aliases)
    return meth

def alias(name):
    def decorator(meth):
        global commands, aliases
        assert name not in commands, "This alias is the name of a command."
        aliases[name] = meth
        return meth
    return decorator

import utils