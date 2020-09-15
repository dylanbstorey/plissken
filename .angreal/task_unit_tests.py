import os
import subprocess
import webbrowser

import angreal
from angreal import venv_required

HERE = os.path.realpath(os.path.dirname(__file__))
one_up = os.path.join(HERE, "..")
environment_name = "plissken"


root_test_dir = os.path.abspath(os.path.join(one_up, "tests"))
test_dir = os.path.join(root_test_dir, "unit")


@angreal.command()
@angreal.option(
    "--open", is_flag=True, help="generate an html report and open in a browser"
)
@venv_required(environment_name)
def angreal_cmd(open):
    """
    run integration tests
    """

    root_dir = os.path.join(HERE, "..", "tests")

    test_dir = os.path.join(HERE, "..", "tests", "unit")

    if open:

        subprocess.run(
            f"pytest {test_dir} -svvv --rootdir={root_test_dir} --cov=plissken --cov-report html",
            shell=True,
        )

        output_file = os.path.realpath(os.path.join(one_up, "htmlcov", "index.html"))

        webbrowser.open_new("file://{}".format(output_file))
    else:

        subprocess.run(
            f"pytest {test_dir} -svvv --rootdir={root_test_dir} --cov=plissken --cov-report html",
            shell=True,
        )

    return
