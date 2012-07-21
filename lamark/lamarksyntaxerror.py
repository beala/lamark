class LaMarkSyntaxError(Exception):
    """Raised when a syntax error is encountered in a LaMark file
    """
    def __init__(self, msg, lineno=None):
        """msg: Error message
        lineno: Line number syntax error occurs on
        """
        self.msg = msg
        self.lineno = lineno

    def __str__(self):
        if self.lineno:
            return "Syntax Error on line %d: %s" % (int(self.lineno),
                    str(self.msg))
        return "Syntax Error: %s" % str(self.msg)

    def __repr__(self):
        return self.__str__()
