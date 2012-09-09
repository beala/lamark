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
                # If we're inside a binary tag, then use the Str node rather
                # than the Markdown tag, because text inside a bintag isn't
                # necessarily Markdown.
                if len(bin_tag_stack) > 0:
                    token_stack.append(
                            lmast.Str(
                                cur_token.raw_match,
                                cur_token.lineno)
                            )
                else:
                    token_stack.append(
                            lmast.Markdown(
                                str(cur_token),
                                cur_token.lineno)
                    )
            elif isinstance(cur_token, lexertokens.ESCAPE):
                # Get the next token and if the next token is one that can be
                # escaped, escape it, and add it to the token_stack.
                try:
                    next_tok = token_gen.next()
                except StopIteration:
                    next_tok = None
                if (
                        isinstance(next_tok, lexertokens.BIN_END) or
                        isinstance(next_tok, lexertokens.BIN_START) or
                        isinstance(next_tok, lexertokens.UNARY_TAG)):
                    escaped_tok = next_tok.raw_match
                elif (
                        isinstance(next_tok, lexertokens.OTHER) or
                        isinstance(next_tok, lexertokens.ESCAPE)):
                    # Next token isn't anything special. Just treat the escape
                    # as a backslash.
                    escaped_tok = "\\" + next_tok.raw_match
                elif next_tok is None:
                    escaped_tok = "\\"
                else:
                    raise Exception("Oops. Something broke in the parser.")
                if len(token_stack) > 0:
                    if (
                            isinstance(token_stack[-1], lmast.Markdown) or
                            isinstance(token_stack[-1], lmast.Str)):
                        # Consolidate consecutive Markdown or Str nodes into
                        # one by appending the the previous Str or Markdown
                        token_stack[-1].string += escaped_tok
                    elif len(bin_tag_stack) > 0:
                        token_stack.append(
                                lmast.Str(escaped_tok, cur_token.lineno)
                                )
                    else:
                        token_stack.append(
                                lmast.Markdown(escaped_tok, cur_token.lineno)
                                )
                else:
                    # Otherwise, make a new node. If the token stack is empty,
                    # we can't be in a bin_tag, so it's safe to just make
                    # a markdown node.
                    token_stack.append(
                            lmast.Markdown(
                                escaped_tok,
                                cur_token.lineno)
                    )
            elif isinstance(cur_token, lexertokens.BIN_START):
                bin_tag_stack.append(cur_token)
                token_stack.append(cur_token)
            elif isinstance(cur_token, lexertokens.BIN_END):
                # Find where the last BIN_START was, so pop off the stack
                # and into the temp_stack, until it's found. The goal is to grab
                # Everything between the current END and last START tag, and
                # wrap it in a BinaryTag node
                temp_stack = []
                while True:
                    try:
                        old_tok = token_stack.pop()
                    except:
                        raise lamarksyntaxerror.LaMarkSyntaxError(
                                "{%end%} tag has no matching start tag.",
                                cur_token.lineno)
                    temp_stack.append(old_tok)
                    if isinstance(old_tok, lexertokens.BIN_START):
                        break
                bin_start = temp_stack.pop()
                # Because temp_stack is a stack, the earliest elements are
                # at the end of the list. Reverse so iterating through it will
                # start with earliest elements.
                temp_stack.reverse()
                bin_body = temp_stack
                # Wrap everything in between in a BinTag AST node.
                token_stack.append(
                        lmast.BinTag(
                            bin_body,
                            bin_start.lineno,
                            bin_start.raw_match,
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
                    "Unexpected end of file. Where's the {%end%} tag?",
                    cur_token.lineno)
        # And then the stack is the AST. How cool is that?
        return lmast.Document(token_stack)
