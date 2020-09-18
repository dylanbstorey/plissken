from collections import namedtuple

import redbaron

from plissken.documents.function import FunctionDoc
from plissken.documents.helpers import get_documented_variables, is_docstring
from plissken.documents.klass import ClassDoc
from plissken.documents.variable import VariableDoc
from plissken.file_operators import code2red, get_qualified_name_from_path

ModuleDocument = namedtuple(
    "ModuleDocument", ["name", "docstring", "variables", "classes", "functions"]
)


def ModuleDoc(file: str):
    # A Module is a python file that isn't an __init__.py file
    # It can have Variables, Classes, Methods, and/or a doc string

    node = code2red(file)

    name = get_qualified_name_from_path(file)

    docstring = ""
    if isinstance(node[0], redbaron.nodes.StringNode):
        docstring = node[0]
    docstring = is_docstring(docstring)

    variables = [VariableDoc(n[0], n[1]) for n in get_documented_variables(node)]
    classes = [ClassDoc(n) for n in node if isinstance(n, redbaron.nodes.ClassNode)]
    functions = [FunctionDoc(n) for n in node if isinstance(n, redbaron.nodes.DefNode)]

    return ModuleDocument(
        name=name,
        docstring=docstring,
        variables=variables,
        classes=classes,
        functions=functions,
    )
