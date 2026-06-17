import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "users.csv"

FIELD_LABELS = ("이름", "지역", "성별", "나이")


def parse_issue_body(body: str) -> dict[str, str]:
    fields = {}
    for label in FIELD_LABELS:
        pattern = rf"###\s*{label}\s*\n+([^\n#]+)"
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            fields[label] = match.group(1).strip()
    return fields


def validate_fields(fields: dict[str, str]) -> None:
    missing = [label for label in FIELD_LABELS if not fields.get(label)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")


def append_user(fields: dict[str, str]) -> None:
    users = []
    if CSV_PATH.exists():
        with CSV_PATH.open(encoding="utf-8", newline="") as f:
            users = list(csv.DictReader(f))

    for user in users:
        if user["이름"] == fields["이름"]:
            raise ValueError(f"User already exists: {fields['이름']}")

    users.append({label: fields[label] for label in FIELD_LABELS})

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(FIELD_LABELS))
        writer.writeheader()
        writer.writerows(users)


def main():
    body = os.environ.get("ISSUE_BODY", "")
    if not body and len(sys.argv) > 1:
        body = sys.argv[1]

    fields = parse_issue_body(body)
    validate_fields(fields)
    append_user(fields)
    print(f"Added user: {fields['이름']}")


if __name__ == "__main__":
    main()
