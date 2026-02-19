import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

def get_pilots():
    sheet = client.open_by_key("1QC2b6VSpenTGbiAEgLYomhEOJbWa3v5_BHa0eh8OAJQ").worksheet("pilot_roster")
    return sheet.get_all_records()

def get_drones():
    sheet = client.open_by_key("1QC2b6VSpenTGbiAEgLYomhEOJbWa3v5_BHa0eh8OAJQ").worksheet("drone_fleet")
    return sheet.get_all_records()
def get_missions():
    sheet = client.open_by_key("1QC2b6VSpenTGbiAEgLYomhEOJbWa3v5_BHa0eh8OAJQ").worksheet("missions")
    return sheet.get_all_records()

def update_pilot_status(pilot_id, new_status):
    sheet = client.open_by_key("1QC2b6VSpenTGbiAEgLYomhEOJbWa3v5_BHa0eh8OAJQ").worksheet("pilot_roster")

    records = sheet.get_all_records()

    for i, row in enumerate(records):
        if row["pilot_id"] == pilot_id:
            sheet.update_cell(i + 2, 6, new_status)  # 6 = status column
            break


def update_drone_status(drone_id, new_status):
    sheet = client.open_by_key("1QC2b6VSpenTGbiAEgLYomhEOJbWa3v5_BHa0eh8OAJQ").worksheet("drone_fleet")

    records = sheet.get_all_records()

    for i, row in enumerate(records):
        if row["drone_id"] == drone_id:
            sheet.update_cell(i + 2, 4, new_status)  # 4 = status column
            break


