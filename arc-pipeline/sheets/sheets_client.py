from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.modify"
]


SPREADSHEET_ID = "1kKGx45db5j0LtkmLn8Q06dT0mNXV2MH5qRONTWtmweA"
SHEET_NAME = "Sheet1"


def get_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    return service


def get_new_rows():
    service = get_service()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:S"
    ).execute()

    values = result.get("values", [])
    if not values or len(values) < 2:
        return []

    headers = values[0]
    rows = values[1:]

    status_index = headers.index("status")
    website_index = headers.index("website_url")
    email_index = headers.index("receiver_email")

    new_rows = []

    for i, row in enumerate(rows, start=2):
        status = row[status_index] if len(row) > status_index else ""
        if status == "NEW":
            new_rows.append({
                "row_number": i,
                "website_url": row[website_index] if len(row) > website_index else "",
                "receiver_email": row[email_index] if len(row) > email_index else ""
            })

    return new_rows


def mark_processing(row_number):
    service = get_service()
    sheet = service.spreadsheets()

    body = {
        "values": [[
            "PROCESSING",
            datetime.utcnow().isoformat()
        ]]
    }

    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!E{row_number}:F{row_number}",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()


def update_row(row_number, updates):
    service = get_service()
    sheet = service.spreadsheets()

    requests = []

    for col, value in updates.items():
        requests.append({
            "range": f"{SHEET_NAME}!{col}{row_number}",
            "values": [[value]]
        })

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": requests
    }

    sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()
