from electrical_engineer.capabilities import (
    CAPABILITIES,
    CD_NO_PROVIDER,
    CapabilityError,
    bind,
    provider_installed,
)


def test_unknown_id_rejected() -> None:
    try:
        bind("lookup_vout_guess")
    except CapabilityError as exc:
        assert "unknown id" in str(exc)
    else:
        raise AssertionError("expected reject")


def test_algebraic_check_binds_check_numeric() -> None:
    bound = bind("algebraic-check")
    assert bound.provider == "check-numeric"
    assert bound.no_provider is False


def test_explicit_provider_passthrough() -> None:
    bound = bind("run-spice")
    assert bound.provider == "run-spice"
    assert bound.capability is None


def test_lumped_sim_without_spice_is_cannot_do() -> None:
    bound = bind("lumped-circuit-sim")
    if provider_installed("run-spice"):
        assert bound.provider == "run-spice"
        assert bound.no_provider is False
    else:
        assert bound.provider == "label-unchecked"
        assert bound.cannot_do == CD_NO_PROVIDER


def test_allowlist_size() -> None:
    assert len(CAPABILITIES) == 14
    assert "algebraic-check" in CAPABILITIES
