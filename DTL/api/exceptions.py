__all__=['InternalError']

class InternalError(Exception):
    """
    General framework (non-application) related errors.
    
    :param msg: The error message.
    """
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg
    