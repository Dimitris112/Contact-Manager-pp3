import gspread
import re
import time
import ascii_py
import sys
import phonenumbers
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
no_words = ("no", "n", "nah", "nope", "negative", "not", "nay", "never", "ne")
failed_times = "\nI can do this all day. You've failed to give a correct answer {} times.\n"
teasing_message = "Oh, close but no cigar! Give it another shot!"
invalid_input_yes_no = "\nInvalid input. Please enter (yes/no)\n"

personal_data = []

professional_data = []

emergency_data = []

favorites_data = []

telephone_pattern =  r'^[\d+\- ]+$'

input_color = None


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
    Allows the user to change the input color with confirmation.
    """
    global input_color
    
    while True:
        print("\nDo you want to change the color for your input? (yes/no)")
        choice = input().strip().lower()

        if choice in yes_words:
            print("Which color do you want?")
            print("1. Red")
            print("2. Green")
            print("3. Yellow")
            print("4. Blue")
            print("5. Magenta")
            print("6. Cyan")
            print("7. Reset")
            color_choice = input("\nEnter the number of the color you want or '7' to reset\n").strip()

            if color_choice == "1":
                chosen_color = COLORS['red']
            elif color_choice == "2":
                chosen_color = COLORS['green']
            elif color_choice == "3":
                chosen_color = COLORS['yellow']
            elif color_choice == "4":
                chosen_color = COLORS['blue']
            elif color_choice == "5":
                chosen_color = COLORS['magenta']
            elif color_choice == "6":
                chosen_color = COLORS['cyan']
            elif color_choice == "7":
                chosen_color = RESET
            else:
                print("Invalid color choice. Please enter a number between 1 and 7.\n")
                continue

            confirm_choice = input(f"You've chosen {chosen_color}as the input color.\nProceed? (yes/no)\n").strip().lower()
            if confirm_choice in yes_words:
                return chosen_color
            else:
                print("Color selection canceled. Please choose again.")
        elif choice in no_words:
            print("No problem. The input color will remain unchanged.")
            return None
        elif choice.lower() == "esc":
            print(exit_program_with_countdown())
            return ""
        else:
            print(invalid_input_yes_no)







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


def view_existing_contacts(input_color):
    """
    Prompts the user if he wants to view existing contacts
    """
    counter = 0
    while True:
        if input_color:
            print(input_color, end="")
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
                print(exit_program_with_countdown)
                return ""
            print(teasing_message)







def add_contacts(input_color):
    """
    Prompts the user if he wants to add new contacts and adds them to the selected category.
    """
    while True:
        add_contacts_input = input("\nDo you want to add new contacts? (yes/no)\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if add_contacts_input in yes_words:
            print("\nWhich category would you like to add contacts to?")
            print("Enter 'Per' for Personal, 'Pro' for Professional, 'Eme' for Emergency,\n'Fav' for Favorites or 'esc' to exit.\n")
            
            while True:
                sheet_choice = input("Enter your choice\n").capitalize()
                
                if sheet_choice in ['Per', 'Pro', 'Eme', 'Fav']:
                    break
                elif sheet_choice == "Esc":
                    return exit_program_with_countdown(input_color)
                else:
                    print("Invalid choice. Please enter 'Per', 'Pro', 'Eme' or 'Fav'.")

            if sheet_choice == 'Per':
                sheet = personal_sheet
            elif sheet_choice == 'Pro':
                sheet = professional_sheet
            elif sheet_choice == 'Eme':
                sheet = emergency_sheet
            elif sheet_choice == 'Fav':
                sheet = favorites_sheet
            
            num_contacts = 0
            contact_count = 0
            while not 1 <= num_contacts <= 5:
                num_contacts_input = input("\nHow many contacts would you like to add? (1-5)\n")
                if num_contacts_input.lower() == "esc":
                    return exit_program_with_countdown(input_color)

                try:
                    num_contacts = int(num_contacts_input)
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 5.")
                    contact_count += 1
                    if contact_count == 1:
                        print("You can't seem to follow instructions. Try again.")
                    elif contact_count == 2:
                        print("Seriously? You're still doing this wrong.")
                    elif contact_count == 3:
                        print("Come on, you can do better than this.")
                    elif contact_count >= 4:
                        print(f"Okay, I see what's happening. You've failed {contact_count} times. Are you even trying?")
                    continue

                if not 1 <= num_contacts <= 5:
                    print("Invalid input. Please enter a number between 1 and 5.")
                    contact_count += 1
                    if contact_count == 1:
                        print("You can't seem to follow instructions. Try again.")
                    elif contact_count == 2:
                        print("Seriously? You're still doing this wrong.")
                    elif contact_count == 3:
                        print("Come on, you can do better than this.")
                    elif contact_count >= 4:
                        print(f"Okay, I see what's happening. You've failed {contact_count} times. Are you even trying?")
            
            for _ in range(num_contacts):
                while True:
                    name = input("Enter contact name (up to 30 characters)\n").strip()
                    if len(name) > 30:
                        print("\nName exceeds 30 characters. Please enter a name with 30 characters or less.")
                        print("Enter 'no' if you don't want to add a contact.")
                        continue
                    elif name.lower() == "no":
                        print("So you don't want to add a contact.")
                        break
                    else:
                        break
                if name.lower() == "no":
                    break
                
                while True:
                    number = input("Enter contact number up to 20 digits (only numbers)\n")
                    if not number.isdigit():
                        print(f"Invalid telephone number. Please enter up to 20 digits containing only numbers.")
                        continue
                    elif len(number) > 20:
                        print(f"Telephone number exceeds 20 digits. Please enter up to 20 digits.")
                        continue
                    elif number.lower() == "esc":
                        return exit_program_with_countdown(input_color)
                    else:
                        break
                
                if check_duplicate_contact(name, number):
                    print("Warning: This contact already exists.")
                else:
                    add_data_with_name_column(sheet, [[name, number]], input_color)
                    print("Contact added successfully.")

            break
        elif add_contacts_input in no_words:
            print("No contacts added.")
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
 


def select_section(input_color):
    """
    Prompts the user to select an action after searching contacts
    """
    while True:
        if input_color:
            print(input_color, end="")
        print("\nWhat would you like to do next?")
        print("1. View contacts")
        print("2. Add contacts")
        print("3. Change color")
        print("4. Exit")
        
        choice = input("Enter the number of your choice.\n").strip()
        
        if choice == "1":
            view_existing_contacts(input_color)
        elif choice == "2":
            add_contacts(input_color)
        elif choice == "3":
            choose_color = choose_color()
            if choose_color is not None:
                print(choose_color + RESET)
        elif choice == "4":
            print(exit_program_with_countdown())
            break
        elif choice.lower() == "esc":
            print(exit_program_with_countdown())
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")





# Basically the function to replace the "Exiting the program" into something nice and simpler
def exit_program_with_countdown():
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
    return ""
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
        print(chosen_color + RESET)
    
    view_existing_contacts(chosen_color)
    
    add_contacts(chosen_color)
    
    # Protect header for all sheets
    protect_header(personal_sheet)
    protect_header(professional_sheet)
    protect_header(emergency_sheet)
    protect_header(favorites_sheet)
    
    search_contacts(chosen_color)
    
    select_section(chosen_color)


if __name__ == "__main__":
    main()

