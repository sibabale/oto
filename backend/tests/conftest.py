"""Default test env: avoid live SEC calls (set OTO_RESEARCH_DATA_SOURCE=sec to override)."""

import os

os.environ.setdefault("OTO_RESEARCH_DATA_SOURCE", "mock")
