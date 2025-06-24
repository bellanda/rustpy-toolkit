# expression_lib/__init__.py
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent


def pig_latinnify(expr: IntoExpr) -> pl.Expr:
    """Pig-latinnify expression."""
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="pig_latinnify",
        args=expr,
        is_elementwise=True,
    )
