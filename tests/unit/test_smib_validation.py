import pytest

from electrical_engineer.engines.smib_swing import SmibCase, validate_smib_case


def test_validate_rejects_bad_pmax_stage() -> None:
    with pytest.raises(ValueError, match="pmax_fault"):
        validate_smib_case(
            SmibCase(pmax_fault_pu=0.0),
        )


def test_validate_rejects_suspicious_defaults() -> None:
    with pytest.raises(ValueError, match="suspicious"):
        validate_smib_case(SmibCase(f0_hz=60.0, pm_pu=1.0))
