use std::fmt::Write;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

/// Converte uma string para pig latin
fn pig_latin_str(value: &str, output: &mut String)
{
    if let Some(first_char) = value.chars().next()
    {
        write!(output, "{}{}ay", &value[1..], first_char).unwrap()
    }
}

/// Converte texto para pig latin
#[polars_expr(output_type=String)]
pub fn pig_latinnify(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_into_string_amortized(pig_latin_str);
    Ok(out.into_series())
}

/// Remove acentos e caracteres especiais
fn remove_accents(text: &str) -> String
{
    text.chars()
        .map(|c| match c
        {
            'á' | 'à' | 'ã' | 'â' | 'ä' => 'a',
            'é' | 'è' | 'ê' | 'ë' => 'e',
            'í' | 'ì' | 'î' | 'ï' => 'i',
            'ó' | 'ò' | 'õ' | 'ô' | 'ö' => 'o',
            'ú' | 'ù' | 'û' | 'ü' => 'u',
            'ç' => 'c',
            'ñ' => 'n',
            'Á' | 'À' | 'Ã' | 'Â' | 'Ä' => 'A',
            'É' | 'È' | 'Ê' | 'Ë' => 'E',
            'Í' | 'Ì' | 'Î' | 'Ï' => 'I',
            'Ó' | 'Ò' | 'Õ' | 'Ô' | 'Ö' => 'O',
            'Ú' | 'Ù' | 'Û' | 'Ü' => 'U',
            'Ç' => 'C',
            'Ñ' => 'N',
            _ => c,
        })
        .collect()
}

/// Remove acentos de texto
#[polars_expr(output_type=String)]
pub fn remove_accents_expr(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_nonnull_values_generic(DataType::String, |s| remove_accents(s));
    Ok(out.into_series())
}

/// Capitaliza primeira letra de cada palavra
fn title_case(text: &str) -> String
{
    text.split_whitespace()
        .map(|word| {
            let mut chars = word.chars();
            match chars.next()
            {
                None => String::new(),
                Some(first) => first.to_uppercase().collect::<String>() + &chars.as_str().to_lowercase(),
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

/// Converte texto para title case
#[polars_expr(output_type=String)]
pub fn title_case_expr(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_nonnull_values_generic(DataType::String, |s| title_case(s));
    Ok(out.into_series())
}
