import argparse

class MdLexer(object):
    t_LSTART = "#@"
    t_LEND = "@#"
    t_ESCAPE = "\\"

    def __init__(self, args):
        self.args = args

    def lex(self, string):
        # Contains the string position that needs to be fast-fowarded to.
        ff = 0
        # The token string. Nodes get appended to this.
        t_stream = []
        # The catch-all accumulator.
        other_acc = ""
        # These test the string for a token.
        tests = [
                self._test_escape,
                self._test_lstart,
                self._test_lend,
                ]
        for i in xrange(len(string)):
            # Fast forward `i` to `ff`
            if i < ff:
                continue
            # Run all the token tests at the current position
            for test in tests:
                (ff, node) = test(string, i)
                # If a test accepts the string then
                # ff will be set to where the test stopped
                # accepting.
                if i < ff:
                    # Flush the `other_acc` into the `t_stream`
                    if other_acc:
                        t_stream.append(OTHER(other_acc))
                        other_acc = ""
                    # Append the node returned by the test onto the `t_stream`
                    t_stream.append(node)
                    # Break, because a test has accepted the string
                    break
            # If no test accepted the string, so add the current character
            # onto the catch-all `other_acc`
            if i >= ff:
                other_acc += string[i]

        # Flush the `other_acc` if it contains anything.
        if other_acc:
            t_stream.append(OTHER(other_acc))

        return t_stream

    def _test_lstart(self, string, n):
        if string[n:n+len(self.t_LSTART)] == self.t_LSTART:
            return (n+len(self.t_LSTART), LSTART())
        else:
            return (n, None)

    def _test_lend(self, string, n):
        if string[n:n+len(self.t_LEND)] == self.t_LEND:
            return (n+len(self.t_LEND), LEND())
        else:
            return (n, None)

    def _test_escape(self, string, n):
        if string[n:n+len(self.t_ESCAPE)] == self.t_ESCAPE:
            return (n+len(self.t_ESCAPE), ESCAPE())
        else:
            return (n, None)

class token(object):
    pass

class LSTART(token):
    def __repr__(self):
        return "LSTART()"

    def __str__(self):
        return MdLexer.t_LSTART

class LEND(token):
    def __repr__(self):
        return "LEND()"

    def __str__(self):
        return MdLexer.t_LEND

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

class MdParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, token_stream):
        ast = []
        acc = ""
        last_escaped = False
        for token in token_stream:
            if last_escaped:
                # If last token was escape, add the escape
                # plus the current token to the accumulator
                last_escaped = False
                acc += MdLexer.t_ESCAPE + str(token)
                continue

            if isinstance(token, ESCAPE):
                last_escaped = True
                continue

            if isinstance(token, LSTART):
                # Beginning of Latex section. Last section must have been
                # markdown. Add md node to AST
                ast.append(Markdown(acc))
                acc = ""
                continue

            if isinstance(token, LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(Latex(acc))
                acc = ""
                continue

            if isinstance(token, OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                continue

        if isinstance(ast[-1], Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = Markdown((str(a[-1]) + acc))
        else:
            # Otherwise, add a final md node to the AST
            ast.append(Markdown(acc))

        return ast

class Markdown(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Markdown(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class Latex(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Latex(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.output_fn = args.OUTPUT_FILE
        self.lg = LatexGen(args)


    def generate(self, matex_ast):
        output_fd = open(self.output_fn, 'w')
        for node in matex_ast:
            if isinstance(node, Markdown):
                output_fd.write(str(node))
            elif isinstance(node, Latex):
                output_fd.write(self.lg.generate(str(node)))
        output_fd.close()


class LatexGen(object):
    """Given a peice of Latex, generate an image, and the markdown
        necessary to display the image.
    """
    def __init__(self, args):
        pass

    def generate(self, latex_string):
        return "![Dummy Image Alt Text](placeholder.png)"

def main():
    cli_parser = argparse.ArgumentParser(
            description="A LATEX processor for Markdown")
    cli_parser.add_argument("FILE")
    cli_parser.add_argument("OUTPUT_FILE")
    args = cli_parser.parse_args()

    l = MdLexer(args)
    token_stream = l.lex(open(args.FILE).read())
    print "Token stream:"
    print token_stream
    m = MdParser(args)
    ast = m.parse(token_stream)
    print "AST:"
    print ast
    mg = MdCodeGen(args)
    mg.generate(ast)

if __name__=="__main__":
    main()
