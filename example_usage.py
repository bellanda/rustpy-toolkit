#!/usr/bin/env python3
"""
Example usage of rustpy-toolkit package

Install first with: uv add rustpy-toolkit
"""

import polars as pl
from rustpy_toolkit.cpf_cnpj import format_cpf_cnpj, is_cpf_or_cnpj, validate_cpf_cnpj
from rustpy_toolkit.phone import format_phone, validate_phone
from rustpy_toolkit.text_utils import remove_accents


def main():
    print("🚀 RustPy Toolkit - Example Usage")

    # Create sample data
    df = pl.DataFrame(
        {
            "name": ["João da Silva", "María José"],
            "document": ["50542983800", "60204424000108"],
            "phone": ["+5516997184720", "11987654321"],
        }
    )

    print("Original data:")
    print(df)

    # Process data
    result = df.with_columns(
        [
            validate_cpf_cnpj("document").alias("doc_valid"),
            is_cpf_or_cnpj("document").alias("doc_type"),
            format_cpf_cnpj("document").alias("doc_formatted"),
            validate_phone("phone").alias("phone_valid"),
            format_phone("phone").alias("phone_formatted"),
            remove_accents("name").alias("name_clean"),
        ]
    )

    print("\nProcessed data:")
    print(result)


if __name__ == "__main__":
    main()
