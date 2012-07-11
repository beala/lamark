import re
import lexertokens

t_ESCAPE = "\\"
t_LSTART = r'{%\s*latex(\s*[a-zA-Z0-9_]*\s*=\s*"(\w|\\"|\s|\.|/|:)*"\s*)*\s*%}'
t_LEND = r"{%\s*endlatex\s*%}"

class LmLexer(object):
    def __init__(self, args):
        self.args = args

    def lex(self, string):
        # Contains the string position that needs to be fast-fowarded to.
        ff = 0
        # The token string. Nodes get appended to this.
        t_stream = []
        # The catch-all accumulator.
        other_acc = ""
        # These test the string for a token.
        tests = [
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
                # If a test accepts the string then
                # ff will be set to where the test stopped
                # accepting.
                if i < ff:
                    # Flush the `other_acc` into the `t_stream`
                    if other_acc:
                        t_stream.append(lexertokens.OTHER(other_acc))
                        other_acc = ""
                    # Append the node returned by the test onto the `t_stream`
                    t_stream.append(node)
                    # Break, because a test has accepted the string
                    break
            # If no test accepted the string, so add the current character
            # onto the catch-all `other_acc`
            if i >= ff:
                other_acc += string[i]

        # Flush the `other_acc` if it contains anything.
        if other_acc:
            t_stream.append(lexertokens.OTHER(other_acc))

        return t_stream

    def _test_lstart(self, string, n):
        matchObj = re.match(t_LSTART, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, lexertokens.LSTART(matchObj.group(0)))
        else:
            return (n, None)

    def _test_lend(self, string, n):
        matchObj = re.match(t_LEND, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, lexertokens.LEND(matchObj.group(0)))
        else:
            return (n, None)

    def _test_escape(self, string, n):
        if string[n:n+len(t_ESCAPE)] == t_ESCAPE:
            return (n+len(t_ESCAPE), lexertokens.ESCAPE())
        else:
            return (n, None)
