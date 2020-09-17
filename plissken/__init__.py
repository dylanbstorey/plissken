import os
import typing
from collections import namedtuple

import redbaron
from redbaron import RedBaron

__version__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()
)


# Documents are just named tuples with data in them
ArgumentDocument = namedtuple("ArgumentDocument", ["name", "default", "annotation"])
DecoratorDocument = namedtuple("DecoratorDocument", ["name", "arguments"])
FunctionDocument = namedtuple(
    "FunctionDocument",
    ["name", "async_", "arguments", "docstring", "decorators", "code"],
)
VariableDocument = namedtuple("VariableDocument", ["name", "annotation", "docstring"])


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


def code2red(filename: str) -> RedBaron:
    with open(filename) as sc:
        red = RedBaron(sc.read())
    return red


def PackageDoc(directory: str):
    raise NotImplemented()
    return PackageDocument()


def ModuleDoc(file: str):
    raise NotImplemented()
    # return ModuleDocument()


def ClassDoc(node: redbaron.nodes.ClassNode):

    name = node.name

    doc_string = ""
    if isinstance(node[0], redbaron.nodes.StringNode):
        doc_string = node[0]

    methods = [FunctionDoc(n) for n in node if isinstance(n, redbaron.nodes.DefNode)]

    init_method = get_init(methods)
    dunder_methods = [n for n in methods if method_is_dunder(n.name)]
    semi_private_methods = [n for n in methods if method_is_semi_private(n.name)]
    private_methods = [n for n in methods if method_is_private(n.name)]
    class_methods = [n for n in methods if method_is_class_method(n.name)]
    class_attributes = [VariableDoc(x[0], x[1]) for x in get_documented_variables(node)]


def get_init(methods):
    init = [n for n in methods if method_is_init(n.name)]
    if len(init) > 1:
        raise ValueError("only one __init__ method allowed")

    rv_init = None
    if init:
        rv_init = init.pop()

    return rv_init


def get_documented_variables(node):
    rv = []
    for ix, n in enumerate(node):
        if isinstance(
            node[ix],
            (
                redbaron.nodes.StandaloneAnnotationNode,
                redbaron.nodes.AssignmentNode,
                redbaron.nodes.NameNode,
            ),
        ):
            if isinstance(node[ix + 1], redbaron.nodes.StringNode):
                rv.append((node[ix], node[ix + 1]))
    return rv

    # return ClassDocument()


def method_is_init(name):
    return name == "__init__"


def method_is_semi_private(name):
    return name.startswith("_") and not name.startswith("__")


def method_is_private(name):
    return name.startswith("_") and not name.endswith("__")


def method_is_dunder(name):
    return name.startswith("__") and name.endswith("__") and name is not "__init__"


def method_is_class_method(name):
    return (
        not method_is_init(name)
        and not method_is_semi_private(name)
        and not method_is_private(name)
        and not method_is_dunder(name)
    )


def FunctionDoc(node: redbaron.nodes.DefNode) -> FunctionDocument:
    """
    A Function is a type of python construct within a Module.
    """
    doc_string = ""
    if isinstance(node[0], redbaron.nodes.StringNode):
        doc_string = node[0]

    decorators = []
    if node.decorators:
        decorators = _generate_decorators(node.decorators)

    return FunctionDocument(
        name=node.name,
        async_=node.async_ or False,
        arguments=_generate_arguments(node.arguments),
        docstring=is_docstring(doc_string),
        decorators=decorators,
        code=node.dumps(),
    )


def _generate_decorators(
    node_list: redbaron.base_nodes.DecoratorsLineProxyList
) -> list:
    decorators = []
    for decorator in node_list:

        assert isinstance(decorator, redbaron.nodes.DecoratorNode)

        call_arguments = []
        if decorator.call:
            for call in decorator.call:
                name = call.value.value

                value = ""
                if call.target:
                    value = call.target.value

                annotation = ""
                call_arguments.append(
                    ArgumentDocument(name=name, default=value, annotation=annotation)
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
            annotation = ""
            if arg.value:
                default = arg.value.value
            if arg.annotation:
                annotation = arg.annotation.value
            args.append(
                ArgumentDocument(name=name, default=default, annotation=annotation)
            )

        if isinstance(arg, redbaron.nodes.ListArgumentNode):
            args.append(
                ArgumentDocument(name=f"*{arg.value.value}", default="", annotation="")
            )

        if isinstance(arg, redbaron.nodes.DictArgumentNode):
            args.append(
                ArgumentDocument(name=f"**{arg.value.value}", default="", annotation="")
            )

    return args


def VariableDoc(
    node: typing.Union[
        redbaron.nodes.NameNode,
        redbaron.nodes.AssignmentNode,
        redbaron.nodes.StandaloneAnnotationNode,
    ],
    doc: redbaron.nodes.StringNode,
):

    name = ""
    annotation = ""
    docstring = ""

    if isinstance(node, redbaron.nodes.NameNode):
        name = node.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""

    elif isinstance(node, redbaron.nodes.AssignmentNode):
        name = node.target.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""

    elif isinstance(node, redbaron.nodes.StandaloneAnnotationNode):
        name = node.target.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""
    else:
        raise ValueError(Node)

    docstring = is_docstring(doc)

    if not docstring:
        raise ValueError(
            f"The docstring for {self.name} doesn't appear valid. Got: {doc.value}"
        )
    return VariableDocument(name=name, annotation=annotation, docstring=docstring)


def is_docstring(string: typing.Union[redbaron.nodes.StringNode, str]) -> str:

    if isinstance(string, redbaron.nodes.StringNode):
        string = string.value

    if string.startswith("'''") and string.endswith("'''"):
        return string[3:][:-3]

    if string.startswith('"""') and string.endswith('"""'):
        return string[3:][:-3]

    return ""
