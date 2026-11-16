"""Control lab display titles and plant labels (round 11 P1)."""

from electrical_engineer.control_studio.session import (
    _human_control_lab_title,
    _unity_plant_diagram,
)


def test_unity_feedback_title_humanized() -> None:
    assert _human_control_lab_title("unity_feedback", 10.0) == "Unity feedback, K = 10"


def test_unity_plant_block_shows_tf() -> None:
    diagram = _unity_plant_diagram(k=10.0, tau=1.0, title="unity_feedback")
    assert diagram["title"] == "Unity feedback, K = 10"
    plant = next(b for b in diagram["blocks"] if b["id"] == "G")
    assert plant["label"] == "10/(s+1)"