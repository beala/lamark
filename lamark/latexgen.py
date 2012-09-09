import subprocess
import tempfile
import os
import shutil
import re
import logging
import sys
import lamarkargumenterror
import lmast
import textwrap

MATH_NAME = "math"
DISPLAYMATH_NAME = "displaymath"
#PICTURE_NAME = "picture"
PREAMBLE_NAME = "pre"
DOC_NAME = "latex"

class LatexGen(object):
    """Given a peice of Latex, generate an image, and the markdown
        necessary to display the image.
    """
    DICT_image_zoom = "imgZoom"
    DICT_fn_prefix = "path"
    DICT_fn = "imgName"
    DICT_alt_txt = "alt"

    prefs_dict = {
            "imgZoom": None,
            "path": None,
            "imgName": None,
            "alt": None,
            "func_name": None,
            }

    TEX_TMP_NAME = "textemp.tex"

    def __init__(self, args, shared_dict):
        """ This initializer SHOULD NOT be used by itself.
            Use the `with` keyword so the __exit__ and __enter__
            methods get used.
        """
        self._fn_gen = self._gen_name()
        self._reset_prefs()
        self._tex_tmp_dir = self._create_tmp_dir()
        self._image_dir = "."
        if args.o and len(os.path.dirname(args.o)) > 0:
            self._image_dir = os.path.dirname(args.o)
        if args.i:
            self._image_dir = args.i
        if self._image_dir[-1] != "/":
            self._image_dir = self._image_dir + "/"

        self._debug_flag = args.debug
        self._check_preconditions()
        self.latex_preamble = None


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.tear_down()

    def tear_down(self):
        shutil.rmtree(self._tex_tmp_dir)

    def _create_tmp_dir(self):
        return tempfile.mkdtemp()

    def _check_preconditions(self):
        if not os.path.exists(self._image_dir):
            raise IOError("ERROR: Image dir does not exist.")

    def _reset_prefs(self):
        prefs_dict = {
                "imgZoom": None,
                "path": None,
                "imgName": None,
                "alt": None,
                "title": None,
                #"x": 0,
                #"y": 0,
                #"unitlength": None,
                }

    def generate(self, children, lineno, args, kwargs):
        latex_body = reduce(
                lambda string, child: string + child.string,
                children,
                "")
        # Ignore empty strings
        #if not latex_body.strip():
        #    return lmast.Markdown("", lineno)
        self._reset_prefs()
        self._process_tag_args(lineno, args, kwargs)
        self._validate_args(args, kwargs)
        if (
                #kwargs["func_name"] == PICTURE_NAME or
                kwargs["func_name"] == MATH_NAME or
                kwargs["func_name"] == DISPLAYMATH_NAME or
                kwargs["func_name"] == DOC_NAME):
            image_name = self._compile_latex(latex_body)
            if self.prefs_dict["alt"] is None:
                alt_text = image_name
            else:
                alt_text = self.prefs_dict["alt"]
            if self.prefs_dict["title"] is not None:
                new_node = lmast.Markdown(
                        '![%s](%s "%s")' % (alt_text, image_name, self.prefs_dict["title"]),
                        lineno)
            else:
                new_node = lmast.Markdown(
                        "![%s](%s)" % (alt_text, image_name),
                        lineno)
        elif kwargs["func_name"] == PREAMBLE_NAME:
            self.latex_preamble = latex_body
            new_node = lmast.Markdown("", lineno)
        else:
            raise Exception("Oops. Something broke in the LaTeX code gen.")
        return new_node

    def _process_math_args(self, lineno, args, kwargs):
        self.prefs_dict["func_name"] = kwargs["func_name"]
        self.prefs_dict["path"] = args[0] if len(args) > 0 else None
        self.prefs_dict["alt"] = args[1] if len(args) > 1 else None
        self.prefs_dict["title"] = args[2] if len(args) > 2 else None
        self.prefs_dict["imgName"] = args[3] if len(args) > 3 else None
        self.prefs_dict["imgZoom"] = args[4] if len(args) > 4 else "2000"
        for key, value in kwargs.items():
            if key not in self.prefs_dict:
                raise lamarkargumenterror.LaMarkArgumentError(
                        "Unrecognized argument: %s" % key,
                        lineno)
            self.prefs_dict[key] = value

        if (
                self.prefs_dict["path"] is not None and
                len(self.prefs_dict["path"]) > 0 and
                self.prefs_dict["path"][-1] != "/"):
            self.prefs_dict["path"] += "/"

    def _process_doc_args(self, lineno, args, kwargs):
        self._process_math_args(lineno, args, kwargs)

    #def _process_picture_args(self, lineno, args, kwargs):
        #self.prefs_dict["func_name"] = kwargs["func_name"]
        #self.prefs_dict["x"] = args[0] if len(args) > 0 else "0"
        #self.prefs_dict["y"] = args[1] if len(args) > 1 else "0"
        #self.prefs_dict["unitlength"] = args[2] if len(args) > 2 else None
        #self.prefs_dict["path"] = args[3] if len(args) > 3 else ""
        #self.prefs_dict["alt"] = args[4] if len(args) > 4 else ""
        #self.prefs_dict["title"] = args[5] if len(args) > 5 else None
        #self.prefs_dict["imgZoom"] = args[6] if len(args) > 6 else "2000"
        #self.prefs_dict["imgName"] = args[7] if len(args) > 7 else ""
        #for key, value in kwargs.items():
            #if key not in self.prefs_dict:
                #raise lamarkargumenterror.LaMarkArgumentError(
                        #"Unrecognized argument: %s" % key,
                        #lineno)
            #self.prefs_dict[key] = value

        #if len(self.prefs_dict["path"]) > 0 and self.prefs_dict["path"][-1] != "/":
            #self.prefs_dict["path"] += "/"

    def _process_pre_args(self, lineno, args, kwargs):
        self.prefs_dict["func_name"] = kwargs["func_name"]

    def _process_tag_args(self, lineno, args, kwargs):
        logging.debug(args)
        if (
                kwargs["func_name"] == MATH_NAME or
                kwargs["func_name"] == DISPLAYMATH_NAME):
            self._process_math_args(lineno, args, kwargs)
        #elif kwargs["func_name"] == PICTURE_NAME:
            #self._process_picture_args(lineno, args, kwargs)
        elif kwargs["func_name"] == DOC_NAME:
            self._process_doc_args(lineno, args, kwargs)
        elif kwargs["func_name"] == PREAMBLE_NAME:
            self._process_pre_args(lineno, args, kwargs)
        else:
            raise Exception("Oops. Something broke in the latex gen.")

    def _validate_args(self, args, kwargs):
        if self.prefs_dict["imgZoom"] is None:
            self.prefs_dict["imgZoom"] = "2000"
        if int(self.prefs_dict["imgZoom"]) > 3000:
            logging.warn("imgZoom is very large: %d", int(self.prefs_dict["imgZoom"]))
        if int(self.prefs_dict["imgZoom"]) < 1000:
            logging.warn("imgZoom is very small: %d", int(self.prefs_dict["imgZoom"]))

    def _gen_name(self):
        counter = 0
        while True:
            yield str(counter) + ".png"
            counter += 1

    def _gen_latex(self, latex_body):
        if self.prefs_dict["func_name"] == DOC_NAME:
            return latex_body.strip()

        latex_string = "\documentclass[fleqn]{standalone}\n"
        if self.latex_preamble is not None:
            latex_string += self.latex_preamble + "\n"

        if self.prefs_dict["func_name"] == MATH_NAME:
            latex_string += "\usepackage{mathtools}\n"
            latex_string += "\\begin{document}\n"
            latex_string += "\\begin{math}\n"
            latex_string += latex_body.strip()
            latex_string += "\\end{math}\n"
            latex_string += "\\end{document}\n"
        elif self.prefs_dict["func_name"] == DISPLAYMATH_NAME:
            latex_string += "\usepackage{mathtools}\n"
            latex_string += "\\begin{document}\n"
            latex_string += "\\begin{displaymath}\n"
            latex_string += latex_body.strip()
            latex_string += "\\end{displaymath}\n"
            latex_string += "\\end{document}\n"
        #elif self.prefs_dict["func_name"] == PICTURE_NAME:
            #latex_string += "\\begin{document}\n"
            #if self.prefs_dict["unitlength"] is not None:
                #latex_string += "\\setlength{\\unitlength}{%s}\n" % self.prefs_dict["unitlength"]
            #latex_string += "\\begin{picture}(%s,%s)\n" % (
                    #self.prefs_dict["x"], self.prefs_dict["y"])
            #latex_string += latex_body + "\n"
            #latex_string += "\\end{picture}\n"
            #latex_string += "\\end{document}\n"
        else:
            raise Exception("Oops.Something broke in the LaTeX code gen.")

        return latex_string

    def _compile_latex(self, latex_body):
        latex_string = self._gen_latex(latex_body)
        logging.debug("Latex String: " + repr(latex_string))

        # Create tmp dir and tmp file to write LaTeX to.
        tex_tmp = open(self._tex_tmp_dir + "/" + self.TEX_TMP_NAME, "w")
        #tex_tmp.write(boilerplate_header + latex_string + boilerplate_footer)
        tex_tmp.write(latex_string)
        tex_tmp.close()

        command_out = subprocess.PIPE

        # Call latex to convert tmp tex file to dvi.
        latex_call = [
                "latex",
                "-output-directory=" + self._tex_tmp_dir,
                "-halt-on-error",
                "-interaction=batchmode",
                tex_tmp.name,
                ]
        p = subprocess.Popen(
                latex_call,
                stderr=command_out,
                stdout=command_out)

        out,err = p.communicate()
        logging.debug(out)
        if p.returncode:
            raise CommandException('Error trying to render LaTeX: "' +
                    str(latex_body) + '".\nLaTeX threw error: "' + str(out)+ '".')

        # Generate file for png and convert dvi to png
        if self.prefs_dict["imgName"] is None:
            image_name = self._fn_gen.next()
        else:
            image_name = self.prefs_dict["imgName"]
        if self.prefs_dict["imgZoom"] is None:
            image_zoom = "2000"
        else:
            image_zoom = str(self.prefs_dict["imgZoom"])
        dvipng_call = [
                "dvipng",
                "-T", "tight",
                "-x", image_zoom,
                "-z", "6",
                tex_tmp.name[0:-3] + "dvi",
                "-o", self._image_dir + ("%s" % image_name),
                ]
        p = subprocess.Popen(
                dvipng_call,
                stdout=command_out,
                stderr=command_out)

        out,err = p.communicate()
        logging.debug(out)
        if p.returncode:
            raise CommandException("Error in call to dvipng: " + str(out))

        if self.prefs_dict["path"] is not None:
            image_name = self.prefs_dict["path"] + image_name

        return image_name

class CommandException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

    def __repr(self):
        return "CommandException(%s)" % repr(self.msg)
