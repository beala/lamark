class token(object):
    pass

class BIN_START(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "BIN_START(%s, %d)" % (repr(self.raw_match), self.lineno)

    def __str__(self):
        return self.raw_match

class BIN_END(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "BIN_END(%s, %d)" % (repr(self.raw_match), self.lineno)

    def __str__(self):
        return self.raw_match

class UNARY_TAG(token):
    def __init__(self, raw_match, lineno):
        self.raw_match = raw_match
        self.lineno = lineno

    def __repr__(self):
        return "UNARY_TAG(%s, %d)" % (repr(self.raw_match), self.lineno)

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
