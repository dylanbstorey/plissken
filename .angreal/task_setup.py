import os
import subprocess

import angreal
from angreal import VirtualEnv

HERE = os.path.realpath(os.path.dirname(__file__))

one_up = os.path.join(HERE, "..")

environment_name = "plissken"

setup_py_path = os.path.realpath(os.path.join(one_up, "project_name"))


@angreal.command()
def angreal_cmd():
    """
    setup a development environment from scratch
    """
    angreal.warn(f"Virtual environment {environment_name} being created.")

    venv = VirtualEnv(name=environment_name, python="python3")
    venv._activate()
    angreal.win(f"Virtual environment {environment_name} created")

    # install dependencies
    subprocess.run("pip install -e .[dev]", shell=True, cwd=one_up)

    # initialize hooks
    subprocess.run("pre-commit install", shell=True, cwd=one_up)

    angreal.win(f"{environment_name} successfully setup !")

    pass
