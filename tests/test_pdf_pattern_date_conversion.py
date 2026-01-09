"""Tests for PDF pattern date conversion."""

import pytest

from src.pdf_pattern_analyzer import PDFPattern, PDFPatternAnalyzer


class TestDateConversion:
    """Test cases for date format conversion."""

    @pytest.mark.parametrize(
        "input_date,expected_yy_mm_dd",
        [
            ("25.12.18", "18-12-25"),
            ("26.01.02", "02-01-26"),
            ("25.12.19", "19-12-25"),
            ("01.01.20", "20-01-01"),
            ("31.12.99", "99-12-31"),
        ],
    )
    def test_date_conversion_dd_mm_yy_to_yy_mm_dd(
        self, input_date: str, expected_yy_mm_dd: str
    ) -> None:
        """Test conversion from DD.MM.YY to YY-MM-DD format."""
        pattern = PDFPattern(
            date=input_date,
            dr_prefix="DR",
            project_number="12345",
            invoice_id="INV001",
            line_item="100",
            vendor="TestVendor",
            original_filename="test.pdf",
        )
        assert pattern.date_yy_mm_dd() == expected_yy_mm_dd

    def test_date_in_string_representation(self) -> None:
        """Test that string representation uses YY-MM-DD format."""
        pattern = PDFPattern(
            date="25.12.18",
            dr_prefix="DR",
            project_number="418500-10",
            invoice_id="I7495694",
            line_item="7063",
            vendor="Franklin",
            original_filename="test.pdf",
        )
        result = str(pattern)
        assert "18-12-25" in result
        assert "25.12.18" not in result  # Original format should not appear
