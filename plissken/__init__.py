"""plissken
"""
import os
import typing

__version__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()
)


def split_all(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def module_to_fqdns(
    folder: str
) -> typing.Tuple[typing.List[str], typing.List[str], typing.List[str]]:

    paths = []
    fqdns = []
    outputs = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            paths.append(os.path.join(root, f))
            if f == "__init__.py":
                fqdns.append(".".join(split_all(root)))
                outputs.append(os.path.join(*split_all(root), "index"))
            else:
                fqdns.append(".".join(split_all(root) + [f[:-3]]))
                outputs.append(os.path.join(*split_all(root), f[:-3]))

    return paths, fqdns, outputs


import os
import typing
from collections import namedtuple

import redbaron
from redbaron import RedBaron

FunctionArgument = namedtuple("FunctionArgument", ["name", "default", "annotation"])
DecoratorDocument = namedtuple("DecoratorDocument", ["name", "arguments"])


def code2red(filename: str) -> RedBaron:
    with open(filename) as sc:
        red = RedBaron(sc.read())
    return red


class PackageDoc(object):
    """
    Package A package is a collection of modules.
    """

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)
        self.modules = []


class ModuleDoc(object):
    """
    Module A module is a python file within a namespace.

    """

    def __init__(self, path: str):
        self.module = path
        self.module_doc = ""
        self.module_import_path
        self.classes = []
        self.functions = []
        self.variables = []
        pass


class ClassDoc(object):
    """
    Class A  class is a type of python construct within a Module
    """

    def __init__(self, node: redbaron.nodes.ClassNode):
        self.methods = []
        self.variables = []
        self.code
        pass


class FunctionDoc(object):
    """
    A Function is a type of python construct within a Module.
    """

    def __init__(self, node: redbaron.nodes.DefNode):
        self.name = node.name
        self.async_ = node.async_ or False
        self.arguments = _generate_arguments(node.arguments)
        self.doc_string = is_docstring(node[0])
        self.decorators = _generate_decorators()
        self.code = node.dumps()


def _generate_decorators(
    node_list: redbaron.base_nodes.DecoratorsLineProxyList
) -> list:
    decorators = []
    for decorator in node_list:
        assert isinstance(decorator, redbaron.nodes.DecoratorNode)
        call_arguments = []
        for call in decorator.call:
            name = call.value.value

            value = ""
            if call.target:
                value = call.target.value

            annotation = ""
            call_arguments.append(
                FunctionArgument(name=name, default=value, annotation=annotation)
            )

        name_list = decorator.value.value
        decorator_name = "@" + ".".join(
            [x.value for x in name_list if isinstance(x, redbaron.nodes.NameNode)]
        )

        decorators.append(
            DecoratorDocument(name=decorator_name, arguments=call_arguments)
        )
    return decorators


def _generate_arguments(node_list: redbaron.base_nodes.CommaProxyList) -> list:
    args = []
    for arg in node_list:
        if isinstance(arg, redbaron.nodes.DefArgumentNode):

            name = arg.target.value
            default = ""
            if arg.value:
                default = arg.value.value or ""
            if arg.annotation:
                annotation = arg.annotation.value
            args.append(
                FunctionArgument(name=name, default=default, annotation=annotation)
            )

        if isinstance(arg, redbaron.nodes.ListArgumentNode):
            args.append(
                FunctionArgument(name=f"*{arg.value.value}", default="", annotation="")
            )

        if isinstance(arg, redbaron.nodes.DictArgumentNode):
            args.append(
                FunctionArgument(name=f"**{arg.value.value}", default="", annotation="")
            )

    return args


class VariableDoc(object):
    """
    A Variable is a variable, it may or may not be assigned a value
    """

    def __init__(
        self,
        node: typing.Union[
            redbaron.nodes.NameNode,
            redbaron.nodes.AssignmentNode,
            redbaron.nodes.StandaloneAnnotationNode,
        ],
        doc: redbaron.nodes.StringNode,
    ):
        self.name = None
        self.type = None
        self.docstring = None

        if isinstance(node, redbaron.nodes.NameNode):
            self.name = node.value
            try:
                self.type = node.annotation.value
            except:
                self.type = ""

        elif isinstance(node, redbaron.nodes.AssignmentNode):
            self.name = node.target.value
            try:
                self.type = node.annotation.value
            except:
                self.type = ""

        elif isinstance(node, redbaron.nodes.StandaloneAnnotationNode):
            self.name = node.target.value
            try:
                self.type = node.annotation.value
            except:
                self.type = ""
        else:
            raise ValueError(Node)

        self.docstring = is_docstring(doc)

        if not self.docstring:
            raise ValueError(
                f"The docstring for {self.name} doesn't appear valid. Got: {doc.value}"
            )


def is_docstring(string: typing.Union[redbaron.nodes.StringNode, str]) -> str:

    if isinstance(string, redbaron.nodes.StringNode):
        string = string.value

    if string.startswith("'''") and string.endswith("'''"):
        return string[3:][:-3]

    if string.startswith('"""') and string.endswith('"""'):
        return string[3:][:-3]

    return ""
