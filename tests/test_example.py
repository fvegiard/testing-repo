"""Tests for example module."""

import pytest

from src.example import add, divide, multiply


class TestAdd:
    """Test cases for add function."""

    def test_add_positive_numbers(self) -> None:
        """Test adding two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self) -> None:
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_zero(self) -> None:
        """Test adding with zero."""
        assert add(5, 0) == 5
        assert add(0, 5) == 5

    @pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (10, 20, 30), (-1, 1, 0)])
    def test_add_parametrized(self, a: int, b: int, expected: int) -> None:
        """Test add function with parametrized inputs."""
        assert add(a, b) == expected


class TestMultiply:
    """Test cases for multiply function."""

    def test_multiply_positive_numbers(self) -> None:
        """Test multiplying two positive numbers."""
        assert multiply(2, 3) == 6

    def test_multiply_by_zero(self) -> None:
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0

    def test_multiply_negative_numbers(self) -> None:
        """Test multiplying negative numbers."""
        assert multiply(-2, 3) == -6
        assert multiply(-2, -3) == 6


class TestDivide:
    """Test cases for divide function."""

    def test_divide_positive_numbers(self) -> None:
        """Test dividing two positive numbers."""
        assert divide(10, 2) == 5.0

    def test_divide_negative_numbers(self) -> None:
        """Test dividing negative numbers."""
        assert divide(-10, 2) == -5.0
        assert divide(-10, -2) == 5.0

    def test_divide_by_zero_raises_error(self) -> None:
        """Test that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_float_result(self) -> None:
        """Test that division can produce float results."""
        result = divide(1, 3)
        assert isinstance(result, float)
        assert abs(result - 0.3333333333333333) < 1e-10
