from pathlib import Path

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent


def pig_latinnify(expr: IntoExpr) -> pl.Expr:
    """
    Converte texto para pig latin.

    Args:
        expr: Expressão contendo o texto a ser convertido

    Returns:
        Expressão Polars que retorna o texto em pig latin

    Examples:
        >>> import polars as pl
        >>> from expression_lib.text_utils import pig_latinnify
        >>> df = pl.DataFrame({"text": ["hello", "world"]})
        >>> df.with_columns(pig_latin=pig_latinnify("text"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="pig_latinnify",
        args=expr,
        is_elementwise=True,
    )


def remove_accents(expr: IntoExpr) -> pl.Expr:
    """
    Remove acentos e caracteres especiais do texto.

    Args:
        expr: Expressão contendo o texto a ser processado

    Returns:
        Expressão Polars que retorna o texto sem acentos

    Examples:
        >>> import polars as pl
        >>> from expression_lib.text_utils import remove_accents
        >>> df = pl.DataFrame({"text": ["café", "coração"]})
        >>> df.with_columns(clean=remove_accents("text"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="remove_accents_expr",
        args=expr,
        is_elementwise=True,
    )


def title_case(expr: IntoExpr) -> pl.Expr:
    """
    Converte texto para title case (primeira letra de cada palavra maiúscula).

    Args:
        expr: Expressão contendo o texto a ser convertido

    Returns:
        Expressão Polars que retorna o texto em title case

    Examples:
        >>> import polars as pl
        >>> from expression_lib.text_utils import title_case
        >>> df = pl.DataFrame({"text": ["hello world", "python programming"]})
        >>> df.with_columns(title=title_case("text"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="title_case_expr",
        args=expr,
        is_elementwise=True,
    )
