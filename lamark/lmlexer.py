import re
import lexertokens
import tokenstream
import tagplugins

t_ESCAPE = "\\"
#_func_name = r'(?:end)[a-zA-Z0-9_]+'
_func_name = r'(?:latex)'
_arg_name = r'[a-zA-Z0-9_]*'
_arg_value  = r'"[a-zA-Z0-9_ \./:\\-]*"'
_arg = r'(\s*(' + _arg_name + r'\s*=)?\s*' + _arg_value + r'\s*)'
#t_LSTART = r'{%\s*' + _func_name + r'\s*' + _arg + r'*\s*%}'
t_LSTART = r'{%\s*latex\s*[a-zA-Z0-9_./:\-"\s=%]*%}'
t_LEND = r"{%\s*end\s*%}"
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
        self._init_func_names()

    def _init_func_names(self):
        func_names = tagplugins.tag_plugins.keys()
        func_names_regex = r"|".join(func_names)
        _func_name = r"(?:" +func_names_regex + r")"

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
            # Flush the `other_acc` if it contains anything.
            t_stream.append(lexertokens.OTHER(other_acc, self._newline_count))

        return tokenstream.TokenStream(t_stream)

    def _count_newlines(self, string):
        newline_count = 0
        for char in string:
            if char == "\n":
                newline_count += 1
        return newline_count

    def _test_lstart(self, string, n):
        matchObj = re.match(t_LSTART, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            new_tok = lexertokens.LSTART(matchObj.group(0), self._newline_count)
            self._newline_count += self._count_newlines(matchObj.group(0))
            return (n, new_tok)
        else:
            return (n, None)

    def _test_lend(self, string, n):
        matchObj = re.match(t_LEND, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            new_tok = lexertokens.LEND(matchObj.group(0), self._newline_count)
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
