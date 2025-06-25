# Tests Directory

Esta pasta contém testes de performance para todas as funções do `rustpy-toolkit`.

## 🚀 Como Executar

### Teste Completo (Recomendado)

```bash
# Executa testes de performance para CPF, CNPJ e telefone
uv run python tests/performance_test.py
```

### Teste Rápido

```bash
# Teste rápido apenas para verificar se está funcionando
uv run python quick_test.py
```

## 📊 O Que É Testado

### Funções Testadas

- **CPF/CNPJ**: `validate_cpf_cnpj()` e `format_cpf_cnpj()` (função unificada)
- **Telefone**: `validate_phone()`, `validate_phone_flexible()` e `format_phone()`

### Tamanhos de Dataset

- 50.000 registros
- 100.000 registros
- 250.000 registros
- Teste de stress: 500.000 registros cada (1.5M total)

### Formatos Testados

#### CPF

- `123.456.789-09` - Formato padrão
- `12345678909` - Apenas números
- `123 456 789 09` - Com espaços
- `123.456.789/09` - Formato misto
- Dados inválidos para teste

#### CNPJ

- `12.345.678/0001-90` - Formato padrão
- `12345678000190` - Apenas números
- `12 345 678 0001 90` - Com espaços
- `12.345.678-0001/90` - Formato misto
- Dados inválidos para teste

#### Telefone

- `+5516997184720` - Internacional padrão
- `+551687184720` - Internacional sem 9
- `5516997184720` - Nacional
- `016997184720` - Com prefixo 0
- `16997184720` - Simples
- `+55 16 99718 4720` - Com espaços
- `+55 (16) 99718-4720` - Formatado
- Dados inválidos para teste

## 📈 Métricas de Performance

### Performance Esperada

- **Excelente**: > 200.000 registros/segundo
- **Boa**: > 100.000 registros/segundo
- **Aceitável**: > 50.000 registros/segundo

### Exemplo de Saída

```
🚀 RustPy-Toolkit Comprehensive Performance Test
============================================================

🎯 Testing with 50,000 records each
========================================

📋 CPF Performance Test (50,000 records)
--------------------------------------------------
  Sample data: ['123.456.789-12', '12345678901', '123 456 789 12']
    🔍 Testing CPF Validation...
      └─ CPF Validation: 0.0234s (2,136,752 records/sec) - 8,333 valid
    🔍 Testing CPF Formatting...
      └─ CPF Formatting: 0.0187s (2,673,797 records/sec) - 50,000 valid
    ⚡ Combined operations: 0.0421s (1,187,648 records/sec)

📊 Overall Performance Summary (50,000 records each):
  └─ CPF throughput: 1,187,648 records/sec
  └─ CNPJ throughput: 1,045,123 records/sec
  └─ Phone throughput: 431,065 records/sec
  └─ Overall throughput: 554,945 records/sec
```

## 🔧 Pré-requisitos

### Build do Módulo

```bash
# Certifique-se de que o módulo Rust está compilado
uv run maturin develop --release
```

### Dependências

- `polars` - Para processamento de dados
- `rustpy-toolkit` - O módulo compilado

## 🐛 Troubleshooting

### Erro de Importação

```bash
# Se houver erro de importação, recompile o módulo
uv run maturin develop --release

# Teste a importação
uv run python -c "from rustpy_toolkit.cpf_cnpj import validate_cpf_cnpj; print('✅ OK')"
```

### Performance Baixa

- Verifique se está compilado em modo release (`--release`)
- Monitore uso de CPU e memória durante os testes
- Execute múltiplas vezes para obter médias consistentes

### Problemas de Memória

- Reduza o tamanho dos datasets de teste
- Execute testes individuais em vez do teste completo
- Monitore uso de memória do sistema

## 📋 Interpretação dos Resultados

### Indicadores de Boa Performance

- Throughput consistente entre iterações
- Escalabilidade linear com tamanho dos dados
- Baixo uso de memória relativo ao tamanho dos dados
- Validação correta dos formatos esperados

### Sinais de Problemas

- Grande variação entre iterações (indica carga do sistema)
- Throughput muito baixo (< 50k records/sec)
- Uso excessivo de memória
- Resultados de validação incorretos

## 🎯 Customização

Você pode modificar `performance_test.py` para:

- Testar tamanhos diferentes de dataset
- Adicionar novos formatos de teste
- Exportar resultados para arquivos
- Adicionar análises estatísticas
- Testar cenários específicos

Exemplo:

```python
# Tamanhos customizados
test_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]

# Formatos customizados de CPF
custom_cpf_formats = [
    "123.456.789-10",
    "123-456-789-10",
    # Adicione seus formatos aqui
]
```

```

```
