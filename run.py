import gspread
import re
import csv
import time
import ascii_py
from google.oauth2.service_account import Credentials
# Not sure if I keep the CSV coz it's going to be updated along the way / after submission (possible) - bad

ascii_art = '''

      ...                                         s                               s                  
   xH88"`~ .x8X                                  :8                              :8                  
 :8888   .f"8888Hf        u.      u.    u.      .88                             .88                  
:8888>  X8L  ^""`   ...ue888b   x@88k u@88c.   :888ooo       u           .     :888ooo               
X8888  X888h        888R Y888r ^"8888""8888" -*8888888    us888u.   .udR88N  -*8888888               
88888  !88888.      888R I888>   8888  888R    8888    .@88 "8888" <888'888k   8888                  
88888   %88888      888R I888>   8888  888R    8888    9888  9888  9888 'Y"    8888                  
88888 '> `8888>     888R I888>   8888  888R    8888    9888  9888  9888        8888                  
`8888L %  ?888   ! u8888cJ888    8888  888R   .8888Lu= 9888  9888  9888       .8888Lu=               
 `8888  `-*""   /   "*888*P"    "*88*" 8888"  ^%888*   9888  9888  ?8888u../  ^%888*                 
   "888.      :"      'Y"         ""   'Y"      'Y"    "888*""888"  "8888P'     'Y"                  
     `""***~"`                                          ^Y"   ^Y'     "P'                            
                                                                                                     
                                                                                                     
                                                                                                     
    ...     ..      ..                                                                               
  x*8888x.:*8888: -"888:                                                                             
 X   48888X `8888H  8888                  u.    u.                                         .u    .   
X8x.  8888X  8888X  !888>        u      x@88k u@88c.       u          uL          .u     .d88B :@8c  
X8888 X8888  88888   "*8%-    us888u.  ^"8888""8888"    us888u.   .ue888Nc..   ud8888.  ="8888f8888r 
'*888!X8888> X8888  xH8>   .@88 "8888"   8888  888R  .@88 "8888" d88E`"888E` :888'8888.   4888>'88"  
  `?8 `8888  X888X X888>   9888  9888    8888  888R  9888  9888  888E  888E  d888 '88%"   4888> '    
  -^  '888"  X888  8888>   9888  9888    8888  888R  9888  9888  888E  888E  8888.+"      4888>      
   dx '88~x. !88~  8888>   9888  9888    8888  888R  9888  9888  888E  888E  8888L       .d888L .+   
 .8888Xf.888x:!    X888X.: 9888  9888   "*88*" 8888" 9888  9888  888& .888E  '8888c. .+  ^"8888*"    
:""888":~"888"     `888*"  "888*""888"    ""   'Y"   "888*""888" *888" 888&   "88888%       "Y"      
    "~'    "~        ""     ^Y"   ^Y'                 ^Y"   ^Y'   `"   "888E    "YP'                 
                                                                 .dWi   `88E                         
                                                                 4888~  J8%                          
                                                                  ^"===*"`                           

'''

print(ascii_art)
#Font Name: Fraktur - Contact Manager 
#https://patorjk.com/software/taag/#p=display&f=Fraktur&t=Contact%0AManager


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

            category_choice = input("\nEnter the number of the category you want to view:\n")
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
            print("Enter 'Per' for Personal, 'Pro' for Professional, 'Eme' for Emergency, or 'Fav' for Favorites or enter 'esc' to exit.\n")
            
            while True:
                sheet_choice = input("Enter your choice: \n").capitalize()
                
                if sheet_choice in ['Per', 'Pro', 'Eme', 'Fav']:
                    break
                elif sheet_choice == "Esc":
                    print(exit_program_with_countdown())
                    return
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
                try:
                    num_contacts = int(num_contacts_input)
                    break
                except ValueError:
                    if num_contacts_input.lower() == "esc":
                        print(exit_program_with_countdown())
                        return
                    else:
                        print("\nInvalid input. Please enter a number or type 'esc' to exit the program.")
             # _ acts as draft / placeholder variable (non main focus)
            for _ in range(num_contacts):
                name = input("Enter contact name: ")
                while True:
                    number = input("Enter contact number (only numbers, + or -): ")
                    # Added regular expression for the telephone number - might just delete it later on and keep it to only to numbers
                    if re.match(r'^[\d\+\-]+$', number):
                        break
                    elif number.lower() == "esc":
                        print(exit_program_with_countdown())
                        return
                    else:
                        print("Invalid telephone number. Please enter only numbers, + or -")
                
                if check_duplicate_contact(name, number):
                    print("Warning: This contact already exists.")
                else:
                    add_data_with_name_column(sheet, [[name, number]])
                    print("Contact added successfully.")
            
            break
        elif add_contacts_input in ["no", "n"]:
            print("No contacts added.")
            break
        elif add_contacts_input == "esc":
            print(exit_program_with_countdown())
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
    
def search_contacts():
    """
    Searches for a contact by name or tel number
    """
    search_query = input("Enter the name or telephone number of the contact you want to search for:\n").strip().lower()
    search_results = []
    
    for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
        contacts = sheet.get_all_records()
        for contact in contacts:
            if search_query in contact["Name"].lower() or search_query in contact["Telephone Number"].lower():
                search_results.append((sheet.title, contact))
    
    if search_results:
        print("\nSearch Results:\n")
        for category, contact in search_results:
            print(f"\nCategory: {category}")
            print("Name:", contact["Name"])
            print("Telephone Number:", contact["Telephone Number"])
    else:
        print("\nNo matching contacts found.")


def print_sheet_data(sheet):
    """
    Prints the data from a specified sheet.
    """
    sheet_data = sheet.get_all_values()
    print(f"\n{sheet.title} Contacts:")
    for row in sheet_data:
        print(row)
 

# Basically the function to replace the "Exiting the program" into something nice and simpler
def exit_program_with_countdown():
    """
    Exits the program with a countdown before exiting.
    """
    countdown = 3
    print(f"\nExiting the program in {countdown}...")
    while countdown > 0:
        time.sleep(1)
        print(countdown)
        countdown -= 1
    print("\nBoom!")
    return ""


def main():
    if not use_program():
        print(exit_program_with_countdown())
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

    search_contacts()
    
    export_contacts()


if __name__ == "__main__":
    main()


