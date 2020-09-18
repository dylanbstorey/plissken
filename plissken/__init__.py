import os

from plissken.documents.helpers import prettyDoc
from plissken.documents.package import PackageDoc

__version__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()
)


def generate_docs(package_directory):
    starting_dir = os.getcwd()
    try:
        os.chdir(os.path.join(package_directory, ".."))
        import json

        doc = prettyDoc(PackageDoc(os.path.basename(package_directory)))
        print(json.dumps(doc, indent=4, separators=(",", ": ")))
    except Exception as e:
        print(e)
    finally:
        os.chdir(starting_dir)
