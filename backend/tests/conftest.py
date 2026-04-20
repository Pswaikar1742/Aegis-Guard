from __future__ import annotations

import os
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# Keep fail-fast semantics while enabling isolated local tests.
# Explicit assignment avoids inheriting a short placeholder key from the shell env.
os.environ["FASTROUTER_API_KEY"] = "sk_test_key_for_pytest_validation_123456"