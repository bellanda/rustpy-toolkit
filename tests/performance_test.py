#!/usr/bin/env python3
"""
Comprehensive performance test for all rustpy-toolkit functions.
Tests CPF, CNPJ, and phone validation/formatting with large datasets.
"""

import os
import random
import sys
import time
from typing import List, Tuple

import polars as pl

# Add the parent directory to sys.path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from rustpy_toolkit.cpf_cnpj import format_cpf_cnpj, is_cpf_or_cnpj, validate_cpf_cnpj
    from rustpy_toolkit.phone import format_phone, validate_phone, validate_phone_flexible
except ImportError:
    print("Error: rustpy_toolkit module not found. Make sure to build the package first.")
    print("Run: uv run maturin develop --release")
    sys.exit(1)


def generate_cpf_data(count: int) -> List[str]:
    """Generate various CPF formats for testing."""
    cpfs = []
    print(f"  Generating {count:,} CPF numbers...")

    for i in range(count):
        format_type = i % 6

        if format_type == 0:
            # Valid CPF: 123.456.789-09
            base = f"{random.randint(100000000, 999999999):09d}"
            cpf = f"{base[:3]}.{base[3:6]}.{base[6:9]}-{random.randint(10, 99)}"
        elif format_type == 1:
            # Valid CPF without formatting: 12345678909
            cpf = f"{random.randint(10000000000, 99999999999):011d}"
        elif format_type == 2:
            # CPF with spaces: 123 456 789 09
            base = f"{random.randint(100000000, 999999999):09d}"
            cpf = f"{base[:3]} {base[3:6]} {base[6:9]} {random.randint(10, 99)}"
        elif format_type == 3:
            # CPF with mixed formatting: 123.456.789/09
            base = f"{random.randint(100000000, 999999999):09d}"
            cpf = f"{base[:3]}.{base[3:6]}.{base[6:9]}/{random.randint(10, 99)}"
        elif format_type == 4:
            # Invalid CPF (wrong length)
            cpf = f"{random.randint(1000000, 9999999):07d}"
        else:
            # Invalid CPF (letters)
            cpf = f"invalid{random.randint(1000, 9999)}"

        cpfs.append(cpf)

    return cpfs


def generate_cnpj_data(count: int) -> List[str]:
    """Generate various CNPJ formats for testing."""
    cnpjs = []
    print(f"  Generating {count:,} CNPJ numbers...")

    for i in range(count):
        format_type = i % 6

        if format_type == 0:
            # Valid CNPJ: 12.345.678/0001-90
            base = f"{random.randint(10000000, 99999999):08d}"
            branch = f"{random.randint(1, 9999):04d}"
            check = f"{random.randint(10, 99):02d}"
            cnpj = f"{base[:2]}.{base[2:5]}.{base[5:8]}/{branch}-{check}"
        elif format_type == 1:
            # Valid CNPJ without formatting: 12345678000190
            cnpj = f"{random.randint(10000000000000, 99999999999999):014d}"
        elif format_type == 2:
            # CNPJ with spaces: 12 345 678 0001 90
            base = f"{random.randint(10000000, 99999999):08d}"
            branch = f"{random.randint(1, 9999):04d}"
            check = f"{random.randint(10, 99):02d}"
            cnpj = f"{base[:2]} {base[2:5]} {base[5:8]} {branch} {check}"
        elif format_type == 3:
            # CNPJ with mixed formatting: 12.345.678-0001/90
            base = f"{random.randint(10000000, 99999999):08d}"
            branch = f"{random.randint(1, 9999):04d}"
            check = f"{random.randint(10, 99):02d}"
            cnpj = f"{base[:2]}.{base[2:5]}.{base[5:8]}-{branch}/{check}"
        elif format_type == 4:
            # Invalid CNPJ (wrong length)
            cnpj = f"{random.randint(100000000, 999999999):09d}"
        else:
            # Invalid CNPJ (letters)
            cnpj = f"invalid{random.randint(10000, 99999)}"

        cnpjs.append(cnpj)

    return cnpjs


def generate_phone_data(count: int) -> List[str]:
    """Generate various phone formats for testing."""
    phones = []
    area_codes = ["11", "16", "21", "31", "41", "51", "61", "71", "81", "85"]
    print(f"  Generating {count:,} phone numbers...")

    for i in range(count):
        area = random.choice(area_codes)
        number = f"{random.randint(90000000, 99999999)}"
        format_type = i % 8

        if format_type == 0:
            # +5516997184720
            phone = f"+55{area}9{number}"
        elif format_type == 1:
            # +551687184720 (without 9)
            phone = f"+55{area}{number}"
        elif format_type == 2:
            # 5516997184720
            phone = f"55{area}9{number}"
        elif format_type == 3:
            # 016997184720
            phone = f"0{area}9{number}"
        elif format_type == 4:
            # 16997184720
            phone = f"{area}9{number}"
        elif format_type == 5:
            # With spaces: +55 16 99718 4720
            phone = f"+55 {area} 9{number[:5]} {number[5:]}"
        elif format_type == 6:
            # With parentheses: +55 (16) 99718-4720
            phone = f"+55 ({area}) 9{number[:5]}-{number[5:]}"
        else:
            # Invalid format
            phone = f"invalid{area}{number}"

        phones.append(phone)

    return phones


def benchmark_function(func, data: pl.DataFrame, col_name: str, func_name: str, iterations: int = 3) -> Tuple[float, int]:
    """Benchmark a function with multiple iterations."""
    times = []
    valid_count = 0

    print(f"    🔍 Testing {func_name}...")

    for i in range(iterations):
        start_time = time.perf_counter()
        result = func(data)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

        # Get valid count from first iteration
        if i == 0:
            if hasattr(result, "sum"):
                # For boolean results (validation functions)
                try:
                    valid_count = result.sum()
                except Exception:
                    # If sum fails, count non-null values
                    valid_count = result.len() - result.null_count()
            elif isinstance(result, pl.DataFrame) and len(result.columns) > 0:
                # For formatting functions, count non-null results
                valid_count = result.select(pl.col(result.columns[0]).is_not_null().sum()).item()
            else:
                # Fallback: count total records
                valid_count = len(data)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    throughput = len(data) / avg_time
    print(f"      └─ {func_name}: {avg_time:.4f}s ({throughput:,.0f} records/sec) - {valid_count:,} valid")

    return avg_time, valid_count


def test_cpf_performance(size: int):
    """Test CPF validation and formatting performance."""
    print(f"\n📋 CPF Performance Test ({size:,} records)")
    print("-" * 50)

    # Generate test data
    cpf_data = generate_cpf_data(size)
    df = pl.DataFrame({"cpf": cpf_data})

    print(f"  Sample data: {cpf_data[:3]}")

    # Test CPF functions
    validate_time, valid_count = benchmark_function(
        lambda data: data.with_columns(validate_cpf_cnpj(pl.col("cpf")).alias("valid"))["valid"], df, "cpf", "CPF Validation"
    )

    format_time, formatted_count = benchmark_function(
        lambda data: data.with_columns(format_cpf_cnpj(pl.col("cpf")).alias("formatted"))["formatted"],
        df,
        "cpf",
        "CPF Formatting",
    )

    # Combined operations
    start_time = time.perf_counter()
    result_df = df.with_columns(
        [validate_cpf_cnpj(pl.col("cpf")).alias("valid"), format_cpf_cnpj(pl.col("cpf")).alias("formatted")]
    )
    combined_time = time.perf_counter() - start_time

    throughput = size / combined_time
    print(f"    ⚡ Combined operations: {combined_time:.4f}s ({throughput:,.0f} records/sec)")

    return combined_time, throughput


def test_cnpj_performance(size: int):
    """Test CNPJ validation and formatting performance."""
    print(f"\n🏢 CNPJ Performance Test ({size:,} records)")
    print("-" * 50)

    # Generate test data
    cnpj_data = generate_cnpj_data(size)
    df = pl.DataFrame({"cnpj": cnpj_data})

    print(f"  Sample data: {cnpj_data[:3]}")

    # Test CNPJ functions
    validate_time, valid_count = benchmark_function(
        lambda data: data.with_columns(validate_cpf_cnpj(pl.col("cnpj")).alias("valid"))["valid"],
        df,
        "cnpj",
        "CNPJ Validation",
    )

    format_time, formatted_count = benchmark_function(
        lambda data: data.with_columns(format_cpf_cnpj(pl.col("cnpj")).alias("formatted"))["formatted"],
        df,
        "cnpj",
        "CNPJ Formatting",
    )

    # Combined operations
    start_time = time.perf_counter()
    result_df = df.with_columns(
        [validate_cpf_cnpj(pl.col("cnpj")).alias("valid"), format_cpf_cnpj(pl.col("cnpj")).alias("formatted")]
    )
    combined_time = time.perf_counter() - start_time

    throughput = size / combined_time
    print(f"    ⚡ Combined operations: {combined_time:.4f}s ({throughput:,.0f} records/sec)")

    return combined_time, throughput


def test_phone_performance(size: int):
    """Test phone validation and formatting performance."""
    print(f"\n📞 Phone Performance Test ({size:,} records)")
    print("-" * 50)

    # Generate test data
    phone_data = generate_phone_data(size)
    df = pl.DataFrame({"phone": phone_data})

    print(f"  Sample data: {phone_data[:3]}")

    # Test phone functions
    strict_time, strict_valid = benchmark_function(
        lambda data: data.with_columns(validate_phone(pl.col("phone")).alias("valid_strict"))["valid_strict"],
        df,
        "phone",
        "Phone Strict Validation",
    )

    flexible_time, flexible_valid = benchmark_function(
        lambda data: data.with_columns(validate_phone_flexible(pl.col("phone")).alias("valid_flexible"))["valid_flexible"],
        df,
        "phone",
        "Phone Flexible Validation",
    )

    format_time, formatted_count = benchmark_function(
        lambda data: data.with_columns(format_phone(pl.col("phone")).alias("formatted"))["formatted"],
        df,
        "phone",
        "Phone Formatting",
    )

    # Combined operations
    start_time = time.perf_counter()
    result_df = df.with_columns(
        [
            validate_phone(pl.col("phone")).alias("valid_strict"),
            validate_phone_flexible(pl.col("phone")).alias("valid_flexible"),
            format_phone(pl.col("phone")).alias("formatted"),
        ]
    )
    combined_time = time.perf_counter() - start_time

    throughput = size / combined_time
    print(f"    ⚡ Combined operations: {combined_time:.4f}s ({throughput:,.0f} records/sec)")

    return combined_time, throughput


def run_comprehensive_test():
    """Run comprehensive performance tests for all functions."""
    print("🚀 RustPy-Toolkit Comprehensive Performance Test")
    print("=" * 60)
    print("Testing CPF, CNPJ, and Phone validation/formatting functions")
    print("=" * 60)

    # Test sizes
    test_sizes = [50_000, 100_000, 250_000]

    all_results = []

    for size in test_sizes:
        print(f"\n🎯 Testing with {size:,} records each")
        print("=" * 40)

        # Test each module
        cpf_time, cpf_throughput = test_cpf_performance(size)
        cnpj_time, cnpj_throughput = test_cnpj_performance(size)
        phone_time, phone_throughput = test_phone_performance(size)

        # Overall statistics
        total_time = cpf_time + cnpj_time + phone_time
        total_records = size * 3  # 3 different data types
        overall_throughput = total_records / total_time

        print(f"\n📊 Overall Performance Summary ({size:,} records each):")
        print(f"  └─ CPF throughput: {cpf_throughput:,.0f} records/sec")
        print(f"  └─ CNPJ throughput: {cnpj_throughput:,.0f} records/sec")
        print(f"  └─ Phone throughput: {phone_throughput:,.0f} records/sec")
        print(f"  └─ Total time: {total_time:.4f}s")
        print(f"  └─ Overall throughput: {overall_throughput:,.0f} records/sec")

        all_results.append(
            {
                "size": size,
                "cpf_throughput": cpf_throughput,
                "cnpj_throughput": cnpj_throughput,
                "phone_throughput": phone_throughput,
                "overall_throughput": overall_throughput,
            }
        )

    # Final summary
    print("\n🎉 Final Performance Summary")
    print("=" * 40)

    for result in all_results:
        size = result["size"]
        print(f"\n{size:,} records:")
        print(f"  CPF:   {result['cpf_throughput']:>8,.0f} records/sec")
        print(f"  CNPJ:  {result['cnpj_throughput']:>8,.0f} records/sec")
        print(f"  Phone: {result['phone_throughput']:>8,.0f} records/sec")
        print(f"  Overall: {result['overall_throughput']:>6,.0f} records/sec")

    # Performance evaluation
    avg_throughput = sum(r["overall_throughput"] for r in all_results) / len(all_results)

    print("\n🎯 Performance Evaluation:")
    print(f"  Average overall throughput: {avg_throughput:,.0f} records/sec")

    if avg_throughput > 200_000:
        print("  🟢 EXCELLENT performance! Production ready.")
    elif avg_throughput > 100_000:
        print("  🟡 GOOD performance! Suitable for most use cases.")
    elif avg_throughput > 50_000:
        print("  🟠 ACCEPTABLE performance! May need optimization for large datasets.")
    else:
        print("  🔴 Performance needs improvement!")


def run_stress_test():
    """Run stress test with very large datasets."""
    print("\n🔥 Stress Test with Large Datasets")
    print("=" * 60)

    size = 500_000
    print(f"Testing with {size:,} records each (1.5M total records)")

    start_time = time.time()

    # Generate all data
    print("📊 Generating test data...")
    cpf_data = generate_cpf_data(size)
    cnpj_data = generate_cnpj_data(size)
    phone_data = generate_phone_data(size)

    generation_time = time.time() - start_time
    print(f"  Data generation: {generation_time:.2f}s")

    # Create DataFrames
    cpf_df = pl.DataFrame({"cpf": cpf_data})
    cnpj_df = pl.DataFrame({"cnpj": cnpj_data})
    phone_df = pl.DataFrame({"phone": phone_data})

    # Test all functions
    print("\n⚡ Running stress test...")

    test_start = time.time()

    # CPF operations
    cpf_result = cpf_df.with_columns(
        [validate_cpf_cnpj(pl.col("cpf")).alias("cpf_valid"), format_cpf_cnpj(pl.col("cpf")).alias("cpf_formatted")]
    )

    # CNPJ operations
    cnpj_result = cnpj_df.with_columns(
        [validate_cpf_cnpj(pl.col("cnpj")).alias("cnpj_valid"), format_cpf_cnpj(pl.col("cnpj")).alias("cnpj_formatted")]
    )

    # Phone operations
    phone_result = phone_df.with_columns(
        [
            validate_phone(pl.col("phone")).alias("phone_strict_valid"),
            validate_phone_flexible(pl.col("phone")).alias("phone_flexible_valid"),
            format_phone(pl.col("phone")).alias("phone_formatted"),
        ]
    )

    test_time = time.time() - test_start
    total_records = size * 3
    throughput = total_records / test_time

    print("\n🎯 Stress Test Results:")
    print(f"  └─ Processing time: {test_time:.2f}s")
    print(f"  └─ Total records processed: {total_records:,}")
    print(f"  └─ Throughput: {throughput:,.0f} records/second")
    print(f"  └─ Records per millisecond: {throughput / 1000:.1f}")

    # Validation statistics
    cpf_valid = cpf_result["cpf_valid"].sum()
    cnpj_valid = cnpj_result["cnpj_valid"].sum()
    phone_strict_valid = phone_result["phone_strict_valid"].sum()
    phone_flexible_valid = phone_result["phone_flexible_valid"].sum()

    print("\n📊 Validation Statistics:")
    print(f"  └─ CPF valid: {cpf_valid:,} / {size:,} ({cpf_valid / size * 100:.1f}%)")
    print(f"  └─ CNPJ valid: {cnpj_valid:,} / {size:,} ({cnpj_valid / size * 100:.1f}%)")
    print(f"  └─ Phone strict valid: {phone_strict_valid:,} / {size:,} ({phone_strict_valid / size * 100:.1f}%)")
    print(f"  └─ Phone flexible valid: {phone_flexible_valid:,} / {size:,} ({phone_flexible_valid / size * 100:.1f}%)")

    if throughput > 200_000:
        print("  ✅ EXCELLENT stress test performance!")
    elif throughput > 100_000:
        print("  ✅ GOOD stress test performance!")
    else:
        print("  ⚠️  Stress test performance could be improved")


if __name__ == "__main__":
    try:
        run_comprehensive_test()

        # Ask user if they want to run stress test
        print("\n❓ Run stress test with 500k records each? (y/N): ", end="")
        try:
            response = input().lower().strip()
            if response in ["y", "yes"]:
                run_stress_test()
        except (EOFError, KeyboardInterrupt):
            print("Skipping stress test.")

        print("\n🎉 Performance tests completed successfully!")
        print("\nTo run this test:")
        print("  uv run python tests/performance_test.py")

    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()
        raise
