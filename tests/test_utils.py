from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_mobile_robot_reloc import utils
import pytest


def test__ensure_rhino():
    with pytest.raises(Exception):
        utils._ensure_rhino()
