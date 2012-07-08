import mdast
import latexgen

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.args = args
        pass

    def generate(self, matex_ast):
        pure_md_acc = ""
        with latexgen.LatexGen(self.args) as lg:
            for node in matex_ast:
                if isinstance(node, mdast.Markdown):
                    pure_md_acc += str(node)
                elif isinstance(node, mdast.Latex):
                    pure_md_acc += str(lg.generate(str(node), node.args))
            return pure_md_acc

