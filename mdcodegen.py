import mdast
import latexgen

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.output_fn = args.OUTPUT_FILE
        self.lg = latexgen.LatexGen(args)


    def generate(self, matex_ast):
        pure_md_acc = ""
        for node in matex_ast:
            if isinstance(node, mdast.Markdown):
                pure_md_acc += str(node)
            elif isinstance(node, mdast.Latex):
                pure_md_acc += str(self.lg.generate(str(node), node.args))
        return pure_md_acc

