import os

import pytest

HERE = os.path.dirname(__file__)

if __name__ == "__main__":
    pytest.run(HERE)  # type: ignore
