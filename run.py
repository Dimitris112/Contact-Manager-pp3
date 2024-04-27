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
            
def add_contacts():
    """
    Prompts the user to choose a category of contacts and adds new contacts
    to the selected category
    
    Displays options to the user to choose from one of each four from
    Personal - Professional - Emergency - Favorites
    And then the user has to enter the amount - number of contacts he wants to add
    including their names and tel. numbers
    
    Then adds the entered contacts to the correct sheet
    """
    print("Which sheet would you like to add contacts to?")
    print("Enter 'Per' for Personal, 'Pro' for Professional, 'Eme' for Emergency, or 'Fav' for Favorites:\n")
    
    while True:
        sheet_choice = input("Enter your choice: \n").capitalize()
        
        if sheet_choice in ['Per', 'Pro', 'Eme', 'Fav']:
            break
        else:
            print("Invalid choice. Please enter 'Per', 'Pro', 'Eme', or 'Fav'.")

    if sheet_choice == 'Per':
        sheet = personal_sheet
    elif sheet_choice == 'Pro':
        sheet = professional_sheet
    elif sheet_choice == 'Eme':
        sheet = emergency_sheet
    elif sheet_choice == 'Fav':
        sheet = favorites_sheet
    
    num_contacts = int(input("How many contacts would you like to add? "))
    
    new_contacts = []
    for _ in range(num_contacts):
        name = input("Enter contact name: ")
        number = input("Enter contact number: ")
        new_contacts.append([name, number])
    
    add_data_with_name_column(sheet, new_contacts)
    print("Contacts added successfully.")
    
   
  
def print_sheet_data(sheet):
    """
    Prints the data from a specified sheet.
    """
    sheet_data = sheet.get_all_values()
    print(sheet.title + " Contacts:")
    for row in sheet_data:
        print(row)  
 

def main():
    add_contacts()
    
      # Add data for all sheets
    add_data_with_name_column(personal_sheet, personal_data)
    add_data_with_name_column(professional_sheet, professional_data)
    add_data_with_name_column(emergency_sheet, emergency_data)
    add_data_with_name_column(favorites_sheet, favorites_data)
    
    # Prints data from each sheet
    print_sheet_data(personal_sheet)
    print_sheet_data(professional_sheet)
    print_sheet_data(emergency_sheet)
    print_sheet_data(favorites_sheet)

if __name__ == "__main__":
    main()