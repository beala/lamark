import lexertokens
import lmast
import lmlexer

class LmParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, token_stream):
        ast = []
        acc = ""
        last_escaped = False
        current_args = ""
        #for token in token_stream:
        self.token_stream_gen = TokenStream(token_stream)
        for token in self.token_stream_gen:
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
                ast.append(lmast.Markdown(acc))
                acc = ""
                current_args = token.raw_match
                self._expect(
                        [lexertokens.ESCAPE, lexertokens.OTHER],
                        token_stream,
                        "Expected either escape char or Markdown"
                        )
                continue

            if isinstance(token, lexertokens.LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(lmast.Latex(acc, current_args))
                acc = ""
                current_args = ""
                self._expect(
                        [lexertokens.ESCAPE, lexertokens.OTHER],
                        token_stream,
                        "Expected either escape char or Markdown"
                        )
                continue

            if isinstance(token, lexertokens.OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                self._expect(
                        [lexertokens.ESCAPE,
                            lexertokens.LEND,
                            lexertokens.LSTART],
                        token_stream,
                        "Expected either escape char, latex end, or latex start"
                        )
                continue

        if len(ast) > 0 and isinstance(ast[-1], lmast.Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = lmast.Markdown((str(ast[-1]) + acc))
        else:
            # Otherwise, add a final md node to the AST
            ast.append(lmast.Markdown(acc))

        return ast

    def _expect(self, valid_tokens, token_stream, error_msg):
        try:
            if self.token_stream_gen.current().__class__ not in valid_tokens:
                raise LaMarkSyntaxError(
                        error_msg,
                        self.token_stream_gen.current().lineno)
        except StopIteration:
            pass

class LaMarkSyntaxError(Exception):
    def __init__(self, msg, line):
        self.msg = msg
        self.line = line

    def __str__(self):
        return "Syntax Error on line %d: %s" % (self.line, self.msg)


class TokenStream(object):
    def __init__(self, token_stream):
        self._token_stream = token_stream
        self._current_index = 0

    def __iter__(self):
        return self

    def next(self):
        try:
            cur_token = self._token_stream[self._current_index]
        except IndexError:
            raise StopIteration
        self._current_index += 1
        return cur_token

    def current(self):
        try:
            return self._token_stream[self._current_index]
        except:
            raise StopIteration

    def peek_ahead(self):
        return self._token_stream[self._current_index + 1]

