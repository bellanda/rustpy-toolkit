use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

/// Função para validar CPF seguindo o algoritmo oficial
fn validate_cpf(cpf: &str) -> bool
{
    let digits: Vec<u32> = cpf
        .chars()
        .filter(|c| c.is_ascii_digit())
        .filter_map(|c| c.to_digit(10))
        .collect();

    if digits.len() != 11
    {
        return false;
    }

    // Verifica se todos os dígitos são iguais (casos inválidos como 111.111.111-11)
    if digits.iter().all(|&x| x == digits[0])
    {
        return false;
    }

    // Calcula o primeiro dígito verificador
    let mut sum = 0;
    for i in 0..9
    {
        sum += digits[i] * (10 - i as u32);
    }
    let remainder = sum % 11;
    let first_check_digit = if remainder < 2 { 0 } else { 11 - remainder };

    // Verifica o primeiro dígito verificador
    if digits[9] != first_check_digit
    {
        return false;
    }

    // Calcula o segundo dígito verificador
    sum = 0;
    for i in 0..10
    {
        sum += digits[i] * (11 - i as u32);
    }
    let remainder = sum % 11;
    let second_check_digit = if remainder < 2 { 0 } else { 11 - remainder };

    // Verifica o segundo dígito verificador
    digits[10] == second_check_digit
}

/// Função para validar CNPJ seguindo o algoritmo oficial
fn validate_cnpj(cnpj: &str) -> bool
{
    let digits: Vec<u32> = cnpj
        .chars()
        .filter(|c| c.is_ascii_digit())
        .filter_map(|c| c.to_digit(10))
        .collect();

    if digits.len() != 14
    {
        return false;
    }

    // Verifica se todos os dígitos são iguais (casos inválidos)
    if digits.iter().all(|&x| x == digits[0])
    {
        return false;
    }

    // Pesos para o primeiro dígito verificador
    let weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

    // Calcula o primeiro dígito verificador
    let mut sum = 0;
    for i in 0..12
    {
        sum += digits[i] * weights1[i];
    }
    let remainder = sum % 11;
    let first_check_digit = if remainder < 2 { 0 } else { 11 - remainder };

    // Verifica o primeiro dígito verificador
    if digits[12] != first_check_digit
    {
        return false;
    }

    // Pesos para o segundo dígito verificador
    let weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

    // Calcula o segundo dígito verificador
    sum = 0;
    for i in 0..13
    {
        sum += digits[i] * weights2[i];
    }
    let remainder = sum % 11;
    let second_check_digit = if remainder < 2 { 0 } else { 11 - remainder };

    // Verifica o segundo dígito verificador
    digits[13] == second_check_digit
}

/// Função para extrair apenas dígitos
fn extract_digits(value: &str) -> String
{
    value.chars().filter(|c| c.is_ascii_digit()).collect()
}

/// Função para identificar se é CPF ou CNPJ
fn identify_cpf_cnpj(value: &str) -> Option<&'static str>
{
    let digits = extract_digits(value);

    match digits.len()
    {
        11 =>
        {
            if validate_cpf(&digits)
            {
                Some("CPF")
            }
            else
            {
                None
            }
        },
        14 =>
        {
            if validate_cnpj(&digits)
            {
                Some("CNPJ")
            }
            else
            {
                None
            }
        },
        _ => None,
    }
}

/// Função para formatar CPF
fn format_cpf(cpf: &str) -> String
{
    let digits = extract_digits(cpf);
    if digits.len() == 11
    {
        format!("{}.{}.{}-{}", &digits[0..3], &digits[3..6], &digits[6..9], &digits[9..11])
    }
    else
    {
        cpf.to_string()
    }
}

/// Função para formatar CNPJ
fn format_cnpj(cnpj: &str) -> String
{
    let digits = extract_digits(cnpj);
    if digits.len() == 14
    {
        format!(
            "{}.{}.{}/{}-{}",
            &digits[0..2],
            &digits[2..5],
            &digits[5..8],
            &digits[8..12],
            &digits[12..14]
        )
    }
    else
    {
        cnpj.to_string()
    }
}

/// Valida CPF ou CNPJ e retorna True/False
#[polars_expr(output_type=Boolean)]
pub fn validate_cpf_cnpj(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(DataType::Boolean, |s| {
        let digits = extract_digits(s);
        match digits.len()
        {
            11 => validate_cpf(&digits),
            14 => validate_cnpj(&digits),
            _ => false,
        }
    });
    Ok(out.into_series())
}

/// Identifica se o valor é CPF, CNPJ ou None
#[polars_expr(output_type=String)]
pub fn is_cpf_or_cnpj(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply(|opt_s| opt_s.and_then(|s| identify_cpf_cnpj(s)).map(|doc_type| doc_type.into()));
    Ok(out.into_series())
}

/// Formata CPF ou CNPJ com pontuação adequada
#[polars_expr(output_type=String)]
pub fn format_cpf_cnpj(inputs: &[Series]) -> PolarsResult<Series>
{
    let ca = inputs[0].str()?;
    let out: StringChunked = ca.apply_nonnull_values_generic(DataType::String, |s| {
        let digits = extract_digits(s);
        match digits.len()
        {
            11 =>
            {
                if validate_cpf(&digits)
                {
                    format_cpf(s)
                }
                else
                {
                    s.to_string()
                }
            },
            14 =>
            {
                if validate_cnpj(&digits)
                {
                    format_cnpj(s)
                }
                else
                {
                    s.to_string()
                }
            },
            _ => s.to_string(),
        }
    });
    Ok(out.into_series())
}

#[cfg(test)]
mod tests
{
    use super::*;

    #[test]
    fn test_cpf()
    {
        assert!(validate_cpf("50542983800"));
        assert!(!validate_cpf("11111111111"));
    }

    #[test]
    fn test_cnpj()
    {
        assert!(validate_cnpj("60204424000108"));
        assert!(!validate_cnpj("11111111111111"));
    }

    #[test]
    fn test_format()
    {
        assert_eq!(format_cpf("50542983800"), "505.429.838-00".to_string());
        assert_eq!(format_cnpj("60204424000108"), "60.204.424/0001-08".to_string());
    }
}
