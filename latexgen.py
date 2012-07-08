import subprocess
import tempfile
import os
import shutil
import re

class LatexGen(object):
    """Given a peice of Latex, generate an image, and the markdown
        necessary to display the image.
    """
    DICT_image_zoom = "imgZoom"
    DICT_fn_prefix = "path"
    DICT_fn = "imgName"
    DICT_alt_txt = "alt"

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
        if args.o:
            self._image_dir = os.path.dirname(args.o)
        if args.i:
            self._image_dir = args.i
        if self._image_dir[-1] != "/":
            self._image_dir = self._image_dir + "/"
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
        # Image prefs
        self.PREF_image_zoom = 2000
        # Filename prefs
        self.PREF_fn_prefix = ""
        self.PREF_fn = "" # Use default filename generator.
        # HTML prefs
        self.PREF_alt_txt = "" # Use filename as alt txt

    def canProcess(func_name):
        if func_name == "latex":
            return True
        return False

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

        # Call latex to convert tmp tex file to dvi.
        latex_call = [
                "latex",
                "-output-directory=" + self._tex_tmp_dir,
                tex_tmp.name,
                ]
        subprocess.check_call(latex_call)

        # Generate file for png and convert dvi to png
        if self.PREF_fn == "":
            image_name = self._fn_gen.next()
        else:
            image_name = self.PREF_fn
        dvipng_call = [
                "dvipng",
                "-T", "tight",
                "-x", str(self.PREF_image_zoom),
                "-z", "6",
                tex_tmp.name[0:-3] + "dvi",
                "-o", self._image_dir + ("%s" % image_name),
                ]
        subprocess.check_call(dvipng_call)

        if self.PREF_fn_prefix != "":
            image_name = self.PREF_fn_prefix + image_name

        return image_name
