class Markdown(object):
    def __init__(self, string, lineno):
        self.string = string
        self.lineno = lineno

    def __repr__(self):
        return "Markdown(%s, %d)" % (repr(self.string), self.lineno)

    def __str__(self):
        return str(self.string)

    def get_contents(self):
        return str(self.string)

class BinTag(object):
    #def __init__(self, string, lineno, args, kwargs={}):
        #self.string = string
        #self.args = args
        #self.kwargs = kwargs
        #self.lineno = lineno

    def __init__(self, children, lineno, raw_tag, args=[], kwargs={}):
        self.children = children
        self.lineno = lineno
        self.raw_tag = raw_tag
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "BinTag(%s, %d, %s, %s)" % (
                repr(self.children),
                self.lineno,
                repr(self.args),
                repr(self.kwargs)
                )

    def __str__(self):
        return str(self.raw_tag)

    def get_contents(self):
        return self.children

class UnaryTag(object):
    def __init__(self, lineno, args, kwargs={}):
        self.args = args
        self.kwargs = kwargs
        self.lineno = lineno

    def __repr__(self):
        return "UnaryTag(%d, %s, %s)" % (
                self.lineno,
                repr(self.args),
                repr(self.kwargs)
                )

    def __str__(self):
        return ""

    def get_contents(self):
        return [self.args, self.kwargs]

class Str(object):
    def __init__(self, string, lineno):
        self.string = string
        self.lineno = lineno

    def __repr__(self):
        return "Str(%s, %d)" % (repr(self.string), self.lineno)

    def __str__(self):
        return str(self.string)

def dump(ast):
    return repr(ast)
