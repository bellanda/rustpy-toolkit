from pathlib import Path

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent


def validate_cpf_cnpj(expr: IntoExpr) -> pl.Expr:
    """
    Valida CPF ou CNPJ e retorna True/False.

    Args:
        expr: Expressão contendo os documentos a serem validados

    Returns:
        Expressão Polars que retorna True para documentos válidos

    Examples:
        >>> import polars as pl
        >>> from expression_lib.cpf_cnpj import validate_cpf_cnpj
        >>> df = pl.DataFrame({"doc": ["11144477735", "11222333000181"]})
        >>> df.with_columns(valid=validate_cpf_cnpj("doc"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="validate_cpf_cnpj",
        args=expr,
        is_elementwise=True,
    )


def is_cpf_or_cnpj(expr: IntoExpr) -> pl.Expr:
    """
    Identifica se o valor é CPF, CNPJ ou None.

    Args:
        expr: Expressão contendo os documentos a serem identificados

    Returns:
        Expressão Polars que retorna "CPF", "CNPJ" ou None

    Examples:
        >>> import polars as pl
        >>> from expression_lib.cpf_cnpj import is_cpf_or_cnpj
        >>> df = pl.DataFrame({"doc": ["11144477735", "11222333000181"]})
        >>> df.with_columns(tipo=is_cpf_or_cnpj("doc"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="is_cpf_or_cnpj",
        args=expr,
        is_elementwise=True,
    )


def format_cpf_cnpj(expr: IntoExpr) -> pl.Expr:
    """
    Formata CPF ou CNPJ com pontuação adequada.
    CPF: 111.444.777-35
    CNPJ: 11.222.333/0001-81

    Args:
        expr: Expressão contendo os documentos a serem formatados

    Returns:
        Expressão Polars que retorna os documentos formatados

    Examples:
        >>> import polars as pl
        >>> from expression_lib.cpf_cnpj import format_cpf_cnpj
        >>> df = pl.DataFrame({"doc": ["11144477735", "11222333000181"]})
        >>> df.with_columns(formatted=format_cpf_cnpj("doc"))
    """
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="format_cpf_cnpj",
        args=expr,
        is_elementwise=True,
    )
