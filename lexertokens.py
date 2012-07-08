class token(object):
    pass

class LSTART(token):
    def __init__(self, raw_match):
        self.raw_match = raw_match

    def __repr__(self):
        return "LSTART(%s)" % self.raw_match

    def __str__(self):
        return self.raw_match

class LEND(token):
    def __init__(self, raw_match):
        self.raw_match = raw_match

    def __repr__(self):
        return "LEND(%s)" % self.raw_match

    def __str__(self):
        return self.raw_match

class ESCAPE(token):
    def __repr__(self):
        return "ESCAPE()"

    def __str__(self):
        return '\\'

class OTHER(token):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "OTHER(%s)" % repr(self.string)

    def __str__(self):
        return self.string
