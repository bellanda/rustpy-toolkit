"""
RustPy Toolkit - High-performance Polars expressions for Brazilian document validation and text processing

This package provides fast, Rust-powered expressions for Polars DataFrames to:
- Validate and format CPF/CNPJ documents
- Validate and format Brazilian phone numbers
- Process text with utilities like accent removal and case conversion

Usage:
    >>> import polars as pl
    >>> from rustpy_toolkit import validate_cpf_cnpj, format_phone
    >>>
    >>> df = pl.DataFrame({"doc": ["11144477735"], "phone": ["+5516997184720"]})
    >>> df.with_columns([
    ...     validate_cpf_cnpj("doc").alias("valid_doc"),
    ...     format_phone("phone").alias("formatted_phone")
    ... ])
"""

# Re-export main functions for convenience
__all__ = [
    # Version
    "__version__",
    # Modules
    "cpf_cnpj",
    "phone",
    "text_utils",
]
