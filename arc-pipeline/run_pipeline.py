from sheets.sheets_client import (
    get_new_rows,
    mark_processing,
    update_row
)
from agents.research_match import analyze_website
from agents.draft import generate_draft
from gmail.draft_creator import create_gmail_draft
from datetime import datetime


def run():
    rows = get_new_rows()

    if not rows:
        print("No NEW rows found.")
        return

    for row in rows:
        row_number = row["row_number"]
        website_url = row["website_url"]
        receiver_email = row["receiver_email"]

        try:
            print(f"Processing row {row_number}...")
            mark_processing(row_number)

            research = analyze_website(website_url)

            update_row(row_number, {
                "H": research["company_name"],
                "I": research["industry"],
                "J": research["region"],
                "K": research["company_summary"],
                "L": research["match_decision"],
                "M": research["match_reason"],
            })

            if research["match_decision"] != "YES":
                update_row(row_number, {
                    "E": "REJECTED"
                })
                print(f"Row {row_number} rejected.")
                continue

            draft = generate_draft(
                company_name=research["company_name"],
                industry=research["industry"],
                region=research["region"],
                company_summary=research["company_summary"],
                receiver_email=receiver_email
            )

            update_row(row_number, {
                "N": draft["draft_subject"],
                "O": draft["draft_body"],
                "P": datetime.utcnow().isoformat(),
                "E": "DRAFTED"
            })

            gmail = create_gmail_draft(
                receiver_email=receiver_email,
                subject=draft["draft_subject"],
                body=draft["draft_body"]
            )

            update_row(row_number, {
                "Q": gmail["gmail_draft_id"],
                "R": gmail["gmail_draft_link"],
                "S": datetime.utcnow().isoformat(),
                "E": "GMAIL_DRAFT_CREATED"
            })

            print(f"Row {row_number} completed.")

        except Exception as e:
            update_row(row_number, {
                "E": "ERROR",
                "G": str(e)
            })
            print(f"Error on row {row_number}: {e}")


if __name__ == "__main__":
    run()
