import lmast
import latexgen
import tagplugins

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.args = args
        self.plugins_dict = {}
        pass

    def generate(self, lamark_ast):
        pure_md_acc = ""
        #with latexgen.LatexGen(self.args) as lg:
            #for node in matex_ast:
                #if isinstance(node, lmast.Markdown):
                    #pure_md_acc += str(node)
                #elif isinstance(node, lmast.Latex):
                    #pure_md_acc += str(lg.generate(
                        #str(node),
                        #node.lineno,
                        #node.args,
                        #node.kwargs)
                        #)
        self._init_plugins()
        for node in lamark_ast:
            if isinstance(node, lmast.Markdown):
                pure_md_acc += str(node)
            elif isinstance(node, lmast.Latex):
                code_gen = self.plugins_dict[node.kwargs["func_name"]].generate
                pure_md_acc += str(code_gen(
                    str(node),
                    node.lineno,
                    node.args,
                    node.kwargs)
                    )
        self._tear_down_plugins()
        return pure_md_acc

    def _init_plugins(self):
        """Create the plugin objects, and add them to the plugin dict
        """
        for func_name, plugin_obj in tagplugins.tag_plugins.items():
            self.plugins_dict[func_name] = plugin_obj(self.args)

    def _tear_down_plugins(self):
        for func_name, plugin_obj in self.plugins_dict.items():
            plugin_obj.tear_down
