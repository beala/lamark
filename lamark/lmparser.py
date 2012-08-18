import lexertokens
import lmast
import lmlexer
import tokenstream
import lamarksyntaxerror

class LmParser(object):
    def __init__(self, args):
        self.args = args

    def parse(self, token_stream):
        """Parses a token stream of type tokenstream.TokenStream.
           Returns an AST (list) of nodes from 'lmast'.
        """
        token_gen = iter(token_stream)
        token_stack = []
        # Keeps track of if we're inside of a binary tag. Everytime we enter
        # a binary tag, we push into it, and when we exit, we pop.
        bin_tag_stack = []
        while True:
            try:
                cur_token = token_gen.next()
            except StopIteration:
                break
            if isinstance(cur_token, lexertokens.OTHER):
                # If we're inside a binary tag, then just leave it as an
                # OTHER token. The binary tag will take care of parsing it.
                if len(bin_tag_stack) > 0:
                    token_stack.append(cur_token)
                else:
                    token_stack.append(
                            lmast.Markdown(
                                str(cur_token),
                                cur_token.lineno)
                    )
            elif isinstance(cur_token, lexertokens.ESCAPE):
                # Peek ahead, and if the next token is a token that can be
                # escaped, pull it off the token stream, escape it, and
                # add it to the token_stack as a Markdown node.
                try:
                    next_tok = token_gen.next()
                except StopIteration:
                    next_tok = None
                if (
                        isinstance(next_tok, lexertokens.BIN_END) or
                        isinstance(next_tok, lexertokens.BIN_START) or
                        isinstance(next_tok, lexertokens.UNARY_TAG)):
                    #next_tok = token_gen.next()
                    escaped_tok = next_tok.raw_match
                elif isinstance(next_tok, lexertokens.OTHER):
                    # Next token isn't anything special. Just treat the escape
                    # as a backslash.
                    escaped_tok = "\\" + next_tok.raw_match
                else:
                    escaped_tok = "\\"
                # WARNING: This might break if we allow nested tags.
                if (
                        len(token_stack) > 0 and
                        isinstance(token_stack[-1], lmast.Markdown)):
                    # If the last node a Markdown node, just append to that.
                    token_stack[-1].string += escaped_tok
                else:
                    # Otherwise, make a new node.
                    token_stack.append(
                            lmast.Markdown(
                                escaped_tok,
                                cur_token.lineno)
                    )
            elif isinstance(cur_token, lexertokens.BIN_START):
                if len(bin_tag_stack) > 0:
                    raise lamarksyntaxerror.LaMarkSyntaxError(
                            "Error: Unexpected tag: '%s'" % str(cur_token),
                            cur_token.lineno)
                bin_tag_stack.append(cur_token)
                token_stack.append(cur_token)
            elif isinstance(cur_token, lexertokens.BIN_END):
                # Find where the last BIN_START was, so pop off the stack
                # and into the temp_stack, until it's found.
                temp_stack = []
                while True:
                    try:
                        old_tok = token_stack.pop()
                    except:
                        raise lamarksyntaxerror.LaMarkSyntaxError(
                                "Error: {%end%} tag has no matching start tag.",
                                cur_token.lineno)
                    temp_stack.append(old_tok)
                    if isinstance(old_tok, lexertokens.BIN_START):
                        break
                bin_start = temp_stack.pop()
                try:
                    bin_body = temp_stack.pop()
                except IndexError:
                    bin_body = lexertokens.OTHER("", bin_start.lineno)
                # Wrap everything in between in a BinTag AST node.
                token_stack.append(
                        lmast.BinTag(
                            str(bin_body),
                            bin_body.lineno,
                            str(bin_start)
                        )
                )
                bin_tag_stack.pop()
            elif isinstance(cur_token, lexertokens.UNARY_TAG):
                # Unary tags are easy. Just convert them in AST nodes.
                token_stack.append(
                        lmast.UnaryTag(
                        cur_token.lineno,
                        cur_token.raw_match)
                )
        if len(bin_tag_stack) > 0:
            raise lamarksyntaxerror.LaMarkSyntaxError(
                    "Error: Unexpected end of file. Where's the {%end%} tag?",
                    cur_token.lineno)
        # And then the stack is the AST. How cool is that?
        return token_stack
