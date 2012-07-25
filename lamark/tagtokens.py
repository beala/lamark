class ARG(object):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "ARG(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class FUNC_NAME(object):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "FUNC_NAME(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class VALUE(object):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "VALUE(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class ASSIGN(object):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "ASSIGN(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)
