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


print(ascii_art)
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

RESET = '\033[0m'



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



def format_phone_number(number):
    phone_pattern = r'^[\+\-\(\)\.\s/0-9]{4,20}$'

    if re.match(phone_pattern, number):
        return number
    else:
        return None



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



def choose_color(input_color=None):
    """
    Allows the user to change the input color for excitement and a dash of spice!
    """
    while True:
        if not input_color:
            print("\nFeeling like changing the color for your input? (yes/no)")
        else:
            print("\nWould you like to change the color for your input? (yes/no)")

        choice = input().strip().lower()

        if choice in yes_words:
            while True:
                print("Alright, let's splash some color into your life!")
                print("Pick your poison:")
                print("1. Red - Like a blazing fire!")
                print("2. Green - As fresh as the morning dew!")
                print("3. Yellow - Bright as the sun!")
                print("4. Blue - Cool as the ocean breeze!")
                print("5. Magenta - A splash of vibrant energy!")
                print("6. Cyan - Like the clear sky on a sunny day!")
                print("7. Reset - Back to basics")

                color_choice = input("\nChoose the number of the color you fancy or '7' to reset\n").strip()

                if color_choice == "1":
                    chosen_color = COLORS['red']
                    chosen_color_name = "Red"
                elif color_choice == "2":
                    chosen_color = COLORS['green']
                    chosen_color_name = "Green"
                elif color_choice == "3":
                    chosen_color = COLORS['yellow']
                    chosen_color_name = "Yellow"
                elif color_choice == "4":
                    chosen_color = COLORS['blue']
                    chosen_color_name = "Blue"
                elif color_choice == "5":
                    chosen_color = COLORS['magenta']
                    chosen_color_name = "Magenta"
                elif color_choice == "6":
                    chosen_color = COLORS['cyan']
                    chosen_color_name = "Cyan"
                elif color_choice == "7":
                    if input_color:
                        print("Resetting color to default.")
                    return RESET if input_color else None
                elif color_choice.lower() == "esc":
                    print(exit_program_with_countdown())
                    return None
                else:
                    print("Whoops! That's not a color I can work with. Try again!\n")
                    continue

                confirm_choice = input(f"\nVoilà! You've chosen {chosen_color}{chosen_color_name} as your input color.\nAre you pleased with that option? (yes/no)\n").strip().lower()
                if confirm_choice in yes_words:
                    return chosen_color
                elif confirm_choice in no_words:
                    print("\nLet's try a different color then!")
                    break
                elif confirm_choice == "esc":
                    print(exit_program_with_countdown())
                    return None
                else:
                    print("Not feeling the vibe? Let's start over then.\n")
        elif choice in no_words:
            print("No problemo! Let's keep it simple and sleek.")
            return RESET if input_color else None
        elif choice.lower() == "esc":
            print(exit_program_with_countdown())
            return None
        else:
            print("Oops! I didn't catch that. Can you try again? (yes/no/esc)\n")





def add_data_with_name_column(sheet, data, input_color):
    """
    Adds new data to the sheets with a predefined header
    If the sheet is empty, it sets a header row with its columns on A1 and B1
    as "Name" and "Telephone Number"
    
    Then it appends the data provided by the user to the sheet
    """
    existing_data = sheet.get_all_values()
    if input_color:
        print(input_color, end="")
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




def view_existing_contacts(input_color=None):
    """
    Prompts the user if he wants to view existing contacts
    """
    counter = 0
    while True:
        view_contacts = input("\nDo you want to view existing contacts? (yes/no)\n").strip().lower()
        if view_contacts in yes_words:
            print("\nChoose a category:")
            print("1. Personal")
            print("2. Professional")
            print("3. Emergency")
            print("4. Favorites")
            print("5. All")
            print("6. I don't want to")

            category_choice = input("\nEnter the number of the category you want to view\n")
            if category_choice == '1':
                print_sheet_data(personal_sheet, input_color)
                break
            elif category_choice == '2':
                print_sheet_data(professional_sheet, input_color)
                break
            elif category_choice == '3':
                print_sheet_data(emergency_sheet, input_color)
                break
            elif category_choice == '4':
                print_sheet_data(favorites_sheet, input_color)
                break
            elif category_choice == '5':
                print_sheet_data(personal_sheet, input_color)
                print_sheet_data(professional_sheet, input_color)
                print_sheet_data(emergency_sheet, input_color)
                print_sheet_data(favorites_sheet, input_color)
                break
            elif category_choice == '6':
                print("\nNo problem. You can view contacts later.")
                break
            elif category_choice.lower() == "esc":
                print(exit_program_with_countdown(input_color))
                return ""
            else:
                counter += 1
                if counter >= 3:
                    print("\nToo many incorrect attempts. See ya")
                    return exit_program_with_countdown(input_color)
                print(teasing_message)
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
    Prompts the user if they want to add new contacts and adds them to the selected category.
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
                    number = input("\nEnter contact number (4 to 20 digits)\n").strip()
                    formatted_number = format_phone_number(number)
                    if formatted_number:
                        break
                    else:
                        print("\nInvalid phone number format. Please enter your contact as\n+1234567890, (123) 456-7890, 123-456-7890, 123.456.7890, 123/456.7890, 1234567890")
                        continue

                if check_duplicate_contact(name, number):
                    print("\nWarning: This contact already exists.")
                else:
                    add_data_with_name_column(sheet, [[name, formatted_number]], input_color)
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
    Searches for a contact by name or telephone number.
    """
    while True:
        search_choice = input("\nDo you want to search for a contact? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if search_choice in yes_words:
            search_query = input("\nEnter the name or telephone number of the contact you want to search for\n").strip().lower()
            search_results = []

            for sheet in [personal_sheet, professional_sheet, emergency_sheet, favorites_sheet]:
                contacts = sheet.get_all_records()
                for contact in contacts:
                    if search_query in str(contact["Name"]).lower() or search_query in str(contact["Telephone Number"]).lower():
                        search_results.append((sheet.title, contact))

            if search_results:
                print("\nSearch Results:\n")
                for category, contact in search_results:
                    print(f"Category: {category}")
                    print("Name:", contact["Name"])
                    print("Telephone Number:", contact["Telephone Number"])
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
            print(invalid_input_yes_no)




def delete_contacts(input_color):
    """
    Deletes a contact from the specified category or from all categories.
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
        print("3. Delete contacts")
        print("4. Change color")
        print("5. Exit")
        
        choice = input("Enter the number of your choice.\n").strip()
        
        if choice == "1":
            view_existing_contacts(input_color)
        elif choice == "2":
            add_contacts(input_color)
        elif choice == "3":
            delete_contacts(input_color)
        elif choice == "4":
            input_color = choose_color(input_color)
        elif choice == "5":
            print(exit_program_with_countdown(input_color))
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")




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
    
    view_existing_contacts(chosen_color)
    
    add_contacts(chosen_color)
    
    # Protect header for all sheets
    protect_header(personal_sheet)
    protect_header(professional_sheet)
    protect_header(emergency_sheet)
    protect_header(favorites_sheet)
    
    search_contacts(chosen_color)
    
    delete_contacts(chosen_color)
    
    select_section(chosen_color)

if __name__ == "__main__":
    main()


