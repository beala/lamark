import re
import mdast
import tagtokens

class TagParser(object):
    t_ARG = r"\w+"
    t_FUNC_NAME = r"{%\s*(\w+)"
    t_ASSIGN = r"="
    t_VALUE = r'"([a-zA-Z0-9_ \./:]*)"'
    t_IGNORE = r"\s*|%\}"

    def __init__(self, args):
        pass

    def parse(self, ast):
        new_ast = []
        for node in ast:
            if isinstance(node, mdast.Markdown):
                new_ast.append(node)
                continue
            elif isinstance(node, mdast.Latex):
                new_ast.append(mdast.Latex(node.string, self._process_tag(node)))
                continue
        return new_ast

    def _process_tag(self, latex_tag):
        tag_token_stream = self._lex_tag(latex_tag)
        return self._parse_tag(tag_token_stream)

    def _lex_tag(self, latex_tag):
        token_tests = [
                self._test_ignore,
                self._test_func_name,
                self._test_arg,
                self._test_value,
                self._test_assign,
                ]
        i = 0
        ff = 0
        t_stream = []
        for i in xrange(len(latex_tag.args)):
            if i < ff:
                continue
            for test in token_tests:
                (ff, node)= test(latex_tag.args, i)
                if i < ff:
                    # Fast forwarded, but ignore whichever characters
                    # we've fast forwarded past.
                    if node == None:
                        break
                    t_stream.append(node)
                    break
        return t_stream

    def _test_ignore(self, string, n):
        matchObj = re.match(self.t_IGNORE, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
        return (n, None)

    def _test_arg(self, string, n):
        matchObj = re.match(self.t_ARG, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, tagtokens.ARG(matchObj.group(0)))
        else:
            return (n, None)

    def _test_value(self, string, n):
        matchObj = re.match(self.t_VALUE, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, tagtokens.VALUE(matchObj.group(1)))
        else:
            return (n, None)

    def _test_assign(self, string, n):
        matchObj = re.match(self.t_ASSIGN, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, tagtokens.ASSIGN(matchObj.group(0)))
        else:
            return (n, None)

    def _test_func_name(self, string, n):
        matchObj = re.match(self.t_FUNC_NAME, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, tagtokens.FUNC_NAME(matchObj.group(1)))
        else:
            return (n, None)


    def _parse_tag(self, tag_token_stream):
        dict_acc = {}
        return self._parse_func_name(tag_token_stream, dict_acc)

    def _parse_func_name(self, t_stream, dict_acc):
        if isinstance(t_stream[0], tagtokens.FUNC_NAME):
            dict_acc["func_name"] = str(t_stream[0])
            res = self._parse_arg(t_stream[1:], dict_acc)
            if res != None:
                return res
            else:
                return dict_acc
        else:
            # TODO: Throw parsing error.
            pass

    def _parse_arg(self, t_stream, dict_acc):
        if len(t_stream) == 0:
            return dict_acc
        if isinstance(t_stream[0], tagtokens.ARG):
            res = self._parse_assign(
                    t_stream[1:],
                    dict_acc,
                    str(t_stream[0])
                    )
            if res != None:
                return res
            else:
                # TODO: Throw parsing error. Must be followed by assign.
                pass

    def _parse_assign(self, t_stream, dict_acc, arg_name):
        if len(t_stream) == 0:
            return dict_acc
        if isinstance(t_stream[0], tagtokens.ASSIGN):
            res = self._parse_value(
                    t_stream[1:],
                    dict_acc,
                    arg_name
                    )
            if res != None:
                return res
            else:
                # TODO: Throw error. Must be followed by value
                pass

    def _parse_value(self, t_stream, dict_acc, arg_name):
        if len(t_stream) == 0:
            return dict_acc
        if isinstance(t_stream[0], tagtokens.VALUE):
            dict_acc[arg_name] = str(t_stream[0])
            res = self._parse_arg(t_stream[1:], dict_acc)
            if res != None:
                return res
