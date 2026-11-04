# Security Audit on Data Platform

## Objective
Perform a static security review of a data platform project
to identify common security weaknesses and recommend improvements.

## Technologies
- Python
- Regular Expressions
- JSON
- CSV
- Python Standard Library

## Security Checks
1. Possible hardcoded credentials
2. Exposed environment files
3. Sensitive credential files
4. Unsafe eval() and exec() usage
5. Subprocess shell execution
6. Unsafe pickle loading
7. Debug mode configuration
8. Permissive CORS settings
9. Potential unsafe SQL construction
10. Unsafe YAML loading
11. Missing .gitignore configuration
12. Missing dependency manifest

## Execution

Run against a target project:

    python security_audit.py --target "..\executive_reports"

## Generated Reports
- security_findings.csv
- security_summary.json
- security_audit_report.md

## Review Process
1. Select the target project.
2. Scan source and configuration files.
3. Identify matching security patterns.
4. Categorize findings by severity.
5. Generate audit reports.
6. Review findings and apply appropriate fixes.

## Limitations
This is a static security review.
It does not perform penetration testing, network scanning,
dependency vulnerability verification, or a complete Git-history scan.

## Conclusion
The project demonstrates how Python can automate basic
security checks and generate structured security audit reports.