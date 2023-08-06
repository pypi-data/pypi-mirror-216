"""convert files to csv"""
from typing_extensions import Literal, TypedDict

CsvOptions = TypedDict(
    "CsvOptions", {"delimiter": str, "quoting": Literal[1], "quotechar": str}
)
