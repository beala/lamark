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

    def get_children(self):
        return []

    def set_children(self, children):
        pass

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

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children

class UnaryTag(object):
    def __init__(self, lineno, raw_tag, args=[], kwargs={}):
        self.args = args
        self.kwargs = kwargs
        self.lineno = lineno
        self.raw_tag = raw_tag

    def __repr__(self):
        return "UnaryTag(%d, %s, %s)" % (
                self.lineno,
                repr(self.args),
                repr(self.kwargs)
                )

    def __str__(self):
        return repr(self)

    def get_contents(self):
        return [self.args, self.kwargs]

    def get_children(self):
        return []

    def set_children(self, children):
        pass

class Str(object):
    def __init__(self, string, lineno):
        self.string = string
        self.lineno = lineno

    def __repr__(self):
        return "Str(%s, %d)" % (repr(self.string), self.lineno)

    def __str__(self):
        return str(self.string)

    def get_children(self):
        return []

    def set_children(self, children):
        pass

class Document(object):
    def __init__(self, doc):
        self.doc = doc

    def __repr__(self):
        return "Document(%s)" % repr(self.doc)

    def __str__(self):
        return repr(self)

    def get_children(self):
        return self.doc

    def set_children(self, children):
        self.doc = children

def dump(ast):
    """Prints a LaMark AST as a string."""
    return repr(ast)

def map_postorder(lamark_ast, visit_func):
    """Maps a function over a LaMark AST. The visit_func takes in one node
       and returns a node. The returned node replaces the original node in
       the AST. Returning None leaves the node unchanged.
    """
    new_children = []
    for node in lamark_ast.get_children():
        new_child = map_postorder(node, visit_func)
        if new_child is not None:
            new_children.append(new_child)
    lamark_ast.set_children(new_children)
    return visit_func(lamark_ast)
