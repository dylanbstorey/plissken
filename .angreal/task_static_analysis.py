import os
import subprocess
import webbrowser

import angreal
from angreal import venv_required

HERE = os.path.dirname(__file__)
up_one = os.path.join(HERE, "..")


@angreal.command()
@angreal.option(
    "--open", is_flag=True, help="generate an html report and open in a browser"
)
@venv_required("plissken")
def angreal_cmd(open):
    """
    static typing via mypy
    """

    if open:
        subprocess.run(
            "mypy plissken --ignore-missing-imports --html-report typing_report",
            shell=True,
            cwd=up_one,
        )
        webbrowser.open(f'file://{os.path.join(up_one,"typing_report","index.html")}')
    else:
        subprocess.run("mypy plissken --ignore-missing-imports", shell=True, cwd=up_one)

    return
