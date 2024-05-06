import gspread
import re
import time
import ascii_py
import sys
from google.oauth2.service_account import Credentials
#The program takes a lot of time to load - be patient

ascii_art = r'''
  /$$$$$$                        /$$                           /$$       
 /$$__  $$                      | $$                          | $$       
| $$  \__/  /$$$$$$  /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$$ /$$$$$$     
| $$       /$$__  $$| $$__  $$|_  $$_/   |____  $$ /$$_____/|_  $$_/     
| $$      | $$  \ $$| $$  \ $$  | $$      /$$$$$$$| $$        | $$       
| $$    $$| $$  | $$| $$  | $$  | $$ /$$ /$$__  $$| $$        | $$ /$$   
|  $$$$$$/|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/   
 \______/  \______/ |__/  |__/   \___/   \_______/ \_______/   \___/     
 /$$      /$$                                                            
| $$$    /$$$                                                            
| $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
| $$ $$/$$ $$ |____  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  $$$| $$  /$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$| $$  \__/
| $$\  $ | $$ /$$__  $$| $$  | $$ /$$__  $$| $$  | $$| $$_____/| $$      
| $$ \/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      
|__/     |__/ \_______/|__/  |__/ \_______/ \____  $$ \_______/|__/      
                                            /$$  \ $$                    
                                           |  $$$$$$/                    
                                            \______/                     

'''
colored_ascii_art = "\033[92m" + ascii_art
print(colored_ascii_art)
#Revert the colors back to default after printing the ascii art
RESET = '\033[0m'
print(RESET)

#Font Name: Big Money-ne / Contact Manager 
#https://patorjk.com/software/taag/#p=display&f=Big%20Money-ne&t=Contact%0AManager


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("contact_manager")

#ANSI escape coloring codes
COLORS = {
    "1": {"name": "black", "code": "\u001b[30m"},
    "2": {"name": "red", "code": "\u001b[31m"},
    "3": {"name": "green", "code": "\u001b[32m"},
    "4": {"name": "yellow", "code": "\u001b[33m"},
    "5": {"name": "blue", "code": "\u001b[34m"},
    "6": {"name": "magenta", "code": "\u001b[35m"},
    "7": {"name": "cyan", "code": "\u001b[36m"},
    "8": {"name": "white", "code": "\u001b[37m"},
    "9": {"name": "reset", "code": "\u001b[0m"},
    "10": {"name": "background_black", "code": "\u001b[40m"},
    "11": {"name": "background_red", "code": "\u001b[41m"},
    "12": {"name": "background_green", "code": "\u001b[42m"},
    "13": {"name": "background_yellow", "code": "\u001b[43m"},
    "14": {"name": "background_blue", "code": "\u001b[44m"},
    "15": {"name": "background_magenta", "code": "\u001b[45m"},
    "16": {"name": "background_cyan", "code": "\u001b[46m"},
    "17": {"name": "background_white", "code": "\u001b[47m"},
    "18": {"name": "background_reset", "code": "\u001b[49m"},
    "19": {"name": "green_on_black", "code": "\u001b[30;42m"}
}

PRESETS = {
    "Vibrant Green": {
        "input_color": COLORS["3"]["code"],
        "background_color": COLORS["10"]["code"]
    },
    "Ocean Breeze": {
        "input_color": COLORS["5"]["code"],
        "background_color": COLORS["17"]["code"]
    },
    "Sunrise": {
        "input_color": COLORS["2"]["code"],
        "background_color": COLORS["13"]["code"]
    },
    "Emerald City": {
        "input_color": COLORS["3"]["code"],
        "background_color": COLORS["10"]["code"]
    },
    "Mystic Purple": {
        "input_color": COLORS["6"]["code"],
        "background_color": COLORS["16"]["code"]
    },
    "Golden Sunset": {
        "input_color": COLORS["4"]["code"],
        "background_color": COLORS["15"]["code"]
    }
}





personal_sheet = SHEET.worksheet("Personal")
professional_sheet = SHEET.worksheet("Professional")
emergency_sheet = SHEET.worksheet("Emergency")
favorites_sheet = SHEET.worksheet("Favorites")

yes_words = ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly", "ye", "ok", "okay", "okey", "alright", "ya", "ofc")
no_words = ("no", "n", "nah", "nope", "negative", "not", "nay", "never", "ne", "nop")
failed_times = "\nI can do this all day. You've failed to give a correct answer {} times.\n"
teasing_message = "Oh, close but no cigar! Give it another shot!"
invalid_input_yes_no = "\nInvalid input. Please enter (yes/no)\n"

personal_data = []

professional_data = []

emergency_data = []

favorites_data = []

input_color = None



def validate_contact_info(phone_number, email, birthday):
    """
    Validates phone number, email address, and birthday format
    """
    phone_pattern = r'^[\+\-\(\)\.\s/0-9]{4,30}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    birthday_pattern = r'^\d{2}[-/._]\d{2}$'

    phone_valid = bool(re.match(phone_pattern, phone_number))
    email_valid = bool(re.match(email_pattern, email))
    birthday_valid = bool(re.match(birthday_pattern, birthday))

    return {
        "phone_valid": phone_valid,
        "email_valid": email_valid,
        "birthday_valid": birthday_valid
    }




def use_program():
    """
    The function to basically ask the user if he wants to
    use the contact manager or not
    and then proceed accordingly.
    """
    global counter
    counter = 0
    while True:
        user_input = input("Do you want to use the contact manager? (yes/no)\nYou can enter 'esc' to terminate the program anytime.\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if user_input in yes_words:
            return True
        elif user_input in no_words:
            return False
        elif user_input == "esc":
            return False
        else:
            counter += 1
            print(failed_times.format(counter))


def choose_color():
    """
    Allows the user to change the input color for excitement and a dash of spice!
    """
    global input_color
    
    while True:
        print("\nFeeling like changing the color for your input? (yes/no)")
        choice = input().strip().lower()

        if choice in yes_words:
            print("\nWould you like to choose a preset color combination or customize your own?")
            print("1. Choose preset")
            print("2. Customize")
            preset_or_custom = input("Enter your choice (1 or 2)\n").strip()
            
            if preset_or_custom == "1":
                print("Pick one of the available presets:")
                for i, preset in enumerate(PRESETS.keys()):
                    print(f"{i + 1}. {preset}")
                preset_choice = input("Enter the number of the preset: ").strip()
                
                if preset_choice.isdigit() and 1 <= int(preset_choice) <= len(PRESETS):
                    chosen_preset = list(PRESETS.values())[int(preset_choice) - 1]
                    input_color = chosen_preset["input_color"]
                    background_color = chosen_preset["background_color"]
                    print(f"\nSelected preset: {list(PRESETS.keys())[int(preset_choice) - 1]}")
                    print("Input color:", input_color["name"])
                    print("Background color:", background_color["name"])
                    return input_color
                else:
                    print("Invalid choice. Please enter a valid preset number.")
            elif preset_or_custom == "2":
                print("Choose your custom color combination:")
                for i, combination in enumerate(COMBINATIONS.keys()):
                    print(f"{i + 1}. {combination}")
                custom_choice = input("Enter the number of the combination: ").strip()
                
                if custom_choice.isdigit() and 1 <= int(custom_choice) <= len(COMBINATIONS):
                    chosen_combination = list(COMBINATIONS.values())[int(custom_choice) - 1]
                    input_color = chosen_combination["input_color"]
                    background_color = chosen_combination["background_color"]
                    print(f"\nSelected custom combination: {custom_choice}")
                    print("Input color:", input_color)
                    print("Background color:", background_color)
                    return input_color
                else:
                    print("Invalid choice. Please enter a valid combination number.")
            else:
                print("Invalid choice. Please enter '1' to choose a preset or '2' to customize.")
                
        elif choice in no_words:
            print("No problemo! Let's keep it simple and sleek.")
            return RESET
        elif choice.lower() == "esc":
            print(exit_program_with_countdown())
            return ""
        else:
            print("Oops! I didn't catch that. Can you try again? (yes/no/esc)\n")




def add_data_with_name_column(sheet, data, input_color):
    """
    Adds new data to the sheets with a predefined header
    If the sheet is empty, it sets a header row with its columns on A1 and E1
    as "Name","Telephone Number", "Email Address", "Birthday" and "Notes" 
    
    Then it appends the data provided by the user to the sheet
    """
    existing_data = sheet.get_all_values()
    if input_color:
        print(input_color, end="")
    print(f"\nExisting data in {sheet.title} sheet:", existing_data)

    if not existing_data or not existing_data[0]:
        header_row = ["Name", "Telephone Number", "Email address", "Birthday", "Notes"]
        sheet.insert_row(header_row, index=1)
        sheet.format("A1:E1", {"textFormat": {"bold": True}})
    else:
        for row in data:
            if len(row[4]) > 60:
                row[4] = row[4][:60]
            sheet.append_row(row)


def protect_header(sheet):
    """
    Protects the header row for the sheets
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
                    "endColumnIndex": 5
                },
                "warningOnly": True
            }
        }
    }]
    SHEET.batch_update({"requests": requests})


def check_duplicate_contact(name, number, email, birthday):
    """
    Checks if a contact already exists (name / tel number / email or dob)
    in any of the sheets
    """
    for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
        contacts = sheet.get_all_records()
        for contact in contacts:
            if contact["Name"] == name or contact["Telephone Number"] == number:
                return True
    return False




def view_existing_contacts(input_color=None):
    """
    Prompts the user if he wants to view existing contacts
    """
    counter = 0
    while True:
        print("\nDo you want to view existing contacts? (yes/no)")
        view_contacts = input().strip().lower()

        if view_contacts in yes_words:
            while True:
                print("\nChoose a category:")
                print("1. Personal")
                print("2. Professional")
                print("3. Emergency")
                print("4. Favorites")
                print("5. All")
                print("6. I don't want to")

                category_choice = input("\nEnter the number of the category you want to view\n").strip()

                if category_choice == '6':
                    print("\nNo problem. You can view contacts later.")
                    break
                elif category_choice.isdigit() and 1 <= int(category_choice) <= 5:
                    if category_choice == '5':
                        print_sheet_data(personal_sheet, input_color)
                        print_sheet_data(professional_sheet, input_color)
                        print_sheet_data(emergency_sheet, input_color)
                        print_sheet_data(favorites_sheet, input_color)
                        return
                    else:
                        sheet = [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet][int(category_choice) - 1]
                        print_sheet_data(sheet, input_color)
                        print("\nDo you want to view contacts from another category? (yes/no)")
                        choice = input().strip().lower()
                        if choice in yes_words:
                            continue
                        elif choice in no_words:
                            break
                        elif choice == "esc":
                            print(exit_program_with_countdown(input_color))
                            return ""
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")
                            continue
                else:
                    print("Oh, close but no cigar! Give it another shot!")
                    continue
        elif view_contacts in no_words:
            print("No problem. You can view contacts later.")
            break
        elif view_contacts == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            counter += 1
            if counter >= 3:
                print("\nToo many incorrect attempts. See ya")
                print(exit_program_with_countdown(input_color))
                return ""
            print(teasing_message)




            
            

def add_contacts(input_color):
    """
    Prompts the user if he wants to add new contacts and adds them to the selected category.
    """
    email = ""
    
    while True:
        add_contacts_input = input("\nDo you want to add new contacts? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if add_contacts_input in yes_words:
            print("\nSelect a category to add contacts to:")
            print("1. Personal")
            print("2. Professional")
            print("3. Emergency")
            print("4. Favorites")
            print("5. Skip")
            print("6. Return to the main menu")

            while True:
                category_choice = input("\nEnter the number of the category you want to add contacts to\n")

                if category_choice == '6':
                    print("\nReturning to the main menu.")
                    select_section()
                    return
                elif category_choice.isdigit() and 1 <= int(category_choice) <= 4:
                    sheet = [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet][int(category_choice) - 1]
                    break
                elif category_choice == '5':
                    print("Alright, skipped.")
                    return
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")

            while True:
                num_contacts_input = input("\nHow many contacts would you like to add? (1-5)\n").strip()
                if num_contacts_input.lower() == "esc":
                    return exit_program_with_countdown(input_color)

                try:
                    num_contacts = int(num_contacts_input)
                    if not 1 <= num_contacts <= 5:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 5.")

            for _ in range(num_contacts):
                while True:
                    name = input("\nEnter contact name (up to 30 characters)\n").strip()
                    if len(name) > 30:
                        print("\nName exceeds 30 characters. Please enter a name with 30 characters or less.")
                        continue
                    else:
                        break

                while True:
                    number = input("\nEnter contact number (4 to 30 digits)\n").strip()
                    formatted_num = number
                    phone_valid = validate_contact_info(formatted_num, "", "")["phone_valid"]
                    if not phone_valid:
                        print("\nInvalid phone number format. Please enter your contact as\n+1234567890, (123) 456-7890, 123-456-7890, 123.456.7890,\n123/456.7890, 1234567890")
                        continue
                    else:
                        break
                
                email = ""

                while True:
                    email_prompt = input("\nDo you want to enter an email address for the contact? (yes/no)\n").strip().lower()
                    if email_prompt in yes_words:
                        email = input("\nEnter the contact's email address\n").strip()
                        if '@' not in email or '.' not in email or email.count('@') != 1:
                            print("\nInvalid email address. Please enter a valid email address containing one '@' and at least one '.'")
                            continue
                        break
                    elif email_prompt in no_words:
                        print("No email added.")
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

                birthday = ""

                while True:
                    add_birthday_prompt = input("\nDo you want to add the contact's birthday? (yes/no)\n").strip().lower()
                    if add_birthday_prompt in yes_words:
                        birthday = input("\nEnter contact birthday (dd/mm)\n").strip()
                        if not re.match(r'^\d{2}[-/._]\d{2}$', birthday) and not re.match(r'^\d{2}[-/._]\d{2}$', birthday):
                            print("\nInvalid birthday format. Please enter birthday in dd/mm format.")
                            continue
                        break
                    elif add_birthday_prompt in no_words:
                        print("Alright. No birthday wishes.")
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

                validation_result = validate_contact_info(formatted_num, email, birthday)
                if not all(validation_result.values()):
                    print("\nInvalid contact information. Please check and try again.")
                    continue

                if check_duplicate_contact(name, formatted_num, email, birthday):
                    print("\nWarning: This contact already exists.")
                else:
                    notes = ""

                    while True:
                        notes_prompt = input("\nDo you want to write some notes for this contact? (yes/no)\n").strip().lower()
                        if notes_prompt in yes_words:
                            notes = input("\nEnter notes for the contact\n")
                            if len(notes) > 60:
                                print("\nNotes exceed 60 characters. C'mon.")
                                notes = notes[:60]
                            break
                        elif notes_prompt in no_words:
                            print("Ok, I get it. You don't want to add any notes.")
                            break
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")

                    add_data_with_name_column(sheet, [[name, formatted_num, email, birthday, notes]], input_color)
                    print("\nContact added successfully.")

            break
        elif add_contacts_input in no_words:
            print("\nNo contacts added.")
            break
        elif add_contacts_input == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            print(invalid_input_yes_no)




def search_contacts(input_color):
    """
    Searches for a contact by name, telephone number, email, or birthday.
    """
    counter = 0
    while True:
        print("\nDo you want to search for a contact? (yes/no)")
        search_choice = input().strip().lower()

        if search_choice in yes_words:
            search_query_map = {
                '1': 'name',
                '2': 'telephone number',
                '3': 'email',
                '4': 'birthday',
                '5': 'skip'
            }

            print("\nEnter the search term number from the following list:\n"
                  "1. Name\n"
                  "2. Telephone number\n"
                  "3. Email\n"
                  "4. Birthday\n"
                  "5. I don't want to")

            search_query = input().strip()

            if search_query not in search_query_map:
                print("\nInvalid search option. Please enter a number from 1 to 5.")
                continue

            search_term = search_query_map[search_query]

            if search_term == 'skip':
                print("\nNo problem. You can search for contacts later.")
                break

            if search_term == 'name':
                search_value = input("\nEnter the name of the contact you want to search for\n").strip().lower()
            elif search_term == 'telephone number':
                search_value = input("\nEnter the telephone number of the contact you want to search for\n").strip().lower()
            elif search_term == 'email':
                search_value = input("\nEnter the email of the contact you want to search for\n").strip().lower()
            elif search_term == 'birthday':
                search_value = input("\nEnter the birthday of the contact you want to search for\n").strip().lower()

            search_results = []

            for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
                contacts = sheet.get_all_records()
                for contact in contacts:
                    contact_name = str(contact["Name"]).lower()
                    contact_email = str(contact["Email address"]).lower()
                    contact_birthday = str(contact["Birthday"]).lower()
                    contact_phone = str(contact["Telephone Number"]).lower()

                    if search_term == 'name' and search_value in contact_name:
                        search_results.append((sheet.title, contact))
                    elif search_term == 'telephone number' and search_value in contact_phone:
                        search_results.append((sheet.title, contact))
                    elif search_term == 'email' and search_value in contact_email:
                        search_results.append((sheet.title, contact))
                    elif search_term == 'birthday' and search_value in contact_birthday:
                        search_results.append((sheet.title, contact))

            if search_results:
                print("\nSearch Results:\n")
                for category, contact in search_results:
                    print(f"Category: {category}")
                    print("Name:", contact["Name"])
                    print("Telephone Number:", contact["Telephone Number"])
                    print("Email:", contact["Email address"])
                    print("Birthday:", contact["Birthday"])
            else:
                print("\nNo matching contacts found.")

            break

        elif search_choice in no_words:
            print("\nNo problem. You can search for contacts later.")
            break
        elif search_choice == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            counter += 1
            if counter >= 4:
                print("\nToo many incorrect attempts. See ya")
                print(exit_program_with_countdown(input_color))
                return ""
            print(teasing_message)




def edit_contact(input_color):
    """
    Allows the user to edit an existing contact.
    """
    while True:
        edit_choice = input("\nDo you want to edit any of your contacts? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if edit_choice in yes_words:
            all_categories = [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]

            while True:
                print("\nSelect a category to edit contacts from:")
                print("1. Personal")
                print("2. Professional")
                print("3. Emergency")
                print("4. Favorites")
                print("5. Return to main menu")

                category_choice = input("\nEnter the number of the category you want to edit contacts from\n")

                if category_choice == '5':
                    print("\nAlright, let's not stir up trouble. Back to the main menu.")
                    return

                try:
                    category_index = int(category_choice) - 1
                    if category_index not in range(len(all_categories)):
                        raise ValueError
                except ValueError:
                    print("Hmm, trying to be tricky, are we? Enter a number between 1 and 5.")
                    continue

                sheet = all_categories[category_index]
                sheet_data = sheet.get_all_values()
                if not sheet_data or len(sheet_data) <= 1:
                    print("No contacts found in this category.")
                    break

                print("Contacts in this category:")
                for index, row in enumerate(sheet_data[1:], start=1):
                    print(f"{index}. {row[0]}")

                action_choice = input("\nDo you want to edit a contact in this category? (yes/no)\n").strip().lower()

                if action_choice in yes_words:
                    name_choice = input("Enter the number of the contact you want to edit or 'cancel' to go back\n").strip().lower()
                    if name_choice == 'cancel':
                        break
                    elif name_choice.isdigit() and 1 <= int(name_choice) <= len(sheet_data) - 1:
                        contact_index = int(name_choice) + 1
                        contact = sheet.row_values(contact_index)
                        print("\nEditing contact:")
                        print(f"Name: {contact[0]}")
                        print(f"Telephone Number: {contact[1]}")
                        print(f"Email: {contact[2]}")
                        print(f"Birthday: {contact[3]}")
                        print(f"Notes: {contact[4]}")

                        while True:
                            field_choice = input("\nEnter the number of the field you want to edit (1-5) or 'cancel' to go back\n").strip().lower()

                            if field_choice == 'cancel':
                                break
                            elif field_choice.isdigit() and 1 <= int(field_choice) <= 5:
                                field_index = int(field_choice) - 1
                                new_value = input("\nEnter the new value for the field\n").strip()

                                
                                contact[field_index] = new_value
                                sheet.update_row(contact_index, contact)

                                print("Contact updated successfully.")
                                break
                            else:
                                print("Invalid input. Please enter a number between 1 and 5.")
                elif action_choice in no_words:
                    print("\nNo contacts edited.")
                    break
                else:
                    print(invalid_input_yes_no)
                break
        elif edit_choice in no_words:
            print("\nAlright, no changes made. Your contacts remain untouched.")
            break
        elif edit_choice == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            print(invalid_input_yes_no)



def delete_contacts(input_color):
    """
    Allows the user to delete contacts from the specified category or from all categories
    If the user selects '5. All categories', a confirmation prompt is displayed before deleting all contacts
    """
    while True:
        delete_choice = input("\nDo you want to delete any of your contacts? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if delete_choice in yes_words:
            all_categories = [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]

            while True:
                print("\nSelect a category to delete contacts from:")
                print("1. Personal")
                print("2. Professional")
                print("3. Emergency")
                print("4. Favorites")
                print("5. All categories")
                print("6. Return to main menu")

                category_choice = input("\nEnter the number of the category you want to clean up\n")

                if category_choice == '6':
                    print("\nAlright, let's not stir up trouble. Back to the main menu.")
                    return

                try:
                    category_index = int(category_choice) - 1
                    if category_index not in range(len(all_categories)):
                        raise ValueError
                except ValueError:
                    print("Hmm, trying to be tricky, are we? Enter a number between 1 and 6.")
                    continue

                sheet = all_categories[category_index]
                sheet_data = sheet.get_all_values()
                if not sheet_data or len(sheet_data) <= 1:
                    print("No contacts found in this category.")
                    break

                print("Contacts in this category:")
                for index, row in enumerate(sheet_data[1:], start=1):
                    print(f"{index}. {row[0]}")

                if category_choice == '5':
                    confirm_choice = input("\nAre you sure you want to delete all contacts in all categories? (yes/no)\n").strip().lower()
                    if confirm_choice in yes_words:
                        for sheet in all_categories:
                            sheet.clear()
                        print("All contacts in all categories deleted successfully.")
                    else:
                        print("Deletion canceled.")
                else:
                    action_choice = input("\nDo you want to delete all contacts in this category? (yes/no)\n").strip().lower()

                    if action_choice in yes_words:
                        sheet.clear()
                        print("All contacts in this category deleted successfully.")
                    elif action_choice in no_words:
                        name_choice = input("Enter the number of the contact you want to delete or 'cancel' to go back\n").strip().lower()
                        if name_choice == 'cancel':
                            break
                        elif name_choice.isdigit() and 1 <= int(name_choice) <= len(sheet_data) - 1:
                            contact_index = int(name_choice) + 1
                            sheet.delete_rows(contact_index)
                            print("Contact removed successfully.")
                        else:
                            print("Invalid input. Please enter the number corresponding to the contact you want to delete.")
                    else:
                        print(invalid_input_yes_no)
                break
        elif delete_choice in no_words:
            print("\nPlaying it safe, eh? No contacts deleted.")
            break
        elif delete_choice == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            print(invalid_input_yes_no)



def print_sheet_data(sheet, input_color):
    """
    Prints the data from a specified sheet.
    """
    sheet_data = sheet.get_all_values()
    if input_color:
        print(input_color, end="")
    print(f"\n{sheet.title} Contacts:")
    for row in sheet_data:
        print(", ".join(row))
 


def select_section(input_color=None):
    while True:
        print("\nWhat would you like to do next?")
        print("1. View contacts")
        print("2. Add contacts")
        print("3. Edit contacts")
        print("4. Delete contacts")
        print("5. Change color")
        print("6. Exit")

        choice = input("Enter the number of your choice.\n").strip()

        if choice == "1":
            view_existing_contacts(input_color)
        elif choice == "2":
            add_contacts(input_color)
        elif choice == "3":
            edit_contact(input_color)
        elif choice == "4":
            delete_contacts(input_color)
        elif choice == "5":
            input_color = choose_color()
        elif choice == "6":
            print(exit_program_with_countdown(input_color))
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")





# Basically the function to replace the "Exiting the program" into something nice
def exit_program_with_countdown(input_color=None):
    """
    Exits the program with a countdown before exiting.
    """
    print(f"\nExiting the program in ...")
    countdown = 3
    while countdown > 0:
        time.sleep(1)
        print(countdown)
        countdown -= 1
    print("\nBoom!")
    print("This is the end of the program created by Dimitris - 2024")
    print("For more information, visit:")
    print("\U0001F464 LinkedIn: https://www.linkedin.com/in/dimitrios-thlivitis/")
    print("\U0001F4BB GitHub Repository: https://github.com/Dimitris112/Contact-Manager-pp3")
    sys.exit()





#MARK: M A I N  
def main():
    if not use_program():
        print(exit_program_with_countdown())
        return
    
    print("Great! Let's proceed with the program.\n")
    
    chosen_color = choose_color()
    if chosen_color is None:
        pass
    elif chosen_color == "":
        return
    else:
        print(chosen_color)
        
    
    view_existing_contacts(chosen_color)
    
    add_contacts(chosen_color)
    
    # Protect header for all sheets
    protect_header(personal_sheet)
    protect_header(professional_sheet)
    protect_header(emergency_sheet)
    protect_header(favorites_sheet)
    
    search_contacts(chosen_color)
    
    edit_contact(chosen_color)
    
    delete_contacts(chosen_color)
    
    select_section(chosen_color)

if __name__ == "__main__":
    main()


