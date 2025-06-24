// src/expressions.rs
use std::fmt::Write;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

fn pig_latin_str(value: &str, output: &mut String)
{
    if let Some(first_char) = value.chars().next()
    {
        write!(output, "{}{}ay", &value[1..], first_char).unwrap()
    }
}

#[polars_expr(output_type=String)]
pub fn pig_latinnify(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_into_string_amortized(pig_latin_str);
    Ok(out.into_series())
}
