class Markdown(object):
    def __init__(self, string, lineno):
        self.string = string
        self.lineno = lineno

    def __repr__(self):
        return "Markdown(%s, %d)" % (repr(self.string), self.lineno)

    def __str__(self):
        return str(self.string)

class BinTag(object):
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
        return str(self.string)

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

class RefItem(object):
    """Node for a reference item. This contains the contents of one
       footnote.
    """
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "RefBody(%s)" % repr(self.text)

    def __str__(self):
        return str(self.text)

class RefFooter(object):
    """For the reference footer. This is the placeholder for where the
       references will be placed in the processed text.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return "RefFooter()"

    def __str__(self):
        return ""
