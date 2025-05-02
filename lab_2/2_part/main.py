import argparse
import math
import os

from scipy.special import gammainc

from consts import (
    TEST_RESULTS_CPP,
    TEST_RESULTS_JAVA,
    TEST_RESULTS_PYTHON,
    PI,
)


def ensure_dirs_exist():
    """
    Create result dirs if needed.
    :return: None
    """
    os.makedirs(os.path.dirname(TEST_RESULTS_CPP), exist_ok=True)
    os.makedirs(os.path.dirname(TEST_RESULTS_JAVA), exist_ok=True)
    os.makedirs(os.path.dirname(TEST_RESULTS_PYTHON), exist_ok=True)


def read_sequence(path):
    """
    Read binary sequence from file.
    :param path: str — file path
    :return: str — sequence or '' on error
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except IOError as e:
        print(f"Error reading {path}: {e}")
        return ""


def write_result(path, text):
    """
    Write report to file.
    :param path: str — output path
    :param text: str — content
    :return: None
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    except IOError as e:
        print(f"Error writing {path}: {e}")


def monobit_test(seq):
    """
    Monobit test.
    :param seq: str — binary sequence
    :return: float — p-value
    """
    n = len(seq)
    if n == 0:
        return 0.0
    ones = seq.count('1')
    zeros = n - ones
    s = abs(ones - zeros)
    return math.erfc(s / math.sqrt(2 * n))


def runs_test(seq):
    """
    Runs (consecutive bits) test.
    :param seq: str — binary sequence
    :return: float — p-value
    """
    n = len(seq)
    if n < 2:
        return 0.0
    pi = seq.count('1') / n
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0
    runs = sum(1 for i in range(1, n) if seq[i] != seq[i - 1])
    num = abs(runs - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    return math.erfc(num / den)


def longest_run_test(seq):
    """
    Longest run of ones in 8-bit blocks.
    :param seq: str — binary sequence
    :return: float — p-value
    :raises ValueError: if len(seq) < 128
    """
    n = len(seq)
    if n < 128:
        raise ValueError("Sequence must be ≥128 bits.")
    counts = [0, 0, 0, 0]
    for i in range(n // 8):
        block = seq[i*8:(i+1)*8]
        max_run = cur = 0
        for b in block:
            if b == '1':
                cur += 1
                max_run = max(max_run, cur)
            else:
                cur = 0
        if max_run <= 1:
            counts[0] += 1
        elif max_run == 2:
            counts[1] += 1
        elif max_run == 3:
            counts[2] += 1
        else:
            counts[3] += 1
    chi2 = sum((counts[i] - 16 * PI[i])**2 / (16 * PI[i]) for i in range(4))
    return gammainc(1.5, chi2 / 2)


def run_all(label, seq_path, result_path):
    """
    Run all NIST tests and write report.
    :param label: str — sequence label
    :param seq_path: str — input file path
    :param result_path: str — output file path
    :return: None
    """
    seq = read_sequence(seq_path)
    if not seq:
        return
    try:
        p1 = monobit_test(seq)
        p2 = runs_test(seq)
        p3 = longest_run_test(seq)
    except ValueError as e:
        print(f"{label}: {e}")
        return
    report = (
        f"{label} Sequence Test Results\n"
        f"{'-' * 30}\n"
        f"Length: {len(seq)} bits\n\n"
        f"1) Monobit P-value:             {p1:.6f}\n"
        f"2) Runs P-value:                {p2:.6f}\n"
        f"3) Longest Run P-value:         {p3:.6f}\n"
    )
    write_result(result_path, report)


def main():
    """
    Main entry point.
    :return: None
    """
    parser = argparse.ArgumentParser(description="Run NIST tests on binary sequences.")
    parser.add_argument(
        "--cpp",
        metavar="FILE",
        required=True,
        help="path to C++ sequence file (required)",
    )
    parser.add_argument(
        "--java",
        metavar="FILE",
        required=True,
        help="path to Java sequence file (required)",
    )
    parser.add_argument(
        "--python",
        metavar="FILE",
        required=True,
        help="path to Python sequence file (required)",
    )
    args = parser.parse_args()

    ensure_dirs_exist()
    run_all("C++", args.cpp, TEST_RESULTS_CPP)
    run_all("Java", args.java, TEST_RESULTS_JAVA)
    run_all("Python", args.python, TEST_RESULTS_PYTHON)


if __name__ == "__main__":
    main()
