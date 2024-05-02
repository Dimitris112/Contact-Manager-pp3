import gspread
import re
import csv
import time
import ascii_py
import sys
from google.oauth2.service_account import Credentials
# Not sure if I keep the CSV coz it's going to be updated along the way / after submission (possible) - bad

ascii_art = '''

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

yes_words = ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly", "ye", "ok", "okay", "okey", "alright")
no_words = ("no", "n", "nah", "nope", "negative", "not", "nay", "never")


personal_data = []

professional_data = []

emergency_data = []

favorites_data = []

telephone_pattern =  r'^[\d+\-]+$'

input_color = None


def use_program():
    """
    The function to basically ask the user if he wants to use
    the program or not
    Y - Yes  / N - No
    and then proceed accordingly
    """
    counter = 0
    while True:
        user_input = input("Do you want to use the contact manager? (yes/no). You can enter 'esc' to terminate the program anytime.\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if user_input in yes_words:
            return True
        elif user_input in no_words:
            return False
        elif user_input == "esc":
            return False
        else:
            counter +=1
            print(f"\nI can do this all day. You've failed to give a correct answer {counter} times.")



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
            color_choice = input("\nEnter the number of the color you want or '7' to reset:\n").strip()

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

            confirm_choice = input(f"You've chosen {chosen_color} as the input color. Proceed? (yes/no)\n").strip().lower()
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
            print("Invalid input. Please enter 'yes', 'no' or 'esc' to exit the program.\n")







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
        view_contacts = input("\nDo you want to view existing contacts? (Yes/No):\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if view_contacts in yes_words:
            print("\nChoose a category:")
            print("1. Personal")
            print("2. Professional")
            print("3. Emergency")
            print("4. Favorites")
            print("5. All")
            print("6. I don't want to")

            category_choice = input("\nEnter the number of the category you want to view:\n")
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
                print("Invalid choice. Please enter a number between 1 and 6.")
        elif view_contacts in no_words:
            print("No problem. You can view contacts later.")
            break
        elif view_contacts == "esc":
            print(exit_program_with_countdown(input_color))
            return ""
        else:
            counter += 1
            print(f"\nI can do this all day. You've failed to give a correct answer {counter} times.")







def add_contacts(input_color):
    """
    Prompts the user if he wants to add new contacts and adds them to the selected category.
    """
    while True:
        add_contacts_input = input("\nDo you want to add new contacts? (Yes/No):\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if add_contacts_input in yes_words:
            print("\nWhich category would you like to add contacts to?")
            print("Enter 'Per' for Personal, 'Pro' for Professional, 'Eme' for Emergency, or 'Fav' for Favorites or enter 'esc' to exit.\n")
            
            while True:
                sheet_choice = input("Enter your choice: \n").capitalize()
                
                if sheet_choice in ['Per', 'Pro', 'Eme', 'Fav']:
                    break
                elif sheet_choice == "Esc":
                    return exit_program_with_countdown(input_color)
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
                num_contacts_input = input("\nHow many contacts would you like to add? (only numbers)\n")
                try:
                    num_contacts = int(num_contacts_input)
                    break
                except ValueError:
                    if num_contacts_input.lower() == "esc":
                        return exit_program_with_countdown(input_color)
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
                        return exit_program_with_countdown(input_color)
                    else:
                        print("Invalid telephone number. Please enter only numbers, + or -")
                
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
    while True:
        export_choice = input("\nDo you want to export contacts? (Yes/No):\n").strip().lower()
        if export_choice in yes_words:
            print("\nWhich category would you like to export contacts from?\n")
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
            elif category_choice.lower() == 'esc':
                print(exit_program_with_countdown())
                return ""
            else:
                print("Invalid choice. Please enter a number between 1 and 5 or 'esc' to exit.\n")
                return

            contacts = sheet.get_all_values()
            existing_contacts = read_existing_contacts()
            contacts += existing_contacts
            export_to_csv(contacts)
            break
        elif export_choice in no_words:
            print("No problem. You can export contacts later.")
            break
        elif export_choice == "esc":
            print(exit_program_with_countdown())
            return ""
        else:
            print("Invalid input. Please enter 'Yes' or 'No', or type 'esc' to exit the program.")



    
def search_contacts(input_color):
    """
    Searches for a contact by name or telephone number.
    """
    while True:
        search_choice = input("\nDo you want to search for a contact? (yes/no):\n").strip().lower()
        if input_color:
            print(input_color, end="")
        if search_choice in yes_words:
            search_query = input("\nEnter the name or telephone number of the contact you want to search for:\n").strip().lower()
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
            print("\nInvalid input. Please enter 'yes' or 'no', or type 'esc' to exit the program.")




def print_sheet_data(sheet, input_color):
    """
    Prints the data from a specified sheet.
    """
    sheet_data = sheet.get_all_values()
    if input_color:
        print(input_color, end="")
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
        print(chosen_color + ascii_art + RESET)
    
    view_existing_contacts(chosen_color)
    
    add_contacts(chosen_color)
    
    # Add data for all sheets
    add_data_with_name_column(personal_sheet, personal_data, chosen_color)
    add_data_with_name_column(professional_sheet, professional_data, chosen_color)
    add_data_with_name_column(emergency_sheet, emergency_data, chosen_color)
    add_data_with_name_column(favorites_sheet, favorites_data, chosen_color)
    
    # Protect header for all sheets
    protect_header(personal_sheet)
    protect_header(professional_sheet)
    protect_header(emergency_sheet)
    protect_header(favorites_sheet)
    
    # Prints data from each sheet
    print_sheet_data(personal_sheet, chosen_color)
    print_sheet_data(professional_sheet, chosen_color)
    print_sheet_data(emergency_sheet, chosen_color)
    print_sheet_data(favorites_sheet, chosen_color)

    search_contacts(chosen_color)
    
    export_contacts()
    
    print(exit_program_with_countdown())


if __name__ == "__main__":
    main()


