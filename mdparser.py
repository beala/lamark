import lexertokens
import mdast
import mdlexer

class MdParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, token_stream):
        ast = []
        acc = ""
        last_escaped = False
        current_args = ""
        for token in token_stream:
            if last_escaped:
                # If last token was an escape
                last_escaped = False
                if (
                        isinstance(token, lexertokens.LSTART) or
                        isinstance(token, lexertokens.LEND)):
                    # If you've escaped a start/end latex tag, then only
                    # keep the tag.
                    acc += str(token)
                else:
                    # Otherwise, keep both.
                    acc += mdlexer.t_ESCAPE + str(token)
                continue

            if isinstance(token, lexertokens.ESCAPE):
                last_escaped = True
                continue

            if isinstance(token, lexertokens.LSTART):
                # Beginning of Latex section. Last section must have been
                # markdown. Add md node to AST
                ast.append(mdast.Markdown(acc))
                acc = ""
                current_args = token.raw_match
                continue

            if isinstance(token, lexertokens.LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(mdast.Latex(acc, current_args))
                acc = ""
                current_args = ""
                continue

            if isinstance(token, lexertokens.OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                continue

        if len(ast) > 0 and isinstance(ast[-1], mdast.Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = mdast.Markdown((str(ast[-1]) + acc))
        else:
            # Otherwise, add a final md node to the AST
            ast.append(mdast.Markdown(acc))

        return ast
