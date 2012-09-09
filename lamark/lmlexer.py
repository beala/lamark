import re
import lexertokens
import tokenstream
import tagplugins

def build_tag_regex(plugin_dict):
    """Given a plugin dict (probably from tagplugins) build an 'or' regex
       group. Something like: (?:latex|ref)
    """
    func_name_list = []
    for func_tuple in plugin_dict:
        for func_name in func_tuple:
            func_name_list.append(func_name)
    regex = '|'.join(func_name_list)
    return '(?:' + regex + ')'

t_ESCAPE = "\\"
t_BIN_START = (r'{%\s*'+
        build_tag_regex(tagplugins.binary_tag_plugins) +
        r'(?:\s+((?!%}).)*%}|\s*%})')
        #r'\s*((?!%}).)*%}')
        #r'(?:\s+[a-zA-Z0-9_./:\-"\s=%]*%}|\s*%})')
t_BIN_END = r"{%\s*end\s*%}"
t_UNARY_TAG = (r'{%\s*'+
        build_tag_regex(tagplugins.unary_tag_plugins) +
        r'(?:\s+((?!%}).)*%}|\s*%})')
        #r'(?:\s+[a-zA-Z0-9_./:\-"\s=%]*%}|\s*%})')
t_NEWLINE = r'\n'

class LmLexer(object):
    """Lexes the token stream into a list of tokens.
    """
    def __init__(self, args):
        self.args = args
        # Current number of newlines counted so far.
        self._newline_count = 1
        # Keeps track of where the OTHER tag started. Necessary because
        # characters that don't match any token get put in a catch-all
        # other_acc. We need to know what line this other_acc started on.
        self._acc_newline_count = 1
        #self._init_func_names()

    def lex(self, string):
        """Lexes the string into a TokenStream of tokens.
        """
        # Contains the string position that needs to be fast-fowarded to.
        ff = 0
        # The token string. Nodes get appended to this.
        t_stream = []
        # The catch-all accumulator.
        other_acc = ""
        # These test the string for a token.
        tests = [
                self._test_newline,
                self._test_escape,
                self._test_bin_start,
                self._test_bin_end,
                self._test_unary_tag,
                ]
        for i in xrange(len(string)):
            # Fast forward `i` to `ff`
            if i < ff:
                continue
            # Run all the token tests at the current position
            for test in tests:
                (ff, node) = test(string, i)
                if i < ff:
                    # If a test accepts the string then
                    # ff will be set to where the test stopped
                    # accepting.
                    if other_acc:
                        if other_acc[0] == "\n":
                            # If the first char of the OTHER token starts with a
                            # newline, say that it starts on the line after the
                            # last tag.
                            self._acc_newline_count += 1
                        # Flush the `other_acc` into the `t_stream`
                        t_stream.append(lexertokens.OTHER(other_acc, self._acc_newline_count))
                        self._acc_newline_count = self._newline_count
                        other_acc = ""
                    # Append the node returned by the test onto the `t_stream`
                    t_stream.append(node)
                    # Break, because a test has accepted the string
                    break
            if i >= ff:
                # If no test accepted the string, so add the current character
                # onto the catch-all `other_acc`
                if string[i] == "\n":
                    # Count the newlines in the OTHER acc
                    self._newline_count += 1
                other_acc += string[i]

        if other_acc:
            trailing_newline_count = self._count_trailing_char(other_acc, "\n")
            # Flush the `other_acc` if it contains anything.
            t_stream.append(
                    lexertokens.OTHER(
                        other_acc,
                        self._newline_count - trailing_newline_count)
            )

        return tokenstream.TokenStream(t_stream)

    def _count_newlines(self, string):
        newline_count = 0
        for char in string:
            if char == "\n":
                newline_count += 1
        return newline_count

    def _count_trailing_char(self, string, target_char):
        trailing_char_count = 0
        for char in reversed(string):
            if char == target_char:
                trailing_char_count += 1
            else:
                break
        return trailing_char_count

    def _test_bin_start(self, string, n):
        matchObj = re.match(t_BIN_START, string[n:], re.DOTALL)
        if matchObj:
            n += len(matchObj.group(0))
            new_tok = lexertokens.BIN_START(matchObj.group(0), self._newline_count)
            self._newline_count += self._count_newlines(matchObj.group(0))
            return (n, new_tok)
        else:
            return (n, None)

    def _test_bin_end(self, string, n):
        matchObj = re.match(t_BIN_END, string[n:], re.DOTALL)
        if matchObj:
            n += len(matchObj.group(0))
            new_tok = lexertokens.BIN_END(matchObj.group(0), self._newline_count)
            self._newline_count += self._count_newlines(matchObj.group(0))
            return (n, new_tok)
        else:
            return (n, None)

    def _test_unary_tag(self, string, n):
        matchObj = re.match(t_UNARY_TAG, string[n:], re.DOTALL)
        if matchObj:
            n += len(matchObj.group(0))
            new_tok = lexertokens.UNARY_TAG(matchObj.group(0), self._newline_count)
            self._newline_count += self._count_newlines(matchObj.group(0))
            return (n, new_tok)
        else:
            return (n, None)

    def _test_newline(self, string, n):
        if string[n:n+len(t_NEWLINE)] == t_NEWLINE:
            self._newline_count += 1
        return (n, None)

    def _test_escape(self, string, n):
        if string[n:n+len(t_ESCAPE)] == t_ESCAPE:
            return (n+len(t_ESCAPE), lexertokens.ESCAPE("\\", self._newline_count))
        else:
            return (n, None)
