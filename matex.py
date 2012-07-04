import argparse
import re
import subprocess
import tempfile
import os

class MdLexer(object):
    t_ESCAPE = "\\"
    #t_OPEN = r"{%"
    #t_CLOSE = r"%}"
    #t_LSTART_KEYWORD = r"\s*latex\s*"
    #t_LEND_KEYWORD = r"\s*endlatex\s*"
    #t_IDENT = r"[a-zA-Z0-9_]*"
    #t_ASSIGN = r"\s*=\s*"
    #t_VALUE = r'"(\w|\\"|\s)*"'
    t_LSTART = r'{%\s*latex(\s*[a-zA-Z0-9_]*\s*=\s*"(\w|\\"|\s|\.|/|:)*"\s*)*\s*%}'
    t_LEND = r"{%\s*endlatex\s*%}"

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
                        t_stream.append(OTHER(other_acc))
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
            t_stream.append(OTHER(other_acc))

        return t_stream

    def _test_lstart(self, string, n):
        matchObj = re.match(self.t_LSTART, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, LSTART(matchObj.group(0)))
        else:
            return (n, None)

    def _test_lend(self, string, n):
        matchObj = re.match(self.t_LEND, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, LEND(matchObj.group(0)))
        else:
            return (n, None)

    def _test_escape(self, string, n):
        if string[n:n+len(self.t_ESCAPE)] == self.t_ESCAPE:
            return (n+len(self.t_ESCAPE), ESCAPE())
        else:
            return (n, None)

class token(object):
    pass

class LSTART(token):
    def __init__(self, raw_match):
        self.raw_match = raw_match

    def __repr__(self):
        return "LSTART(%s)" % self.raw_match

    def __str__(self):
        return self.raw_match

class LEND(token):
    def __init__(self, raw_match):
        self.raw_match = raw_match

    def __repr__(self):
        return "LEND(%s)" % self.raw_match

    def __str__(self):
        return self.raw_match

class ESCAPE(token):
    def __repr__(self):
        return "ESCAPE()"

    def __str__(self):
        return '\\'

class OTHER(token):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "OTHER(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class MdParser(object):
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
                if isinstance(token, LSTART) or isinstance(token, LEND):
                    # If you've escaped a start/end latex tag, then only
                    # keep the tag.
                    acc += str(token)
                else:
                    # Otherwise, keep both.
                    acc += MdLexer.t_ESCAPE + str(token)
                continue

            if isinstance(token, ESCAPE):
                last_escaped = True
                continue

            if isinstance(token, LSTART):
                # Beginning of Latex section. Last section must have been
                # markdown. Add md node to AST
                ast.append(Markdown(acc))
                acc = ""
                current_args = token.raw_match
                continue

            if isinstance(token, LEND):
                # End of Latex section. Add Latex node to AST
                ast.append(Latex(acc, current_args))
                acc = ""
                current_args = ""
                continue

            if isinstance(token, OTHER):
                # String section. Flush to accumulator.
                acc += str(token)
                continue

        if isinstance(ast[-1], Markdown):
            # If the last node is md, merge the remainder in the accumulator
            # into the last node.
            ast[-1] = Markdown((str(ast[-1]) + acc))
        else:
            # Otherwise, add a final md node to the AST
            ast.append(Markdown(acc))

        return ast

class Markdown(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Markdown(%s)" % repr(self.string)

    def __str__(self):
        return self.string

class Latex(object):
    def __init__(self, string, args):
        self.string = string
        self.args = args

    def __repr__(self):
        return "Latex(%s, %s)" % (repr(self.args), repr(self.string))

    def __str__(self):
        return self.string

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
            if isinstance(node, Markdown):
                new_ast.append(node)
                continue
            elif isinstance(node, Latex):
                new_ast.append(Latex(node.string, self._process_tag(node)))
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
            return (n, ARG(matchObj.group(0)))
        else:
            return (n, None)

    def _test_value(self, string, n):
        matchObj = re.match(self.t_VALUE, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, VALUE(matchObj.group(1)))
        else:
            return (n, None)

    def _test_assign(self, string, n):
        matchObj = re.match(self.t_ASSIGN, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, ASSIGN(matchObj.group(0)))
        else:
            return (n, None)

    def _test_func_name(self, string, n):
        matchObj = re.match(self.t_FUNC_NAME, string[n:])
        if matchObj:
            n += len(matchObj.group(0))
            return (n, FUNC_NAME(matchObj.group(1)))
        else:
            return (n, None)


    def _parse_tag(self, tag_token_stream):
        dict_acc = {}
        return self._parse_func_name(tag_token_stream, dict_acc)

    def _parse_func_name(self, t_stream, dict_acc):
        if isinstance(t_stream[0], FUNC_NAME):
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
        if isinstance(t_stream[0], ARG):
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
        if isinstance(t_stream[0], ASSIGN):
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
        if isinstance(t_stream[0], VALUE):
            dict_acc[arg_name] = str(t_stream[0])
            res = self._parse_arg(t_stream[1:], dict_acc)
            if res != None:
                return res

class ARG(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "ARG(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class FUNC_NAME(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "FUNC_NAME(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class VALUE(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "VALUE(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class ASSIGN(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "ASSIGN(%s)" % repr(self.value)

    def __str__(self):
        return str(self.value)

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.output_fn = args.OUTPUT_FILE
        self.lg = LatexGen(args)


    def generate(self, matex_ast):
        #output_fd = open(self.output_fn, 'w')
        pure_md_acc = ""
        for node in matex_ast:
            if isinstance(node, Markdown):
                pure_md_acc += str(node)
                #output_fd.write(str(node))
            elif isinstance(node, Latex):
                pure_md_acc += str(self.lg.generate(str(node), node.args))
                #output_fd.write(self.lg.generate(str(node)))
        #output_fd.close()
        return pure_md_acc


class LatexGen(object):
    """Given a peice of Latex, generate an image, and the markdown
        necessary to display the image.
    """
    DICT_image_zoom = "imgZoom"
    DICT_fn_prefix = "path"
    DICT_fn = "imgName"
    DICT_alt_txt = "alt"

    def __init__(self, args):
        self._fn_gen = self._gen_name()
        self._reset_prefs()
        pass

    def _reset_prefs(self):
        # Image prefs
        self.PREF_image_zoom = 2000
        # Filename prefs
        self.PREF_fn_prefix = ""
        self.PREF_fn = "" # Use default filename generator.
        # HTML prefs
        self.PREF_alt_txt = "" # Use filename as alt txt

    def generate(self, latex_string, latex_args_dict):
        self._reset_prefs()
        self._process_tag_args(latex_args_dict)
        image_name = self._compile_latex(latex_string)
        if self.PREF_alt_txt == "":
            alt_text = image_name
        else:
            alt_text = self.PREF_alt_txt
        return "![%s](%s)" % (alt_text, image_name)

    def _process_tag_args(self, args_dict):
        my_attrs = dir(self)
        my_dict_attrs = []
        for attr in my_attrs:
            if re.match(r"DICT", attr):
                my_dict_attrs.append(attr)

        print my_dict_attrs
        for attr in my_dict_attrs:
            if getattr(self,attr) in args_dict:
                pref_name = "PREF" + attr[4:]
                print pref_name
                print args_dict
                setattr(self, pref_name, args_dict[getattr(self,attr)])

    def _gen_name(self):
        counter = 0
        while True:
            yield str(counter) + ".png"
            counter += 1

    def _compile_latex(self, latex_string):
        boilerplate = (
        """
        \documentclass{article}
        \pagestyle{empty}
        \\begin{document}
        $%s$
        \end{document}
        """)


        tex_tmp = tempfile.NamedTemporaryFile(suffix=".tex", delete=False)
        tex_tmp.write(boilerplate % latex_string)
        tex_tmp.close()


        latex_call = [
                "latex",
                "-output-directory=latex-tmp",
                tex_tmp.name,
                ]
        subprocess.check_call(latex_call)

        if self.PREF_fn == "":
            image_name = self._fn_gen.next()
        else:
            image_name = self.PREF_fn
        dvipng_call = [
                "dvipng",
                "-T", "tight",
                "-x", str(self.PREF_image_zoom),
                "-z", "6",
                "latex-tmp/" + os.path.basename(tex_tmp.name)[0:-3] + "dvi",
                "-o", "%s" % image_name]
        subprocess.check_call(dvipng_call)
        os.remove(tex_tmp.name)

        if self.PREF_fn_prefix != "":
            image_name = self.PREF_fn_prefix + image_name

        return image_name


def main():
    cli_parser = argparse.ArgumentParser(
            description="A LATEX processor for Markdown")
    cli_parser.add_argument("FILE")
    cli_parser.add_argument("OUTPUT_FILE")
    args = cli_parser.parse_args()

    l = MdLexer(args)
    token_stream = l.lex(open(args.FILE).read())
    print "Token stream:"
    print token_stream
    m = MdParser(args)
    ast = m.parse(token_stream)
    print "AST:"
    print ast
    tagparser = TagParser(args)
    tag_ast = tagparser.parse(ast)
    print "Tag AST:"
    print tag_ast
    mg = MdCodeGen(args)
    md = mg.generate(tag_ast)
    print md
    output_f = open(args.OUTPUT_FILE, 'w')
    output_f.write(md)
    output_f.close()

if __name__=="__main__":
    main()
