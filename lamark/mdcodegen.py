import lmast
import latexgen
import tagplugins
import logging

class MdCodeGen(object):
    """ Last stage. Generate Markdown from the AST
    """
    def __init__(self, args):
        self.args = args
        self.binary_plugins_dict = {}
        self.unary_plugins_dict = {}
        self.shared_dict = {}
        pass

    def generate(self, lamark_ast):
        self._init_plugins()
        md_ast = lmast.map_postorder(
                lamark_ast,
                self.gen_dispatch)
        md_string = ""
        for md_node in md_ast.doc:
            md_string += md_node.string
        self._tear_down_plugins()
        return md_string

    def gen_dispatch(self, node):
        if isinstance(node, lmast.Markdown):
            new_node = node
        elif isinstance(node, lmast.Str):
            new_node = node
        elif isinstance(node, lmast.BinTag):
            func_name = node.kwargs["func_name"]
            plugin_obj = self._find_binary_plugin(func_name)
            if plugin_obj == None:
                logging.warning(
                        "Unrecognized tag: " + func_name + ". Skipping.")
                return None
            new_node = plugin_obj.generate(
                node.children,
                node.lineno,
                node.args,
                node.kwargs)
        elif isinstance(node, lmast.UnaryTag):
            func_name = node.kwargs["func_name"]
            plugin_obj = self._find_unary_plugin(func_name)
            if plugin_obj == None:
                logging.warning(
                        "Unrecognized tag: " + func_name + ". Skipping.")
                return None
            new_node = plugin_obj.generate(
                node.lineno,
                node.args,
                node.kwargs)
        elif isinstance(node, lmast.Document):
            new_node = node
        return new_node

    def _init_plugins(self):
        """Create the plugin objects, and add them to the plugin dict
        """
        # Init binary tag plugins
        for func_name, plugin_class in tagplugins.binary_tag_plugins.items():
            self.binary_plugins_dict[func_name] = plugin_class(
                    self.args,
                    self.shared_dict)
        # Init unary tag plugins
        for func_name, plugin_class in tagplugins.unary_tag_plugins.items():
            self.unary_plugins_dict[func_name] = plugin_class(
                    self.args,
                    self.shared_dict)

    def _find_binary_plugin(self, func_name):
        return self._search_plugin_dict(self.binary_plugins_dict, func_name)

    def _find_unary_plugin(self, func_name):
        return self._search_plugin_dict(self.unary_plugins_dict, func_name)

    def _search_plugin_dict(self, plugin_dict, func_name):
        for key in plugin_dict:
            if func_name in key:
                return plugin_dict[key]
        return None

    def _tear_down_plugins(self):
        for func_name, plugin_obj in self.unary_plugins_dict.items():
            plugin_obj.tear_down()

        for func_name, plugin_obj in self.binary_plugins_dict.items():
            plugin_obj.tear_down()
