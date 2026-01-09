"""PDF filename pattern analyzer for invoice documents."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class PDFPattern:
    """Represents a parsed PDF filename pattern."""

    date: str  # DD.MM.YY format
    dr_prefix: str  # Should be "DR"
    project_number: str
    invoice_id: str
    line_item: str
    vendor: str
    original_filename: str

    def __str__(self) -> str:
        """Return formatted string representation."""
        return (
            f"Date: {self.date} | "
            f"Project: {self.project_number} | "
            f"Invoice: {self.invoice_id} | "
            f"Line: {self.line_item} | "
            f"Vendor: {self.vendor}"
        )


class PDFPatternAnalyzer:
    """Analyzes PDF filename patterns from invoice documents."""

    # Pattern: DD.MM.YY - DR - PROJECT - INVOICE - LINE - VENDOR.pdf
    # Line item can be numeric or alphanumeric (e.g., 7063 or BM14278)
    # Invoice ID can be numeric or alphanumeric (e.g., 8522940 or I7495694 or 021336)
    PATTERN = re.compile(
        r"^(\d{2}\.\d{2}\.\d{2})\s*-\s*DR\s*-\s*"
        r"(\d+(?:-\d+)?)\s*-\s*"
        r"([A-Z]*\d+)\s*-\s*"  # Invoice ID: optional letters + digits
        r"([A-Z]*\d+)\s*-\s*"  # Line Item: optional letters + digits
        r"([A-Za-z]+)\.pdf$"
    )

    @classmethod
    def parse_filename(cls, filename: str) -> Optional[PDFPattern]:
        """Parse a PDF filename and extract pattern components.

        Args:
            filename: The PDF filename to parse

        Returns:
            PDFPattern object if pattern matches, None otherwise
        """
        match = cls.PATTERN.match(filename)
        if not match:
            return None

        date, project, invoice_id, line_item, vendor = match.groups()

        return PDFPattern(
            date=date,
            dr_prefix="DR",
            project_number=project,
            invoice_id=invoice_id,
            line_item=line_item,
            vendor=vendor,
            original_filename=filename,
        )

    @classmethod
    def analyze_directory(cls, directory: Path) -> dict:
        """Analyze all PDF files in a directory.

        Args:
            directory: Path to directory containing PDF files

        Returns:
            Dictionary with analysis results
        """
        pdf_files = list(directory.glob("*.pdf"))
        parsed_patterns = []
        failed_parses = []

        for pdf_file in pdf_files:
            pattern = cls.parse_filename(pdf_file.name)
            if pattern:
                parsed_patterns.append(pattern)
            else:
                failed_parses.append(pdf_file.name)

        # Extract statistics
        vendors = [p.vendor for p in parsed_patterns]
        dates = [p.date for p in parsed_patterns]
        projects = [p.project_number for p in parsed_patterns]
        invoice_ids = [p.invoice_id for p in parsed_patterns]

        return {
            "total_pdfs": len(pdf_files),
            "successfully_parsed": len(parsed_patterns),
            "failed_parses": len(failed_parses),
            "failed_filenames": failed_parses,
            "patterns": parsed_patterns,
            "statistics": {
                "unique_vendors": sorted(set(vendors)),
                "unique_dates": sorted(set(dates)),
                "unique_projects": sorted(set(projects)),
                "unique_invoice_ids": sorted(set(invoice_ids)),
                "vendor_counts": {v: vendors.count(v) for v in set(vendors)},
            },
        }

    @classmethod
    def generate_report(cls, analysis: dict) -> str:
        """Generate a human-readable report from analysis.

        Args:
            analysis: Analysis dictionary from analyze_directory

        Returns:
            Formatted report string
        """
        report_lines = [
            "# PDF Filename Pattern Analysis Report\n",
            "## Summary\n",
            f"- **Total PDF files:** {analysis['total_pdfs']}",
            f"- **Successfully parsed:** {analysis['successfully_parsed']}",
            f"- **Failed to parse:** {analysis['failed_parses']}",
            "",
            "## Pattern Structure\n",
            "The PDF filenames follow this pattern:",
            "```",
            "DD.MM.YY - DR - PROJECT_NUMBER - INVOICE_ID - LINE_ITEM - VENDOR.pdf",
            "```",
            "",
            "### Pattern Components:",
            "1. **Date (DD.MM.YY)**: Date in day.month.year format (2-digit year)",
            "2. **DR**: Constant prefix (likely 'DR' for company identifier)",
            "3. **Project Number**: Project or order number (may include hyphens)",
            "4. **Invoice ID**: Invoice identifier (may start with letter prefix)",
            "5. **Line Item**: Line item or sequence number",
            "6. **Vendor**: Vendor/supplier name",
            "",
            "## Statistics\n",
        ]

        stats = analysis["statistics"]

        # Vendor statistics
        report_lines.extend([
            "### Vendors",
            f"- **Unique vendors:** {len(stats['unique_vendors'])}",
            f"- **Vendor list:** {', '.join(stats['unique_vendors'])}",
            "",
            "**Vendor distribution:**",
        ])
        for vendor, count in sorted(stats["vendor_counts"].items()):
            report_lines.append(f"- {vendor}: {count} file(s)")

        # Date statistics
        report_lines.extend([
            "",
            "### Dates",
            f"- **Unique dates:** {len(stats['unique_dates'])}",
            f"- **Date range:** {min(stats['unique_dates'])} to {max(stats['unique_dates'])}",
            f"- **Dates:** {', '.join(stats['unique_dates'])}",
            "",
        ])

        # Project statistics
        report_lines.extend([
            "### Projects",
            f"- **Unique projects:** {len(stats['unique_projects'])}",
            f"- **Projects:** {', '.join(stats['unique_projects'])}",
            "",
        ])

        # Invoice ID statistics
        report_lines.extend([
            "### Invoice IDs",
            f"- **Unique invoice IDs:** {len(stats['unique_invoice_ids'])}",
            f"- **Invoice IDs:** {', '.join(stats['unique_invoice_ids'])}",
            "",
        ])

        # Detailed breakdown
        report_lines.extend([
            "## Detailed File Breakdown\n",
        ])

        for pattern in analysis["patterns"]:
            report_lines.append(f"### {pattern.original_filename}")
            report_lines.append(f"- Date: `{pattern.date}`")
            report_lines.append(f"- Project: `{pattern.project_number}`")
            report_lines.append(f"- Invoice ID: `{pattern.invoice_id}`")
            report_lines.append(f"- Line Item: `{pattern.line_item}`")
            report_lines.append(f"- Vendor: `{pattern.vendor}`")
            report_lines.append("")

        # Failed parses
        if analysis["failed_parses"] > 0:
            report_lines.extend([
                "## Files That Failed to Parse\n",
                "The following files did not match the expected pattern:",
                "",
            ])
            for filename in analysis["failed_filenames"]:
                report_lines.append(f"- `{filename}`")
            report_lines.append("")

        return "\n".join(report_lines)


def main() -> None:
    """Main function to run the analysis."""
    emails_dir = Path(__file__).parent.parent / "emails-project"

    if not emails_dir.exists():
        print(f"Error: Directory not found: {emails_dir}")
        return

    print(f"Analyzing PDF files in: {emails_dir}\n")
    analysis = PDFPatternAnalyzer.analyze_directory(emails_dir)
    report = PDFPatternAnalyzer.generate_report(analysis)

    # Print report
    print(report)

    # Save report to file
    report_file = emails_dir / "pdf_pattern_analysis.md"
    report_file.write_text(report, encoding="utf-8")
    print(f"\n✅ Report saved to: {report_file}")


if __name__ == "__main__":
    main()
