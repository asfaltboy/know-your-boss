from pathlib import Path
from typing import TextIO

import pytest


DATA_PATH = Path(__file__).parent / "fixtures"


@pytest.fixture()
def data_file():
    file = None

    def f(filename: str) -> TextIO:
        nonlocal file
        file = open(DATA_PATH / filename)
        return file

    yield f
    if file:
        file.close()
