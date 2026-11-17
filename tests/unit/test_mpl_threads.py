import threading

import pytest


def test_concurrent_mathtext_renders_do_not_raise() -> None:
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    import io

    import matplotlib.pyplot as plt

    from electrical_engineer.visual_kit.mpl_threads import install_matplotlib_lock

    assert install_matplotlib_lock()
    errors: list[BaseException] = []

    def render(i: int) -> None:
        try:
            for _ in range(6):
                fig, ax = plt.subplots(figsize=(2, 2))
                ax.set_title(rf"$\omega_n = {i}\,\mathrm{{rad/s}}$, $\zeta={i}.5$")
                ax.set_xlabel(r"$\frac{V_o}{V_m}$")
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                plt.close(fig)
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=render, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors[:1]
