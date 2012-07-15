import lexertokens
import lmast
import lmlexer
import tokenstream
import lamarksyntaxerror

class LmParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, token_stream):
        ast = []
        acc = ""
        last_escaped = False
        current_args = ""
        #for token in token_stream:
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
                    acc += lmlexer.t_ESCAPE + str(token)
                continue

            if isinstance(token, lexertokens.ESCAPE):
                last_escaped = True
                continue

            if isinstance(token, lexertokens.LSTART):
                # Beginning of Latex section. Last section must have been
                # markdown. Add md node to AST
                ast.append(lmast.Markdown(acc, token.lineno))
                acc = ""
                current_args = token.raw_match
                self._expect(
                        [lexertokens.ESCAPE, lexertokens.OTHER],
                        token_stream
                        )
                continue

            if isinstance(token, lexertokens.LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(lmast.Latex(acc, token.lineno, current_args))
                acc = ""
                current_args = ""
                self._expect(
                        [lexertokens.ESCAPE, lexertokens.OTHER],
                        token_stream
                        )
                continue

            if isinstance(token, lexertokens.OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                # Save lineno for when it get flushed
                acc_lineno = token.lineno
                self._expect(
                        [lexertokens.ESCAPE,
                            lexertokens.LEND,
                            lexertokens.LSTART],
                        token_stream
                        )
                continue

        if len(ast) > 0 and isinstance(ast[-1], lmast.Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = lmast.Markdown((str(ast[-1]) + acc), ast[-1].lineno)
        else:
            # Otherwise, add a final md node to the AST
            ast.append(lmast.Markdown(acc, acc_lineno))

        return ast

    def _expect(self, valid_tokens, token_stream):
        """Looks ahead to the next token to make sure it's one of
        the valid_tokens. Otherwise, throws a SyntaxError
        """
        try:
            if token_stream.peek_ahead().__class__ not in valid_tokens:
                raise lamarksyntaxerror.LaMarkSyntaxError(
                        "Unexpected token: %s" % repr(
                            token_stream.peek_ahead().raw_match),
                        token_stream.peek_ahead().lineno)
        except StopIteration:
            # Reached end of token stream
            pass
