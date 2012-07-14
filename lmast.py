class Markdown(object):
    def __init__(self, string, lineno):
        self.string = string
        self.lineno = lineno

    def __repr__(self):
        return "Markdown(%s, %d)" % (repr(self.string), self.lineno)

    def __str__(self):
        return str(self.string)

class Latex(object):
    def __init__(self, string, lineno, args, kwargs={}):
        self.string = string
        self.args = args
        self.kwargs = kwargs
        self.lineno = lineno

    def __repr__(self):
        return "Latex(%s, %d, %s, %s)" % (
                repr(self.string),
                self.lineno,
                repr(self.args),
                repr(self.kwargs)
                )

    def __str__(self):
        return self.string
