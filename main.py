from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS (VERY IMPORTANT as per question)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):

    # 1️⃣ Ticket Status
    ticket_match = re.search(r"ticket (\d+)", q, re.IGNORECASE)
    if "status" in q.lower() and ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": ticket_id
            })
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.search(
        r"on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.",
        q,
        re.IGNORECASE
    )
    if "schedule" in q.lower() and meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        meeting_room = meeting_match.group(3)

        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": meeting_room
            })
        }

    # 3️⃣ Expense Balance
    expense_match = re.search(r"employee (\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": employee_id
            })
        }

    # 4️⃣ Performance Bonus
    bonus_match = re.search(r"employee (\d+).*?(\d{4})", q, re.IGNORECASE)
    if "bonus" in q.lower() and bonus_match:
        employee_id = int(bonus_match.group(1))
        current_year = int(bonus_match.group(2))
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": employee_id,
                "current_year": current_year
            })
        }

    # 5️⃣ Report Office Issue
    issue_match = re.search(
        r"issue (\d+) for the (.+?) department",
        q,
        re.IGNORECASE
    )
    if "report" in q.lower() and issue_match:
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2)
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": issue_code,
                "department": department
            })
        }

    return {"error": "Query not recognized"}
