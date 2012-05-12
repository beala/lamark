import argparse

class MdLexer(object):
    def lex(self, string):
        pass

class MdParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, string):
        ff = 0
        ast = []
        token = ""
        for n in xrange(len(string)):
            if n < ff:
                continue
            elif string[n] == "\\":
                token += string[n] + string[n+1]
                ff = n + 2
            elif string[n] == "@":
                maybe_latex = self.parse_latex(string, n+1)
                if maybe_latex != None:
                    (m, latex) = maybe_latex
                    ast += [Markdown(token)]
                    ast += [latex]
                    token =""
                else:
                    token += string[n]
            else:
                token += string[n]
        ast += [Markdown(token)]
        return ast

    def parse_latex(self, string, n):
        if string[n:n+2] != "la":
            return None
        token = ""
        ff = 0
        for n in xrange(n+2, len(string)):
            if n < ff:
                continue
            elif string[n] == "\\":
                token += string[n] + string[n+1]
                ff = n + 2
            elif string[n] == "@":
                return (n+1, Latex(token))
            else:
                token += string[n]

class Markdown(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Markdown(%s)" % repr(self.string)

class Latex(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Latex(%s)" % repr(self.string)

def main():
    cli_parser = argparse.ArgumentParser(
            description="A LATEX parser for Markdown")
    cli_parser.add_argument("FILE")
    args = cli_parser.parse_args()

    m = MdParser(args)
    print m.parse(open(args.FILE).read())

if __name__=="__main__":
    main()
