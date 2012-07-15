class LaMarkSyntaxError(Exception):
    """Raised when a syntax error is encountered in a LaMark file
    """
    def __init__(self, msg, lineno):
        """msg: Error message
        lineno: Line number syntax error occurs on
        """
        self.msg = msg
        self.lineno = lineno

    def __str__(self):
        return "Syntax Error on line %d: %s" % (self.lineno, self.msg)
