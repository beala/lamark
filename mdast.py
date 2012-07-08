class Markdown(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Markdown(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class Latex(object):
    def __init__(self, string, args):
        self.string = string
        self.args = args

    def __repr__(self):
        return "Latex(%s, %s)" % (repr(self.args), repr(self.string))

    def __str__(self):
        return self.string
