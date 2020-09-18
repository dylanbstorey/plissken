import os
from collections import namedtuple

from plissken.documents.module import ModuleDoc

PackageDocument = namedtuple(
    "PackageDocument",
    [
        "name",
        "docstring",
        "variables",
        "classes",
        "functions",
        "sub_packages",
        "modules",
    ],
)


def PackageDoc(directory: str):

    init_py_path = os.path.join(directory, "__init__.py")

    sub_packages = []
    modules = []

    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            if f == "__init__.py":
                if root == directory:
                    package_doc = ModuleDoc(os.path.join(root, f))
            elif f.endswith(".py") and f is not "__init__.py":
                modules.append(os.path.join(root, f))

        for d in dirs:
            if os.path.isfile(os.path.join(root, d, "__init__.py")):
                sub_packages.append(os.path.join(root, d))

        break

    sub_packages = [PackageDoc(n) for n in sub_packages]
    modules = [ModuleDoc(n) for n in modules]
    name = package_doc.name
    docstring = package_doc.docstring
    variables = package_doc.variables
    classes = package_doc.classes
    functions = package_doc.functions

    return PackageDocument(
        name=name,
        docstring=docstring,
        variables=variables,
        classes=classes,
        functions=functions,
        sub_packages=sub_packages,
        modules=modules,
    )
