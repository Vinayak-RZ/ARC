from electrical_engineer.capabilities import CAPABILITIES, CapabilityError, bind


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


def test_lumped_sim_binds_run_spice() -> None:
    bound = bind("lumped-circuit-sim")
    assert bound.provider == "run-spice"
    assert bound.no_provider is False


def test_allowlist_size() -> None:
    assert len(CAPABILITIES) == 14
    assert "algebraic-check" in CAPABILITIES
