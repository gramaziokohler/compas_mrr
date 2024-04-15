from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_mrr.utils import _ensure_rhino
from pytest import raises


def test__ensure_rhino():
    with raises(ImportError):
        _ensure_rhino()
