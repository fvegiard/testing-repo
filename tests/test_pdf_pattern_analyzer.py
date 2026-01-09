"""Tests for PDF pattern analyzer."""

import pytest
from pathlib import Path

from src.pdf_pattern_analyzer import PDFPattern, PDFPatternAnalyzer


class TestPDFPattern:
    """Test cases for PDFPattern dataclass."""

    def test_pattern_str_representation(self) -> None:
        """Test string representation of PDFPattern."""
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
        assert "25.12.18" in result
        assert "418500-10" in result
        assert "I7495694" in result
        assert "Franklin" in result


class TestPDFPatternAnalyzer:
    """Test cases for PDFPatternAnalyzer."""

    @pytest.mark.parametrize(
        "filename,expected",
        [
            (
                "25.12.18 - DR - 418500-10 - I7495694 - 7063 - Franklin.pdf",
                {
                    "date": "25.12.18",
                    "date_yy_mm_dd": "18-12-25",
                    "project": "418500-10",
                    "invoice_id": "I7495694",
                    "line_item": "7063",
                    "vendor": "Franklin",
                },
            ),
            (
                "26.01.02 - DR - 18999 - 8522940 - 7078 - Guillevin.pdf",
                {
                    "date": "26.01.02",
                    "date_yy_mm_dd": "02-01-26",
                    "project": "18999",
                    "invoice_id": "8522940",
                    "line_item": "7078",
                    "vendor": "Guillevin",
                },
            ),
            (
                "25.12.19 - DR - 68209 - 021336 - BM14278 - Wesco.pdf",
                {
                    "date": "25.12.19",
                    "date_yy_mm_dd": "19-12-25",
                    "project": "68209",
                    "invoice_id": "021336",
                    "line_item": "BM14278",
                    "vendor": "Wesco",
                },
            ),
        ],
    )
    def test_parse_valid_filename(self, filename: str, expected: dict) -> None:
        """Test parsing valid PDF filenames."""
        pattern = PDFPatternAnalyzer.parse_filename(filename)
        assert pattern is not None
        # Check original date format (DD.MM.YY)
        assert pattern.date == expected["date"]
        # Check converted date format (YY-MM-DD)
        assert pattern.date_yy_mm_dd() == expected.get("date_yy_mm_dd", expected["date"])
        assert pattern.project_number == expected["project"]
        assert pattern.invoice_id == expected["invoice_id"]
        assert pattern.line_item == expected["line_item"]
        assert pattern.vendor == expected["vendor"]
        assert pattern.dr_prefix == "DR"

    def test_parse_invalid_filename(self) -> None:
        """Test parsing invalid PDF filename."""
        pattern = PDFPatternAnalyzer.parse_filename("invalid_filename.pdf")
        assert pattern is None

    def test_parse_filename_without_pdf_extension(self) -> None:
        """Test that non-PDF files are not parsed."""
        pattern = PDFPatternAnalyzer.parse_filename(
            "25.12.18 - DR - 418500-10 - I7495694 - 7063 - Franklin.txt"
        )
        assert pattern is None

    def test_analyze_directory(self) -> None:
        """Test analyzing a directory of PDF files."""
        emails_dir = Path(__file__).parent.parent / "emails-project"
        if not emails_dir.exists():
            pytest.skip("emails-project directory not found")

        analysis = PDFPatternAnalyzer.analyze_directory(emails_dir)

        assert "total_pdfs" in analysis
        assert "successfully_parsed" in analysis
        assert "failed_parses" in analysis
        assert "patterns" in analysis
        assert "statistics" in analysis

        assert analysis["total_pdfs"] > 0
        assert len(analysis["patterns"]) == analysis["successfully_parsed"]

    def test_generate_report(self) -> None:
        """Test report generation."""
        emails_dir = Path(__file__).parent.parent / "emails-project"
        if not emails_dir.exists():
            pytest.skip("emails-project directory not found")

        analysis = PDFPatternAnalyzer.analyze_directory(emails_dir)
        report = PDFPatternAnalyzer.generate_report(analysis)

        assert isinstance(report, str)
        assert "PDF Filename Pattern Analysis Report" in report
        assert "Summary" in report
        assert "Pattern Structure" in report
        assert "Statistics" in report

        # Check that all parsed patterns are in the report
        for pattern in analysis["patterns"]:
            assert pattern.original_filename in report
            assert pattern.vendor in report
