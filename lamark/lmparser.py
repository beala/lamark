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
        acc_lineno = 0
        last_escaped = False
        current_args = ""
        tag_counter = 0
        #for token in token_stream:
        for token in token_stream:
            if last_escaped:
                # If last token was an escape
                last_escaped = False
                if (
                        isinstance(token, lexertokens.BIN_START) or
                        isinstance(token, lexertokens.BIN_END) or
                        isinstance(token, lexertokens.UNARY_TAG)):
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

            if isinstance(token, lexertokens.BIN_START):
                # Beginning of binary section. Last section must have been
                # markdown. Add md node to AST, if there's something in acc.
                tag_counter = self._count_tag_check(token_stream, tag_counter)
                self.last_bin_start_lineno=token.lineno
                if acc:
                    ast.append(lmast.Markdown(acc, token.lineno))
                    acc = ""
                current_args = token.raw_match
                self._expect(
                        [lexertokens.ESCAPE, lexertokens.OTHER,
                            lexertokens.BIN_END],
                        token_stream
                        )
                continue

            if isinstance(token, lexertokens.BIN_END):
                # End of binary tag section. Add binary node to AST
                tag_counter = self._count_tag_check(token_stream, tag_counter)
                ast.append(lmast.Latex(
                    acc,
                    self.last_bin_start_lineno,
                    current_args))
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
                            lexertokens.BIN_END,
                            lexertokens.BIN_START],
                        token_stream
                        )
                continue

        if acc:
            #If tokens left in acc
            if len(ast) > 0 and isinstance(ast[-1], lmast.Markdown):
                # If the last node is md, merge the remainder in the accumulator
                # into the last node.
                ast[-1] = lmast.Markdown((str(ast[-1]) + acc), ast[-1].lineno)
            else:
                # Otherwise, add a final md node to the AST
                ast.append(lmast.Markdown(acc, acc_lineno))

        if tag_counter != 0:
            # Check to make sure every BIN_START has an BIN_END
            raise lamarksyntaxerror.LaMarkSyntaxError(
                    "Unexpected end of file. Missing end tag.")

        return ast

    def _expect(self, valid_tokens, token_stream):
        """Looks ahead to the next token to make sure it's one of
        the valid_tokens. Otherwise, throws a SyntaxError
        """
        try:
            if token_stream.peek_ahead().__class__ not in valid_tokens:
                raise lamarksyntaxerror.LaMarkSyntaxError(
                        "Unexpected token: %s" % str(
                            token_stream.peek_ahead()),
                        token_stream.peek_ahead().lineno)
        except StopIteration:
            pass

    def _count_tag_check(self, token_stream, tag_counter):
        """Count the number of start and end tags. Throw an error if
        binary tags are nested.
        """
        if isinstance(token_stream.current(), lexertokens.BIN_START):
            if tag_counter > 0:
                raise lamarksyntaxerror.LaMarkSyntaxError(
                        "Unexpected start tag.",
                        token_stream.current().lineno)
            tag_counter += 1
        elif isinstance(token_stream.current(), lexertokens.BIN_END):
            if tag_counter < 1:
                raise lamarksyntaxerror.LaMarkSyntaxError(
                        "Unexpected end tag.",
                        token_stream.current().lineno)
            tag_counter -= 1
        elif isinstance(token_stream.current(), lexertokens.UNARY_TAG):
            if tag_counter != 0:
                raise lamarksyntaxerror.LaMarkSyntaxError(
                        "Unexpected unary tag.",
                        token_stream().lineno)
        return tag_counter

