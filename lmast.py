class Markdown(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Markdown(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class Latex(object):
    def __init__(self, string, args, kwargs={}):
        self.string = string
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "Latex(%s, %s, %s)" % (
                repr(self.args),
                repr(self.string),
                repr(self.kwargs)
                )

    def __str__(self):
        return self.string
