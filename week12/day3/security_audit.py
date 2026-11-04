import os
import re
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime


# -----------------------------------
# 1. Configuration
# -----------------------------------

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__",
    "node_modules", "site-packages", "outputs"
}

SCANNED_EXTENSIONS = {
    ".py", ".js", ".ts", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".env", ".txt", ".sql"
}

MAX_FILE_SIZE = 1_000_000  # 1 MB


# -----------------------------------
# 2. Security patterns
# -----------------------------------

RULES = [
    {
        "name": "Possible hardcoded credential",
        "pattern": re.compile(
            r"""(?i)\b(api[_-]?key|secret[_-]?key|password|passwd|access[_-]?token)\b"""
            r"""\s*[:=]\s*["'][^"'\s]{6,}["']"""
        ),
        "severity": "High",
        "recommendation": "Move credentials to environment variables or a secret manager."
    },
    {
        "name": "Possible AWS access key",
        "pattern": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "severity": "Critical",
        "recommendation": "Revoke exposed credentials and use a secure IAM role."
    },
    {
        "name": "Unsafe eval or exec usage",
        "pattern": re.compile(r"\b(eval|exec)\s*\("),
        "severity": "High",
        "recommendation": "Avoid executing dynamic input. Use safe parsing alternatives."
    },
    {
        "name": "Subprocess shell execution",
        "pattern": re.compile(r"subprocess\.\w+\([^)]*shell\s*=\s*True"),
        "severity": "High",
        "recommendation": "Avoid shell=True where possible. Pass command arguments as a list."
    },
    {
        "name": "Unsafe pickle loading",
        "pattern": re.compile(r"pickle\.load\s*\("),
        "severity": "High",
        "recommendation": "Only load trusted pickle files. Prefer safer model/data formats where practical."
    },
    {
        "name": "Debug mode enabled",
        "pattern": re.compile(r"(?i)\bdebug\s*=\s*True\b"),
        "severity": "Medium",
        "recommendation": "Disable debug mode in production."
    },
    {
        "name": "Permissive CORS configuration",
        "pattern": re.compile(r"""allow_origins\s*=\s*\[\s*["']\*["']\s*\]"""),
        "severity": "High",
        "recommendation": "Restrict CORS to trusted application origins."
    },
    {
        "name": "Potential unsafe SQL construction",
        "pattern": re.compile(
            r"""(?i)(execute|executemany)\s*\(\s*(f["']|["'][^"']*["']\s*\+)"""
        ),
        "severity": "High",
        "recommendation": "Use parameterized SQL queries instead of string interpolation."
    },
    {
        "name": "Unsafe YAML loading",
        "pattern": re.compile(r"yaml\.load\s*\("),
        "severity": "Medium",
        "recommendation": "Use yaml.safe_load for untrusted YAML input."
    }
]


# -----------------------------------
# 3. Helper functions
# -----------------------------------

def add_finding(findings, file_name, line_number,
                issue, severity, recommendation):

    findings.append({
        "file": file_name,
        "line": line_number,
        "issue": issue,
        "severity": severity,
        "recommendation": recommendation
    })


def get_project_files(target):
    files = []

    for root, dirs, filenames in os.walk(target):
        dirs[:] = [
            directory for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in filenames:
            path = Path(root) / filename

            if path.suffix.lower() in SCANNED_EXTENSIONS:
                try:
                    if path.stat().st_size <= MAX_FILE_SIZE:
                        files.append(path)
                except OSError:
                    pass

    return files


# -----------------------------------
# 4. Audit project files
# -----------------------------------

def run_audit(target):

    findings = []
    scanned_files = get_project_files(target)

    for file_path in scanned_files:

        relative_path = str(file_path.relative_to(target))

        # Check sensitive filenames
        lower_name = file_path.name.lower()

        if lower_name == ".env":
            add_finding(
                findings, relative_path, 0,
                "Environment file present in project",
                "High",
                "Ensure .env is excluded from Git and secrets are stored securely."
            )

        if lower_name in {
            "credentials.json",
            "service-account.json",
            "id_rsa",
            "private.key"
        }:
            add_finding(
                findings, relative_path, 0,
                "Potential sensitive credential file",
                "High",
                "Remove private credentials from source control and rotate exposed secrets."
            )

        # Read source text
        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except OSError:
            continue

        # Scan each line
        for line_number, line in enumerate(content.splitlines(), start=1):

            # Skip comments for common source formats
            stripped = line.strip()

            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            for rule in RULES:
                if rule["pattern"].search(line):
                    add_finding(
                        findings,
                        relative_path,
                        line_number,
                        rule["name"],
                        rule["severity"],
                        rule["recommendation"]
                    )

    # Check Git ignore configuration
    gitignore = Path(target) / ".gitignore"

    if not gitignore.exists():
        add_finding(
            findings,
            ".gitignore",
            0,
            "Missing .gitignore file",
            "Medium",
            "Add .gitignore rules for .env, virtual environments and generated files."
        )
    else:
        ignore_text = gitignore.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        if ".env" not in ignore_text:
            add_finding(
                findings,
                ".gitignore",
                0,
                "Environment file not explicitly ignored",
                "High",
                "Add .env to .gitignore and verify it is not already tracked by Git."
            )

    # Check dependency manifest
    requirements = Path(target) / "requirements.txt"
    pyproject = Path(target) / "pyproject.toml"

    if not requirements.exists() and not pyproject.exists():
        add_finding(
            findings,
            "Project root",
            0,
            "No Python dependency manifest found",
            "Low",
            "Maintain a dependency manifest and review dependencies for vulnerabilities."
        )

    return findings, len(scanned_files)


# -----------------------------------
# 5. Generate reports
# -----------------------------------

def generate_reports(findings, scanned_count):

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    severity_order = ["Critical", "High", "Medium", "Low"]

    counts = {
        severity: sum(
            1 for finding in findings
            if finding["severity"] == severity
        )
        for severity in severity_order
    }

    summary = {
        "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files_scanned": scanned_count,
        "total_findings": len(findings),
        "severity_breakdown": counts,
        "audit_type": "Static code and configuration review",
        "limitations": [
            "Does not perform penetration testing.",
            "Pattern matching may produce false positives.",
            "Does not verify whether dependencies contain known vulnerabilities.",
            "Does not prove that secrets are absent from Git history."
        ]
    }

    # CSV report
    csv_path = output_dir / "security_findings.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "file", "line", "issue",
                "severity", "recommendation"
            ]
        )
        writer.writeheader()
        writer.writerows(findings)

    # JSON summary
    json_path = output_dir / "security_summary.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    # Markdown report
    report_path = output_dir / "security_audit_report.md"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("# Data Platform Security Audit\n\n")
        file.write(f"Audit date: {summary['audit_date']}\n\n")
        file.write(f"Files scanned: {scanned_count}\n\n")
        file.write(f"Total findings: {len(findings)}\n\n")

        file.write("## Severity Summary\n\n")

        for severity, count in counts.items():
            file.write(f"- {severity}: {count}\n")

        file.write("\n## Findings\n\n")

        if not findings:
            file.write("No matching security patterns were detected.\n")
        else:
            for index, finding in enumerate(findings, start=1):
                file.write(f"### Finding {index}: {finding['issue']}\n\n")
                file.write(f"- File: `{finding['file']}`\n")
                file.write(f"- Line: {finding['line']}\n")
                file.write(f"- Severity: {finding['severity']}\n")
                file.write(
                    f"- Recommendation: {finding['recommendation']}\n\n"
                )

        file.write("\n## Limitations\n\n")

        for limitation in summary["limitations"]:
            file.write(f"- {limitation}\n")

    return summary


# -----------------------------------
# 6. Main
# -----------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Static security audit for a data platform project."
    )

    parser.add_argument(
        "--target",
        default=".",
        help="Project folder to audit."
    )

    args = parser.parse_args()

    target = Path(args.target).resolve()

    if not target.exists() or not target.is_dir():
        raise SystemExit("Error: Target must be an existing directory.")

    findings, scanned_count = run_audit(target)
    summary = generate_reports(findings, scanned_count)

    print("\nDATA PLATFORM SECURITY AUDIT")
    print("--------------------------------")
    print(f"Files scanned: {scanned_count}")
    print(f"Total findings: {summary['total_findings']}")

    for severity, count in summary["severity_breakdown"].items():
        print(f"{severity}: {count}")

    print("\nReports generated:")
    print("outputs/security_findings.csv")
    print("outputs/security_summary.json")
    print("outputs/security_audit_report.md")