# PDF Filename Pattern Analysis Report

## Summary

- **Total PDF files:** 5
- **Successfully parsed:** 5
- **Failed to parse:** 0

## Pattern Structure

The PDF filenames follow this pattern:
```
DD.MM.YY - DR - PROJECT_NUMBER - INVOICE_ID - LINE_ITEM - VENDOR.pdf
```

### Pattern Components:
1. **Date (DD.MM.YY)**: Date in day.month.year format (2-digit year), displayed as YY-MM-DD in output
2. **DR**: Constant prefix (likely 'DR' for company identifier)
3. **Project Number**: Project or order number (may include hyphens)
4. **Invoice ID**: Invoice identifier (may start with letter prefix)
5. **Line Item**: Line item or sequence number
6. **Vendor**: Vendor/supplier name

## Statistics

### Vendors
- **Unique vendors:** 3
- **Vendor list:** Franklin, Guillevin, Wesco

**Vendor distribution:**
- Franklin: 2 file(s)
- Guillevin: 2 file(s)
- Wesco: 1 file(s)

### Dates
- **Unique dates:** 3
- **Date range:** 02-01-26 to 19-12-25
- **Dates:** 02-01-26, 18-12-25, 19-12-25

### Projects
- **Unique projects:** 3
- **Projects:** 18999, 418500-10, 68209

### Invoice IDs
- **Unique invoice IDs:** 5
- **Invoice IDs:** 021336, 8522940, 8522975, I7495694, I7495700

## Detailed File Breakdown

### 26.01.02 - DR - 18999 - 8522940 - 7078 - Guillevin.pdf
- Date: `02-01-26`
- Project: `18999`
- Invoice ID: `8522940`
- Line Item: `7078`
- Vendor: `Guillevin`

### 25.12.18 - DR - 418500-10 - I7495700 - 7121 - Franklin.pdf
- Date: `18-12-25`
- Project: `418500-10`
- Invoice ID: `I7495700`
- Line Item: `7121`
- Vendor: `Franklin`

### 26.01.02 - DR - 18999 - 8522975 - 7167 - Guillevin.pdf
- Date: `02-01-26`
- Project: `18999`
- Invoice ID: `8522975`
- Line Item: `7167`
- Vendor: `Guillevin`

### 25.12.18 - DR - 418500-10 - I7495694 - 7063 - Franklin.pdf
- Date: `18-12-25`
- Project: `418500-10`
- Invoice ID: `I7495694`
- Line Item: `7063`
- Vendor: `Franklin`

### 25.12.19 - DR - 68209 - 021336 - BM14278 - Wesco.pdf
- Date: `19-12-25`
- Project: `68209`
- Invoice ID: `021336`
- Line Item: `BM14278`
- Vendor: `Wesco`
