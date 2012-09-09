import logging
import lmast
import random

REFGEN_DICT="RefGenDict"

class RefGen(object):
    def __init__(self, args, shared_dict):
        self._ref_count = 0
        self._shared_dict = shared_dict
        self._shared_dict[REFGEN_DICT] = {}
        self._shared_dict[REFGEN_DICT]["refs"] = []
        self.filename = args.f if args.f is not None else str(random.getrandbits(50)) + "-"
        self._shared_dict[REFGEN_DICT]["nonce"] = self.filename

    def tear_down(self):
        pass

    def generate(self, children, lineno, args, kwargs):
        string_list = map(str, children)
        ref_string = "".join(string_list)
        self._ref_count += 1
        self._add_ref(ref_string.strip())
        footer_link = "#" + self.filename + str(self._ref_count) + "footer"
        ref_link = self.filename + str(self._ref_count) + "ref"
        return lmast.Markdown("<a name='%s'>[<sup>%d</sup>](%s)</a>" % (ref_link,self._ref_count,footer_link), lineno)

    def _add_ref(self, ref_string):
        self._shared_dict[REFGEN_DICT]["refs"].append(ref_string)

class FooterGen(object):
    def __init__(self, args, shared_dict):
        self._shared_dict = shared_dict
        self.filename = args.f if args.f is not None else self._shared_dict[REFGEN_DICT]["nonce"]

    def tear_down(self):
        pass

    def generate(self, lineno, args, kwargs):
        md_ref = "\n".join(self._ref_markdown_gen())
        return lmast.Markdown(md_ref, lineno)

    def _ref_markdown_gen(self):
        ref_count = 0
        for ref in self._shared_dict[REFGEN_DICT]["refs"]:
            ref_count += 1
            ref_link = "#" + self.filename + str(ref_count) + "ref"
            footer_link = self.filename + str(ref_count) + "footer"
            yield "%d. <a name='%s'>[<sup>^</sup>](%s)</a> %s" % (ref_count, footer_link, ref_link, ref)
