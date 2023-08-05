import pathlib
import subprocess

from distutils.core import run_setup

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class NameVersionProcessor(AbstractContextProcessor):
    """
    A context processor that adds the following keys to the context:

    * ``name``: the project name
    * ``version``: the current version of the project

    If this is a python project, we'll get the name and version from setup.py.

    If not, we'll try to get it from Makefile by doing ``make image_name``
    for the name and ``make version`` for the version.
    """

    def annotate(self, context: MessageContext) -> None:
        """
        Add the following keys to ``context``:

        * ``name``: the project name
        * ``version``: the current version of the project

        If this is a python project, we'll get the name and version from
        setup.py.

        If not, we'll try to get it from Makefile by doing ``make image_name``
        for the name and ``make version`` for the version.
        """
        super().annotate(context)
        setup_py = pathlib.Path.cwd() / 'setup.py'
        if setup_py.exists():
            # Extract some stuff from python itself
            python_setup = run_setup(str(setup_py))
            context['name'] = python_setup.get_name()  # type: ignore
            context['version'] = python_setup.get_version()  # type: ignore
        else:
            # No setup.py; let's try Makefile
            makefile = pathlib.Path.cwd() / 'Makefile'
            if makefile.exists():
                context['name'] = subprocess.check_output(['make', 'image_name']).decode('utf8').strip()
                context['version'] = subprocess.check_output(['make', 'version']).decode('utf8').strip()
