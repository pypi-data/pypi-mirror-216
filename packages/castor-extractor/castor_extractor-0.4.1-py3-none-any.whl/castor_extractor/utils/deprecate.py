import logging
import sys
import warnings
from typing import Tuple

# DeprecationWarning is filtered by default
warnings.filterwarnings("once", category=DeprecationWarning)


def deprecate_python(min_version_supported: Tuple[int]):
    """raises a warning if python version < min_version_supported"""

    python_version = (
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )

    python_version_str = ".".join(map(str, python_version))
    min_supported_str = ".".join(map(str, min_version_supported))

    if python_version < min_version_supported:
        warnings.warn(
            f"You are using python version {python_version_str}, please upgrade to version {min_supported_str} or higher."
            " Your version will be soon deprecated",
            DeprecationWarning,
        )
