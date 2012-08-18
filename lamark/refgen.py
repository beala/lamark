import logging

REFGEN_DICT="RefGenDict"

class RefGen(object):
    def __init__(self, args, shared_dict):
        self._ref_count = 0
        self._shared_dict = shared_dict
        self._shared_dict[REFGEN_DICT] = []

    def tear_down(self):
        pass

    def generate(self, ref_string, lineno, args, kwargs):
        self._ref_count += 1
        self._add_ref(ref_string)
        return "<sup>%d</sup>" % self._ref_count

    def _add_ref(self, ref_string):
        self._shared_dict[REFGEN_DICT].append(ref_string)

class FooterGen(object):
    def __init__(self, args, shared_dict):
        self._shared_dict = shared_dict

    def tear_down(self):
        pass

    def generate(self, lineno, args, kwargs):
        for ref in self._ref_markdown_gen():
            return ref + "\n"

    def _ref_markdown_gen(self):
        ref_count = 0
        for ref in self._shared_dict[REFGEN_DICT]:
            ref_count += 1
            yield "%d. %s" % (ref_count, ref)
