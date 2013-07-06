__all__=['InternalError']

class InternalError(Exception):
    """
    General framework (non-application) related errors.
    
    :param msg: The error message.
    """
    def __init__(self, msg='Internal API Error'):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
    
class DeprecatedError(InternalError):
    """
    General framework deprecation error.
    """
    
    def __str__(self):
        return "Deprecated"
    