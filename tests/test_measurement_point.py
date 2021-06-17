from pytest import fixture
from compas_mobile_robot_reloc import MeasurementPoint
from compas.geometry import Point


@fixture
def example_instance():
    return MeasurementPoint(1000, 0, 1000, "example_pt1", attrs={"attribute": 1})


@fixture
def example_instance_wo_idx():
    return MeasurementPoint(5.2, 2.1, 3.4, "example_pt")


def test_init(example_instance):
    assert isinstance(example_instance, Point)
    assert example_instance.pt_name == "example_pt1"
    assert example_instance.attrs["attribute"] == 1


def test___repr__(example_instance):
    assert (
        repr(example_instance) == "Point ID: example_pt1, Location: 1000.0, 0.0, 1000.0"
    )


def test_prefix(example_instance):
    assert example_instance.prefix == "example_pt"


def test_idx(example_instance):
    assert example_instance.idx == 1
    assert isinstance(example_instance.idx, int)


def test__split_pt_name(example_instance):
    assert example_instance._split_pt_name() == ("example_pt", 1)


def test__split_pt_name_no_idx(example_instance_wo_idx):
    _, idx = example_instance_wo_idx._split_pt_name()

    assert idx == 0
