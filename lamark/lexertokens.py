class token(object):
    pass

class LSTART(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "LSTART(%s, %d)" % (self.raw_match, self.lineno)

    def __str__(self):
        return self.raw_match

class LEND(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "LEND(%s, %d)" % (self.raw_match, self.lineno)

    def __str__(self):
        return self.raw_match

class ESCAPE(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "ESCAPE(%s, %d)" % (repr(self.raw_match), self.lineno)

    def __str__(self):
        return self.raw_match

class OTHER(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "OTHER(%s, %d)" % (repr(self.raw_match), self.lineno)

    def __str__(self):
        return self.raw_match
