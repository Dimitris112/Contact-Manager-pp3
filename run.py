import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("contact_manager")

personal_sheet = SHEET.worksheet("Personal")
professional_sheet = SHEET.worksheet("Professional")
emergency_sheet = SHEET.worksheet("Emergency")
favorites_sheet = SHEET.worksheet("Favorites")

personal_data = []

professional_data = []

emergency_data = []

favorites_data = []

def add_data_with_name_column(sheet, data):
    """
    Adds new data to the sheets with a predefined header
    If the sheet is empty, it sets a header row with its columns on A1 and B1
    as "Name" and "Telephone Number"
    
    Then it appends the data provided by the user to the sheet
    """
    existing_data = sheet.get_all_values()
    print("Existing data:", existing_data)

    if not existing_data or not existing_data[0]:
        header_row = ["Name", "Telephone Number"]
        sheet.insert_row(header_row, index=1)
        header_range = sheet.range("A1:B1")
        for cell in header_range:
            cell.textFormat['bold'] = True
        sheet.update_cells(header_range)
    else:
        for row in data:
            sheet.append_row(row)