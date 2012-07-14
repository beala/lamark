class LaMarkArgumentError(Exception):
    def __init__(self, msg, lineno):
        self.msg = msg
        self.lineno = lineno

    def __str__(self):
        return "Argument error in tag beginning on line %d: %s" % (
                self.lineno, self.msg)
