import os
import pytest

from contextlib import ExitStack
from sybil import Sybil
from doctest import ELLIPSIS, REPORT_NDIFF, NORMALIZE_WHITESPACE
from sybil.parsers.doctest import DocTestParser
from sybil.parsers.codeblock import PythonCodeBlockParser


DOCTEST_FLAGS = ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_NDIFF


class DoctestNamespace:
    def __init__(self):
        self._resources = ExitStack()

    def setup(self, namespace):
        # The docs include an example of how enums can be pickled and
        # unpickled.  For this, our test module must be importable.  Hack
        # sys.path so that the `fruit.py` module (containing an enum for the
        # pickle tests) can be imported.  There's probably a more robust way to
        # do this, but it works and is simple so fix it only if necessary.
        test_dir = os.path.join(os.getcwd(), 'test')
        assert os.path.isfile(os.path.join(test_dir, 'fruit.py'))
        self._resources.enter_context(
            pytest.MonkeyPatch.context()).syspath_prepend(test_dir)

    def teardown(self, namespace):
        self._resources.close()


namespace = DoctestNamespace()


pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=DOCTEST_FLAGS),
        PythonCodeBlockParser(),
        ],
    pattern='*.rst',
    setup=namespace.setup,
    teardown=namespace.teardown,
    ).pytest()
