import logging

class RefGen(object):
    def __init__(self, args):
        self._refs = []
        self._ref_count = 0

    def tear_down(self):
        pass

    def generate(self, ref_string, lineno, args, kwargs):
        if len(args) > 0 and args[0] == "footer":
            md_refs = "### References\n"
            for md_line in self._ref_markdown_gen():
                md_refs += md_line + "\n"
            return md_refs
        else:
            self._ref_count += 1
            self._add_ref(ref_string)
            return "<sup>%d</sup>" % self._ref_count

    def _add_ref(self, ref_string):
        self._refs.append(ref_string)

    def _ref_markdown_gen(self):
        ref_count = 0
        for ref in self._refs:
            ref_count += 1
            yield "%d. %s" % (ref_count, ref)
