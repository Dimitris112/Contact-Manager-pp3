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
print(colored_ascii_art + "PLEASE BE PATIENT. The program takes more time to load than GTA V does.")
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
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m'
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


#Basically a refactored choose_color function broken into 4 smaller ones
def print_color_options(colors):
    """
    Print color options along with reset option
    """
    for index, (color_name, color_code) in enumerate(colors.items(), start=1):
        print(f"{index}. {color_name.capitalize()}")
    print(f"7. Reset")

def reset_color():
    """
    Reset the input color to default
    """
    global input_color
    input_color = RESET
    return input_color

def select_color(choice):
    """
    Select the input color based on the user's choice
    """
    global input_color
    if choice == 7:
        reset_color()
        return
    elif 1 <= choice <= len(COLORS):
        chosen_color = list(COLORS.values())[choice - 1]
        input_color = chosen_color
        return input_color
    else:
        print("Oops! That's not a valid option. Please try again.")




def choose_color():
    """
    Allow the user to change the input color
    """
    global input_color

    while True:
        print("\nFeeling like changing the color for your input? (yes/no)")
        choice = input().strip().lower()

        if choice in yes_words:
            print("Alright, let's splash some color into your life!")
            print_color_options(COLORS)
            
            color_choice = input("\nChoose the number of the color you fancy or '7' to reset\n").strip()

            if color_choice == "7":
                input_color = reset_color()
                print(input_color + "Color reset to default")
                continue
            elif color_choice.isdigit() and 1 <= int(color_choice) <= len(COLORS):
                selected_color = select_color(int(color_choice))
                if selected_color:
                    color_name = list(COLORS.keys())[int(color_choice)  - 1]
                    print(f"Selected color: {input_color}{color_name.capitalize()}")
                    confirm = input("\nAre you sure? (yes/no)\n").strip().lower()
                    if confirm in yes_words:
                        return selected_color
                    elif confirm in no_words:
                        continue
                    elif confirm == "esc":
                        return exit_program_with_countdown()
                    else:
                        print("Invalid input. Please enter 'yes', 'no', or 'esc'.")
            else:
                print("Oops! That's not a valid option. Please try again.")
        elif choice in no_words:
            print("No problemo! Let's keep it simple and sleek.")
            input_color = reset_color()
            print("Current color:", input_color)
            return RESET
        elif choice.lower() == "esc":
            return exit_program_with_countdown()
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
                    return
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
                            return
                        elif choice == "esc":
                            print(exit_program_with_countdown(input_color))
                            return ""
                        else:
                            print(invalid_input_yes_no)
                            continue
                else:
                    print("Oh, close but no cigar! Give it another shot!")
                    continue
            break
        elif view_contacts in no_words:
            print("No problem. You can view contacts later.")
            return
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
    Prompts the user if he wants to add new contacts and adds them to the selected category
    """
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
                        else:
                            break
                    elif email_prompt == 'esc':
                        return exit_program_with_countdown(input_color)
                    elif email_prompt in no_words:
                        print("No email added.")
                        break
                    else:
                        print(invalid_input_yes_no)
                    
                birthday = ""
                add_birthday_prompt = input("\nDo you want to add the contact's birthday? (yes/no)\n").strip().lower()
                if add_birthday_prompt in yes_words:
                    birthday = input("\nEnter contact birthday (dd/mm)\n").strip()
                    if not re.match(r'^\d{2}[-/._]\d{2}$', birthday) and not re.match(r'^\d{2}[-/._]\d{2}$', birthday):
                        print("\nInvalid birthday format. Please enter birthday in dd/mm format.")
                        continue
                elif add_birthday_prompt == 'esc':
                    return exit_program_with_countdown(input_color)
                elif add_birthday_prompt not in no_words:
                    print(invalid_input_yes_no)
                    continue
                else:
                    print("No birthday added.")
                
                notes = ""
                while True:
                    notes_prompt = input("\nDo you want to write some notes for this contact? (yes/no)\n").strip().lower()
                    if notes_prompt in yes_words:
                        notes = input("\nEnter notes for the contact\n")
                        if len(notes) > 60:
                            print("\nNotes exceed 60 characters.")
                            notes = notes[:60]
                        else:
                            print("Notes added.")
                        break
                    elif notes_prompt == 'esc':
                        return exit_program_with_countdown(input_color)
                    elif notes_prompt in no_words:
                        print("No notes added.")
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
                    added_contact_info = {
                        "Name": name,
                        "Phone Number": formatted_num,
                        "Email": email,
                        "Birthday": birthday,
                        "Notes": notes
                    }
                    add_data_with_name_column(sheet, [[name, formatted_num, email, birthday, notes]], input_color)
                    print("\nContact added successfully.")

            print("\nAdded Contact Information:")
            for key, value in added_contact_info.items():
                print(f"{key}: {value}")

            break
        elif add_contacts_input in no_words:
            print("\nNo contacts added.")
            return
        elif add_contacts_input == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            print(invalid_input_yes_no)


                            
def search_contacts(input_color):
    """
    Searches for a contact by name, telephone number, email, or birthday
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

            print("\nEnter the search term number from the following list\n"
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
                    print("1. Name:", contact["Name"])
                    print("2. Telephone Number:", contact["Telephone Number"])
                    print("3. Email:", contact["Email address"])
                    print("4. Birthday:", contact["Birthday"])
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
    Allows the user to edit an existing contact
    """
    while True:
        edit_choice = input("\nDo you want to edit any of your contacts? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if edit_choice in yes_words:
            all_categories = [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]

            while True:
                print("\nSelect a category to edit contacts from")
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
                        
                        if len(contact) >= 5:
                            print(f"Notes: {contact[4]}")
                        else:
                            print("No notes for this contact.")
                            
                        while True:
                            field_choice = input("\nEnter the number of the field you want to edit (1-5) or 'cancel' to go back\n").strip().lower()

                            if field_choice == 'cancel':
                                break
                            elif field_choice.isdigit() and 1 <= int(field_choice) <= 5:
                                field_index = int(field_choice) - 1
                                category = sheet.title.lower()
                                new_value = input(f"\nEnter the new value for the {category}\n").strip()

                                while len(contact) <= field_index:
                                    contact.append('')
                                
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
            return
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
            return
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
        print("Using default color.")
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