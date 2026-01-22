import csv
import json
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("issues.csv")
JSON_FILE = Path("issues.json")

ALLOWED_TYPES = ["software", "hardware", "network"]


def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_issue_type(value: str) -> str:
    return value.strip().lower()


def validate_issue(issue_type: str, description: str) -> tuple[bool, str]:
    if issue_type not in ALLOWED_TYPES:
        return False, f"Invalid issue type. Use one of: {', '.join(ALLOWED_TYPES)}"
    if not description.strip():
        return False, "Description cannot be empty."
    if len(description.strip()) < 5:
        return False, "Description is too short (min 5 characters)."
    return True, ""


def ensure_csv_header():
    """Create CSV with header if it doesn't exist."""
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "type", "description"])


def save_to_csv(issue: dict):
    ensure_csv_header()
    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([issue["datetime"], issue["type"], issue["description"]])


def load_json() -> list[dict]:
    if not JSON_FILE.exists():
        return []
    try:
        with JSON_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_to_json(issue: dict):
    data = load_json()
    data.append(issue)
    with JSON_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def log_issue():
    print("\nLog new issue")
    print("-------------")
    raw_type = input("Issue type (software/hardware/network): ")
    issue_type = normalize_issue_type(raw_type)
    description = input("Short description: ").strip()

    ok, err = validate_issue(issue_type, description)
    if not ok:
        print(f"\n❌ {err}\n")
        return

    issue = {
        "datetime": now_ts(),
        "type": issue_type,
        "description": description
    }

    save_to_csv(issue)
    save_to_json(issue)
    print("\n✅ Issue logged successfully (saved to CSV + JSON).\n")


def read_issues_from_csv() -> list[dict]:
    if not CSV_FILE.exists():
        return []
    with CSV_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def print_issues(issues: list[dict]):
    if not issues:
        print("\nNo issues found.\n")
        return

    print("\nLogged issues")
    print("------------")
    for i, item in enumerate(issues, start=1):
        dt = item.get("datetime", "")
        t = item.get("type", "")
        desc = item.get("description", "")
        print(f"{i}. [{dt}] ({t}) {desc}")
    print("")


def view_issues():
    issues = read_issues_from_csv()
    print_issues(issues)


def filter_issues():
    issues = read_issues_from_csv()
    if not issues:
        print("\nNo issues logged yet.\n")
        return

    print("\nFilter issues")
    print("-------------")
    print("1. Filter by type")
    print("2. Filter by keyword (in description)")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        t = normalize_issue_type(input("Type (software/hardware/network): "))
        if t not in ALLOWED_TYPES:
            print(f"\n❌ Invalid type. Use: {', '.join(ALLOWED_TYPES)}\n")
            return
        filtered = [x for x in issues if x.get("type", "").strip().lower() == t]
        print_issues(filtered)

    elif choice == "2":
        keyword = input("Keyword: ").strip().lower()
        if not keyword:
            print("\n❌ Keyword cannot be empty.\n")
            return
        filtered = [x for x in issues if keyword in x.get("description", "").lower()]
        print_issues(filtered)

    else:
        print("\n❌ Invalid option.\n")


def main():
    print("IT Issue Logger")
    print("===============")

    while True:
        print("1. Log new issue")
        print("2. View all issues")
        print("3. Search / filter issues")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_issue()
        elif choice == "2":
            view_issues()
        elif choice == "3":
            filter_issues()
        elif choice == "4":
            print("\nGoodbye!\n")
            break
        else:
            print("\n❌ Invalid choice.\n")


if __name__ == "__main__":
    main()
