from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = ""):

    # 1️⃣ Ticket Status
    ticket_match = re.search(r"ticket\s+(\d+)", q, re.IGNORECASE)
    if ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps(
                {"ticket_id": int(ticket_match.group(1))},
                separators=(",", ":")
            )
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)",
        q,
        re.IGNORECASE
    )
    if meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps(
                {
                    "date": meeting_match.group(1),
                    "time": meeting_match.group(2),
                    "meeting_room": meeting_match.group(3).rstrip(".")
                },
                separators=(",", ":")
            )
        }

    # 3️⃣ Expense Balance
    expense_match = re.search(r"expense.*?employee\s+(\d+)", q, re.IGNORECASE)
    if expense_match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps(
                {"employee_id": int(expense_match.group(1))},
                separators=(",", ":")
            )
        }

    # 4️⃣ Performance Bonus
    bonus_match = re.search(
        r"bonus.*?employee\s+(\d+).*?(\d{4})",
        q,
        re.IGNORECASE
    )
    if bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps(
                {
                    "employee_id": int(bonus_match.group(1)),
                    "current_year": int(bonus_match.group(2))
                },
                separators=(",", ":")
            )
        }

    # 5️⃣ Report Office Issue
    issue_match = re.search(
        r"issue\s+(\d+).*?department\s+(.+)",
        q,
        re.IGNORECASE
    )
    if issue_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps(
                {
                    "issue_code": int(issue_match.group(1)),
                    "department": issue_match.group(2).rstrip(".")
                },
                separators=(",", ":")
            )
        }

    # If nothing matches, return valid JSON (never empty name)
    return {
        "name": "unknown_function",
        "arguments": "{}"
    }
