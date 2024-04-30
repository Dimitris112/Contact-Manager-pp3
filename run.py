import gspread
import re
import csv
from google.oauth2.service_account import Credentials
# Not sure if I keep the CSV coz it's going to be updated along the way / after submission (possible) - bad

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

telephone_pattern =  r'^[\d+\-]+$'


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
        if user_input in ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly","ye", "ok", "okay", "okey"):
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


def view_existing_contacts():
    """
    Prompts the user if he wants to view existing contacts
    """
    counter = 0
    while True:
        view_contacts = input("Do you want to view existing contacts? (Yes/No):\n").strip().lower()
        if view_contacts in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly","ye", "ok", "okay", "okey"]:
            print("Choose a category:")
            print("1. Personal")
            print("2. Professional")
            print("3. Emergency")
            print("4. Favorites")
            print("5. All")
            print("6. I don't want to")

            category_choice = input("\nEnter the number of the category you want to view: ")
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
                print("\nNo problem. You can view contacts later.")
                break
            else:
                counter += 1
                print("Invalid choice. Please enter a number between 1 and 6.")
        elif view_contacts in ["no", "n", "nah", "nope", "negative"]:
            print("\nNo problem. You can view contacts later.")
            break
        else:
            counter += 1
            print(f"\nI can do this all day. You've failed to give a correct answer {counter} times.")




def add_contacts():
    """
    Prompts the user if he wants to add new contacts and adds them to the selected category.
    """
    while True:
        add_contacts_input = input("\nDo you want to add new contacts? (Yes/No): ").strip().lower()
        if add_contacts_input in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly","ye", "ok", "okay", "okey"]:
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
            
            while True:
                num_contacts_input = input("How many contacts would you like to add? (only numbers) ")
                if num_contacts_input.isdigit():
                    num_contacts = int(num_contacts_input)
                    break
                elif num_contacts_input.lower() == "esc":
                    print("Exiting the program.")
                    return
                else:
                    print("\nInvalid input. Please enter a number or type 'esc' to exit the program.")
            
            # _ acts as draft / placeholder variable (non main focus)
            for _ in range(num_contacts):
                name = input("Enter contact name: ")
                while True:
                    number = input("Enter contact number (only numbers, +, or -): ")
                    # Added regular expression for the telephone number - might just delete it later on and keep it to only to numbers
                    if re.match(r'^[\d\+\-]+$', number):
                        break
                    elif number.lower() == "esc":
                        print("Exiting the program.")
                        return
                    else:
                        print("Invalid telephone number. Please enter only numbers, +, or -.")
                
                if check_duplicate_contact(name, number):
                    print("Warning: This contact already exists.")
                else:
                    add_data_with_name_column(sheet, [[name, number]])
                    print("Contact added successfully.")
            
            break
        elif add_contacts_input in ["no", "n", "nah", "nope", "negative"]:
            print("No contacts added.")
            break
        elif add_contacts_input == "esc":
            print("Exiting the program.")
            return
        else:
            print("Invalid input. Please enter 'Yes' or 'No', or type 'esc' to exit the program.")



def read_existing_contacts():
    """
    Reads existing contacts data from the 'contacts.csv' file.
    """
    file_name = "contacts.csv"
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            existing_contacts = list(reader)
    except FileNotFoundError:
        existing_contacts = []
    return existing_contacts


def export_all_contacts():
    """
    Exports contacts from all categories to the 'contacts.csv' file.
    """
    all_contacts = []
    for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
        all_contacts += sheet.get_all_values()
    existing_contacts = read_existing_contacts()
    all_contacts += existing_contacts
    export_to_csv(all_contacts)


def export_to_csv(data):
    """
    Writes the contacts data to a CSV file named 'contacts.csv'.
    """
    file_name = "contacts.csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"\nContacts exported to '{file_name}' successfully.\n")


def export_contacts():
    """
    Exports contacts to the 'contacts.csv' file.
    """
    print("Which category would you like to export contacts from?\n")
    print("1. Personal")
    print("2. Professional")
    print("3. Emergency")
    print("4. Favorites")
    print("5. All")
    
    category_choice = input("\nEnter the number of the category you want to export:\n")
    if category_choice == '1':
        sheet = personal_sheet
    elif category_choice == '2':
        sheet = professional_sheet
    elif category_choice == '3':
        sheet = emergency_sheet
    elif category_choice == '4':
        sheet = favorites_sheet
    elif category_choice == '5':
        export_all_contacts()
        return
    else:
        print("Invalid choice. Please enter a number between 1 and 5.\n")
        return

    contacts = sheet.get_all_values()
    existing_contacts = read_existing_contacts()
    contacts += existing_contacts
    export_to_csv(contacts)
    



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

    export_contacts()


if __name__ == "__main__":
    main()


