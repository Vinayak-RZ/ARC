"""Serialize matplotlib's non-thread-safe parts inside the UI server.

The server seeds sample runs on a background thread (rendering figures) while
request threads render Control Studio plots. matplotlib's mathtext parser
(pyparsing state) and figure drawing are not thread-safe, so concurrent use
raised ParseException and surfaced as intermittent HTTP 500s on simulate.
"""

from __future__ import annotations

import functools
import threading

MPL_LOCK = threading.RLock()
_installed = False


def _locked(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with MPL_LOCK:
            return fn(*args, **kwargs)

    wrapper.__arc_mpl_locked__ = True  # type: ignore[attr-defined]
    return wrapper


def install_matplotlib_lock() -> bool:
    """Wrap mathtext parsing, figure drawing and savefig with one process lock. Idempotent."""
    global _installed
    if _installed:
        return True
    try:
        import matplotlib

        matplotlib.use("Agg", force=False)
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
        from matplotlib.mathtext import MathTextParser
    except ImportError:
        return False
    for owner, name in ((MathTextParser, "parse"), (FigureCanvasAgg, "draw"), (Figure, "savefig")):
        fn = getattr(owner, name)
        if not getattr(fn, "__arc_mpl_locked__", False):
            setattr(owner, name, _locked(fn))
    _installed = True
    return True
