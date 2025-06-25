use std::sync::LazyLock;

use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use regex::Regex;

/// Pre-compiled regex patterns for phone validation (compiled only once)
static PHONE_STRICT_REGEX: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"^\+55\d{2}9?\d{8}$").unwrap());

static PHONE_FLEXIBLE_PATTERNS: LazyLock<Vec<Regex>> = LazyLock::new(|| {
    vec![
        Regex::new(r"^\+55\d{2}9\d{8}$").unwrap(), // +5516997184720
        Regex::new(r"^\+55\d{2}\d{8}$").unwrap(),  // +551687184720 (sem o 9)
        Regex::new(r"^55\d{2}9\d{8}$").unwrap(),   // 5516997184720
        Regex::new(r"^0\d{2}9\d{8}$").unwrap(),    // 016997184720
        Regex::new(r"^\d{2}9\d{8}$").unwrap(),     // 16997184720
    ]
});

/// Função para validar telefone brasileiro
/// Formatos aceitos: +5516997184720, +5511987654321, etc.
/// Padrão: +55 + código de área (2 dígitos) + 9 (opcional) + número (8 dígitos)
fn validate_phone_internal(phone: &str) -> bool
{
    PHONE_STRICT_REGEX.is_match(phone)
}

/// Função para validar telefone com formato mais flexível
fn validate_phone_flexible(phone: &str) -> bool
{
    // Remove espaços e caracteres especiais
    let clean_phone = phone.replace([' ', '-', '(', ')', '.'], "");

    // Usa regex pré-compiladas para verificar diferentes formatos
    PHONE_FLEXIBLE_PATTERNS.iter().any(|regex| regex.is_match(&clean_phone))
}

/// Função para formatar telefone brasileiro
fn format_phone(phone: &str) -> String
{
    let digits: String = phone.chars().filter(|c| c.is_ascii_digit()).collect();

    match digits.len()
    {
        // Formato: 5516997184720 -> +55 (16) 99718-4720
        13 if digits.starts_with("55") =>
        {
            format!("+55 ({}) {}-{}", &digits[2..4], &digits[4..9], &digits[9..13])
        },
        // Formato: 16997184720 -> +55 (16) 99718-4720
        11 =>
        {
            format!("+55 ({}) {}-{}", &digits[0..2], &digits[2..7], &digits[7..11])
        },
        // Formato: 016997184720 -> +55 (16) 99718-4720
        12 if digits.starts_with("0") =>
        {
            format!("+55 ({}) {}-{}", &digits[1..3], &digits[3..8], &digits[8..12])
        },
        _ => phone.to_string(),
    }
}

/// Valida telefone brasileiro no formato +5516997184720
/// Otimizado com regex pré-compiladas
#[polars_expr(output_type=Boolean)]
pub fn validate_phone(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(DataType::Boolean, |s| validate_phone_internal(s));
    Ok(out.into_series())
}

/// Valida telefone brasileiro com formato mais flexível
/// Otimizado com regex pré-compiladas
#[polars_expr(output_type=Boolean)]
pub fn validate_phone_flexible_expr(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(DataType::Boolean, |s| validate_phone_flexible(s));
    Ok(out.into_series())
}

/// Formata telefone brasileiro
/// Otimizado com validação eficiente
#[polars_expr(output_type=String)]
pub fn format_phone_expr(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_nonnull_values_generic(DataType::String, |s| {
        if validate_phone_flexible(s)
        {
            format_phone(s)
        }
        else
        {
            s.to_string()
        }
    });
    Ok(out.into_series())
}
