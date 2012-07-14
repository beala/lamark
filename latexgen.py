import subprocess
import tempfile
import os
import shutil
import re
import logging
import sys
import lamarkargumenterror

class LatexGen(object):
    """Given a peice of Latex, generate an image, and the markdown
        necessary to display the image.
    """
    DICT_image_zoom = "imgZoom"
    DICT_fn_prefix = "path"
    DICT_fn = "imgName"
    DICT_alt_txt = "alt"

    prefs_dict = {
            "imgZoom": 2000,
            "path": "",
            "imgName": "",
            "alt": "",
            "func_name": "latex"
            }

    TEX_TMP_NAME = "textemp.tex"

    def __init__(self, args):
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


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self._tex_tmp_dir)

    def _create_tmp_dir(self):
        return tempfile.mkdtemp()

    def _check_preconditions(self):
        if not os.path.exists(self._image_dir):
            raise IOError("ERROR: Image dir does not exist.")

    def _reset_prefs(self):
        prefs_dict = {
                "imgZoom": 2000,
                "path": "",
                "imgName": "",
                "alt": "",
                "func_name": "latex"
                }

    def canProcess(func_name):
        if func_name == "latex":
            return True
        return False

    def generate(self, latex_string, lineno, args, kwargs):
        # Ignore empty strings
        if not latex_string.strip():
            return ""
        self._reset_prefs()
        self._process_tag_args(lineno, args, kwargs)
        self._validate_args(args, kwargs)
        image_name = self._compile_latex(latex_string)
        if self.prefs_dict["alt"] == "":
            alt_text = image_name
        else:
            alt_text = self.prefs_dict["alt"]
        return "![%s](%s)" % (alt_text, image_name)

    def _process_tag_args(self, lineno, args, kwargs):
        logging.debug(args)
        self.prefs_dict["path"] = args[0] if len(args) > 0 else ""
        self.prefs_dict["alt"] = args[1] if len(args) > 1 else ""
        self.prefs_dict["imgZoom"] = args[2] if len(args) > 2 else "2000"
        self.prefs_dict["imgName"] = args[3] if len(args) > 3 else ""
        for key, value in kwargs.items():
            if key not in self.prefs_dict:
                raise lamarkargumenterror.LaMarkArgumentError(
                        "Unrecognized argument: %s" % key,
                        lineno)
            self.prefs_dict[key] = value

        if len(self.prefs_dict["path"]) > 0 and self.prefs_dict["path"][-1] != "/":
            self.prefs_dict["path"] += "/"

    def _validate_args(self, args, kwargs):
        if int(self.prefs_dict["imgZoom"]) > 3000:
            logging.warn("imgZoom is very large: %d", int(self.prefs_dict["imgZoom"]))
        if int(self.prefs_dict["imgZoom"]) < 1000:
            logging.warn("imgZoom is very small: %d", int(self.prefs_dict["imgZoom"]))

    def _gen_name(self):
        counter = 0
        while True:
            yield str(counter) + ".png"
            counter += 1

    def _compile_latex(self, latex_string):
        boilerplate_header = (
                """
                \documentclass{article}
                \pagestyle{empty}
                \\begin{document}
                $""")
        boilerplate_footer = "$\n\end{document}"

        # Create tmp dir and tmp file to write LaTeX to.
        tex_tmp = open(self._tex_tmp_dir + "/" + self.TEX_TMP_NAME, "w")
        tex_tmp.write(boilerplate_header + latex_string + boilerplate_footer)
        tex_tmp.close()

        command_out = subprocess.PIPE

        # Call latex to convert tmp tex file to dvi.
        latex_call = [
                "latex",
                "-output-directory=" + self._tex_tmp_dir,
                "-halt-on-error",
                tex_tmp.name,
                ]
        p = subprocess.Popen(
                latex_call,
                stderr=command_out,
                stdout=command_out)

        out,err = p.communicate()
        logging.debug(out)
        if p.returncode:
            raise CommandException("Error in callto LaTeX: " + str(out))

        # Generate file for png and convert dvi to png
        if self.prefs_dict["imgName"] == "":
            image_name = self._fn_gen.next()
        else:
            image_name = self.prefs_dict["imgName"]
        dvipng_call = [
                "dvipng",
                "-T", "tight",
                "-x", str(self.prefs_dict["imgZoom"]),
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

        if self.prefs_dict["path"] != "":
            image_name = self.prefs_dict["path"] + image_name

        return image_name

class CommandException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

    def __repr(self):
        return "CommandException(%s)" % repr(self.msg)
