from pathlib import Path

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent


def validate_phone(expr: IntoExpr) -> pl.Expr:
    """
    Valida telefone brasileiro no formato +5516997184720.

    Args:
        expr: Expressão contendo os telefones a serem validados

    Returns:
        Expressão Polars que retorna True para telefones válidos

    Examples:
        >>> import polars as pl
        >>> from expression_lib.phone import validate_phone
        >>> df = pl.DataFrame({"phone": ["+5516997184720", "+5511987654321"]})
        >>> df.with_columns(valid=validate_phone("phone"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="validate_phone",
        args=expr,
        is_elementwise=True,
    )


def validate_phone_flexible(expr: IntoExpr) -> pl.Expr:
    """
    Valida telefone brasileiro com formato mais flexível.
    Aceita: +5516997184720, 5516997184720, 016997184720, 16997184720, etc.

    Args:
        expr: Expressão contendo os telefones a serem validados

    Returns:
        Expressão Polars que retorna True para telefones válidos

    Examples:
        >>> import polars as pl
        >>> from expression_lib.phone import validate_phone_flexible
        >>> df = pl.DataFrame({"phone": ["16997184720", "+5516997184720"]})
        >>> df.with_columns(valid=validate_phone_flexible("phone"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="validate_phone_flexible_expr",
        args=expr,
        is_elementwise=True,
    )


def format_phone(expr: IntoExpr) -> pl.Expr:
    """
    Formata telefone brasileiro para o padrão +55 (16) 99718-4720.

    Args:
        expr: Expressão contendo os telefones a serem formatados

    Returns:
        Expressão Polars que retorna os telefones formatados

    Examples:
        >>> import polars as pl
        >>> from expression_lib.phone import format_phone
        >>> df = pl.DataFrame({"phone": ["16997184720", "+5516997184720"]})
        >>> df.with_columns(formatted=format_phone("phone"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="format_phone_expr",
        args=expr,
        is_elementwise=True,
    )
