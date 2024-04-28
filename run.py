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

def use_program():
    """
    The function to basically ask the user if he wants to use
    the program or not
    Y - Yes  / N - No
    and then proceed accordingly
    """
    counter = 0
    while True:
        user_input = input("Do you want to use the contact manager? (yes/no):\n").strip().lower()
        if user_input in ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly"):
            return True
        elif user_input in ("no", "n", "nah", "nope", "negative"):
            return False
        else:
            counter +=1
            print(f"\nI can do this all day. You've failed to give a correct answer {counter} times.")

def add_data_with_name_column(sheet, data):
    """
    Adds new data to the sheets with a predefined header
    If the sheet is empty, it sets a header row with its columns on A1 and B1
    as "Name" and "Telephone Number"
    
    Then it appends the data provided by the user to the sheet
    """
    existing_data = sheet.get_all_values()
    print(f"\nExisting data in {sheet.title} sheet:", existing_data)

    if not existing_data or not existing_data[0]:
        header_row = ["Name", "Telephone Number"]
        sheet.insert_row(header_row, index=1)
        sheet.format("A1:B1", {"textFormat": {"bold": True}})
    else:
        for row in data:
            sheet.append_row(row)

def protect_header(sheet):
    """
    Basically this function will pop an "alert" to the user if he tries to 
    delete the header row (Name, Telephone Number) - A1:B1
    """
    sheet_id = sheet.id
    requests = [{
        "addProtectedRange": {
            "protectedRange": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "warningOnly": True
            }
        }
    }]
    SHEET.batch_update({"requests": requests})


def check_duplicate_contact(name, number):
    """
    Checks if a contact already exists (name or tel number)
    in any of the sheets
    """
    for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
        contacts = sheet.get_all_records()
        for contact in contacts:
            if contact["Name"] == name or contact["Telephone Number"] == number:
                return True
    return False


def want_to_view_existing_contacts():
    """
    Asks the user if he wants to view existing contacts
    Returns True if he does, False otherwise
    """
    view_contacts = input("Do you want to view existing contacts? (Yes/No): ").strip().lower()
    if view_contacts in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap"]:
        return True
    else:
        return False



def view_existing_contacts():
    """
    Prompts the user if he wants to view existing contacts
    """
    while True:
        view_contacts = input("Do you want to view existing contacts? (Yes/No): ").strip().lower()
        if view_contacts in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly"]:
            print("Choose a category:")
            print("1. Personal")
            print("2. Professional")
            print("3. Emergency")
            print("4. Favorites")
            print("5. All")
            print("6. I don't want to")

            category_choice = input("Enter the number of the category you want to view: ")
            if category_choice == '1':
                print_sheet_data(personal_sheet)
                break
            elif category_choice == '2':
                print_sheet_data(professional_sheet)
                break
            elif category_choice == '3':
                print_sheet_data(emergency_sheet)
                break
            elif category_choice == '4':
                print_sheet_data(favorites_sheet)
                break
            elif category_choice == '5':
                print_sheet_data(personal_sheet)
                print_sheet_data(professional_sheet)
                print_sheet_data(emergency_sheet)
                print_sheet_data(favorites_sheet)
                break
            elif category_choice == '6':
                print("No problem. You can view contacts later.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        elif view_contacts in ["no", "n", "nah", "nope", "negative"]:
            print("No problem. You can view contacts later.")
            break
        else:
            print("Invalid choice. Please enter 'Yes' or 'No'.")


def want_to_add_contacts():
    """
    Asks the user if he wants to add new contacts
    Returns True if he does, False otherwise
    """
    add_contacts_input = input("\nDo you want to add new contacts? (Yes/No): ").strip().lower()
    return add_contacts_input in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly"]
            
            
def add_contacts():
    """
    Prompts the user to choose a category of contacts and adds new contacts
    to the selected category
    
    Displays options to the user to choose from one of each four from
    Personal - Professional - Emergency - Favorites
    And then the user has to enter the amount - number of contacts he wants to add
    including their names and tel. numbers
    
    Then adds the entered contacts to the correct sheet after checking for duplicates.
    """
    print("Which category would you like to add contacts to?")
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
    
    # _ acts as draft / placeholder variable (non main focus)
    for _ in range(num_contacts):
        name = input("Enter contact name: ")
        number = int(input("Enter contact number (only numbers): "))
        
        if check_duplicate_contact(name, number):
            print("Warning: This contact already exists.")
        else:
            add_data_with_name_column(sheet, [[name, number]])
            print("Contact added successfully.")


   
  
def print_sheet_data(sheet):
    """
    Prints the data from a specified sheet.
    """
    sheet_data = sheet.get_all_values()
    print(f"\n{sheet.title} Contacts:")
    for row in sheet_data:
        print(row)
 
   
    
def main():
    if not use_program():
        print("Exiting the program.")
        return
    
    print("Great! Let's proceed with the program.\n")
    
    view_existing_contacts()
    
    if want_to_add_contacts():
        add_contacts()
    
    # Add data for all sheets
    add_data_with_name_column(personal_sheet, personal_data)
    add_data_with_name_column(professional_sheet, professional_data)
    add_data_with_name_column(emergency_sheet, emergency_data)
    add_data_with_name_column(favorites_sheet, favorites_data)
    
    # Protect header for all sheets
    protect_header(personal_sheet)
    protect_header(professional_sheet)
    protect_header(emergency_sheet)
    protect_header(favorites_sheet)
    
    # Prints data from each sheet
    print_sheet_data(personal_sheet)
    print_sheet_data(professional_sheet)
    print_sheet_data(emergency_sheet)
    print_sheet_data(favorites_sheet)


if __name__ == "__main__":
    main()

