"""Test defaults for the Arc suite."""

import os

# UI sample seeding must not fire during TestClient create_app calls.
os.environ.setdefault("EE_NO_SEED", "1")
