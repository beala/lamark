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
                ast.append(lmast.Markdown(acc))
                acc = ""
                current_args = token.raw_match
                continue

            if isinstance(token, lexertokens.LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(lmast.Latex(acc, current_args))
                acc = ""
                current_args = ""
                continue

            if isinstance(token, lexertokens.OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                continue

        if len(ast) > 0 and isinstance(ast[-1], lmast.Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = lmast.Markdown((str(ast[-1]) + acc))
        else:
            # Otherwise, add a final md node to the AST
            ast.append(lmast.Markdown(acc))

        return ast

    def parse2(self, token_stream):
        ast = []
        stream_obj = TokenStream(token_stream)
        _parse_start(stream_obj, ast)

    def _parse_start(token_stream, ast):
        if isinstance(token_stream.cur(), lexertokens.LSTART):
            token_stream.consume()
            self._parse_latex(token_stream, ast)
        elif isinstance(token_stream.cur(), lexertokens.OTHER):
            other_tok = token_stream.consume()
            ast.append(lmast.Markdown(str(other_tok)))
            self_parse_
        else:
            raise LaMarkSyntaxError(
                    "Unexpected symbol: " + str(token_stream.cur()))

    def _parse_latex(token_stream, ast):
        pass

class LaMarkSyntaxError(Exception):
    def __init__(self, msg, line, col):
        self.msg = msg
        self.line = line
        self.col = col

    def __str__(self):
        return "Syntax Error: " + str(self.msg)


class TokenStream(object):
    def __init__(self, token_stream):
        self._token_stream = token_stream
        self._current_index = 0

    def consume(self):
        try:
            cur_token = self._token_stream[self._current_index]
        except IndexError:
            raise StopIteration
        self._current_index += 1
        return cur_token

    def cur(self):
        try:
            return self._token_stream[self._current_index]
        except:
            raise StopIteration

    def peek(self):
        return self._token_stream[self._current_index + 1]

