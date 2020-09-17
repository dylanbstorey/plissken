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
