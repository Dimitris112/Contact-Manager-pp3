## 📞 **[Live application](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/)**
##### In order to open the application in a new tab, please hold **Ctrl** and left click or click it with your **mousewheel** if you're on Windows machine - hold **Command key** and left click if you're on Mac.

# Purpose of the project
   The purpose of the [Contact Manager](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/) is to allow users to create and manage their contacts in different tabs like  **Name**, **Telephone Number**, **Email**, **Birthday**, **Notes** and sort them as **Personal - Professional - Emergency - Favorites** inside a terminal environment.


## ⚠️ **WARNING** ⚠️

The program may take longer to load due to poor read latency on the *Google Sheets API (GetSpreadsheet)*.

<details>
  <summary><strong>Click here to view the graphs</strong></summary>
  
  ![API & Services google sheets & google drive API graphs](images/validation/warning/warning_1.png)
  
  ![API & Services showing high Methods GetSpreadsheet latency and graphs](images/validation/warning/warning_2.png)
  
  ![IAM & Admin Authentication graphs](images/validation/warning/warning_3.png)
</details>

## Navigate to the README Sections

1. [User Stories 🌟](#user-stories-)
    - [First Timer 🚀](#first-timer-)
    - [Frequent User ✨](#frequent-user-)
2. [Features 📋](#features-)
    - [Select Different Input Colors 🎨](#select-different-input-colors-)
    - [View Contacts 👀](#view-contacts-)
    - [Add Contacts ➕](#add-contacts-)
    - [Search Contacts 🔍](#search-contacts-)
    - [Edit Contacts 🖋️](#edit-contacts-)
    - [Delete Contacts 🗑️](#delete-contacts-)
    - [Main Menu 🏠](#main-menu-)
3. [Technology Stack ⚙️](#technology-stack-)
    - [Overview](#overview)
    - [Tools 🛠️](#tools-️)
    - [API 🔌](#api-)
    - [Libraries and Packages Used](#libraries-and-packages-used)
    - [ANSI Escape codes and ASCII Art](#ansi-escape-codes-and-ascii-art)
    - [Flowchart 🗺️](#flowchart-)
4. [Testing 📝](#testing-)
    - [Python Validation](#python-validation)
    - [Test Cases](#test-cases)
    - [Fixed Bugs 🐛](#fixed-bugs-)
    - [Unfixed issues](#unfixed-issues)
5. [Deployment 🌐](#deployment-)
    - [Via Heroku](#via-heroku)
    - [Via Git clone](#via-git-clone)
6. [Credits 🙏](#credits-)


##  User Stories 🌟

###  First Timer 🚀
🌿 **As a first timer, I'd like to:**
- **Add:** Seamlessly add my friends, colleagues, and relatives to my contacts list.
- **Organize:** Categorize contacts into Personal 🏠, Professional 💼, Emergency 🚨, and Favorites ⭐.
- **Access:** Navigate my contacts with an intuitive and visually appealing interface.
- **Manage:** Easily view, search, edit, and delete contacts with a keystroke.
- **Experience:** Enjoy a delightful and user-friendly program, even without any prior experience with terminal-based applications.

###  Frequent User ✨
🌟 **As a returning user, I want to:**
- **Access:** Quickly retrieve previously added contacts for efficient communication.
- **Search:** Effortlessly search for contacts by name, phone number, email, or birthday.
- **Personalize:** Customize my experience by setting preferred input prompt colors and interface themes.
- **Manage:** Streamline contact management tasks with powerful batch editing and deletion features.
- **Expect:** Rely on the program's reliability, responsiveness, and lightning-fast performance for all my contact management needs.


## Features 📋

###  Select Different Input Colors 🎨

- **Customization:** Users can personalize their experience by selecting from a vibrant palette of 6 colors, including Red, Green, Yellow, Blue, Magenta, and Cyan.
- **Reset:** With just a click, users can revert to the program's default color scheme to maintain consistency and clarity.

###  View Contacts 👀

- **Comprehensive Display:** Experience a detailed overview of all existing contacts, complete with every field meticulously organized for easy reference.

###  Add Contacts ➕

- **Effortless Addition:** Seamlessly add new contacts across four distinct categories: Personal, Professional, Emergency, and Favorites.
- **Flexible Fields:** Capture all essential contact details, including **Name**, **Telephone Number**, **Email Address**, **Birthday**, and **Notes**.

###  Search Contacts 🔍

- **Efficient Search:** Quickly locate specific contacts by **Name**, **Telephone Number**, **Email Address**, or **Birthday** using both letters and numbers.
- **Case Insensitive:** Enjoy hassle-free searching as the program ignores case sensitivity, ensuring accurate results every time.

###  Edit Contacts 🖋️

- **Customization Options:** Modify contact details with ease, providing flexibility and control over every aspect of your contact list.

###  Delete Contacts 🗑️

- **Streamlined Deletion:** Effortlessly remove unwanted contacts, whether it's clearing an entire category or targeting specific individuals for deletion.

###  Main Menu 🏠

- **Intuitive Navigation:** Seamlessly navigate between different program functionalities using simple numeric inputs, making it easy to find what you need.


##  **Technology Stack ⚙️** 

### **Overview**

The project structure is built upon the [Code Institute P3 template](https://github.com/Code-Institute-Org/p3-template), including custom Python code, along with the integration of ANSI escape codes and ASCII art for visual appeal and user interface enhancement.

### Tools 🛠️

- **Git** Used for version control eg. **`git`** `add - commit - push`
- **Github** Used as the hosting platform for the repository.
- **Gitpod** Used as the IDE for writing, editing and debugging code.
- **Heroku** Used for deploying the application.
- **Python** Used as the programming language for creating the application.
- **Gspread** Used for interacting with Google Sheets.
- **Tabulate** Used to format data into tables for easy reading.
- **Numpy** Used for handling large amounts of data efficiently.
- **OpenCV** Used for advanced image processing tasks.
- **Requests-OAuthlib** Used to connect to Google services.
- **StrEnum** Used to manage string constants.
- **ANSI Escape Codes** Used to add color to terminal text.


### API 🔌
- **Google Sheets** Used for managing data stored in Google Sheets.
- **Google Drive** Used to manage file permissions and sharing the stored data.

### Libraries and Packages Used

```python
import gspread
import re
import time
import sys
from tabulate import tabulate
from google.oauth2.service_account import Credentials

"""
Requirements
"""
cachetools==5.3.3
google-auth==2.29.0
google-auth-oauthlib==1.2.0
gspread==6.1.0
numpy==1.26.4
oauthlib==3.2.2
opencv-python==4.9.0.80
pyasn1==0.6.0
pyasn1_modules==0.4.0
requests-oauthlib==2.0.0
rsa==4.9
StrEnum==0.4.15
tabulate==0.9.0
```
### ANSI Escape codes and ASCII Art
```python
# ANSI Escape codes
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m'
}
RESET = '\033[0m'

# Ascii art
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
# Font Name: Big Money-ne / Contact Manager
# https://patorjk.com/software/taag/#p=display&f=Big%20Money-ne&t=Contact%0AManager
```
### Users can enter a variety of inputs such as 'yes' and 'no'
```python
yes_words = ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative",
             "absolutely", "sure", "aye", "certainly", "ye", "ok", "okay",
             "okey", "alright", "ya", "ofc", "yep", "definitely",
             "exactly", "for sure", "fo sho")

no_words = ("no", "n", "nah", "nope", "negative", "not", "nay", "never",
            "ne", "nop", "na")
```
### This adds a human element to the user experience

### Here lie the details for each of the libraries and package used in this project

<details>
  <summary><strong>Click to view libraries and package details</strong></summary>

- **cachetools**: Provides caching utilities.
- **google-auth**: Handles authentication for Google APIs.
- **google-auth-oauthlib**: Google authentication with OAuth.
- **gspread**: Interacts with Google Sheets.
- **numpy**: Performs numerical computations efficiently.
- **oauthlib**: Implements OAuth for Python applications.
- **opencv-python**: Offers computer vision capabilities.
- **pyasn1**: Supports ASN.1 data encoding and decoding.
- **pyasn1_modules**: Additional modules for pyasn1.
- **requests-oauthlib**: Implements OAuth for HTTP requests.
- **rsa**: Implements RSA encryption and decryption.
- **StrEnum**: Implements string enumerations.
- **tabulate**: Formats tabular data for easy display.

</details>


## Flowchart 🗺️

### Used **[Lucid Chart](https://www.lucidchart.com/pages/)** to draw it.

<details>

<summary><strong>Click to view the flowchart</strong></summary>

![Flowchart from Start to End of the program](images/validation/flowchart/flowchart.png)

</details>


## Testing 📝

### Through **[PEP8](https://pep8ci.herokuapp.com/)**

<details>

  <summary><strong>Click to view the python validation</strong></summary>

  ![PEP8 python validation gif](images/validation/pep8/pep8_valid.gif)

</details>


### Test cases

#### Start

- The **first thing** the users come to see when the land on the program, deciding whether to use the program or not with different outcomes.

  <details>

  <summary><strong>Click to view the main shot and the yes or no outputs</strong></summary>

  ### Main

  ![Main shot of the program showing the ASCII Art](images/main_shot.png)
    ### Upon launching the program, users are greeted with an eye-catching ASCII art, setting the tone for their interaction with the application.

  ### Start Confirmation - 'Yes'

  ![Enter 'yes' to start the program](images/validation/test_cases/start/start_yes.png)
    ### Users can initiate the program by entering 'yes', signaling their intent to proceed with the contact management functionality.

  ### Start Confirmation - 'No'

  ![Enter 'no' to terminate the program](images/validation/test_cases/start/start_no.png)
    ### If users decide not to proceed, they can enter 'no' to terminate the program.

  ### Termination - 'Esc'
  ![Enter 'esc' to terminate the program](images/validation/test_cases/start/start_esc.png)
    ### Alternatively, users can terminate the program at any time by entering 'esc', providing a quick exit option.

  </details>

#### Choose color prompt

- After the users choose to `use` essentially the program, they come across to the `choose color` functionality. Users can choose up to 6 colors which are *Red - Green - Yellow - Blue - Magenta - Cyan* as their input color, upon selecting one (1 - 6), then a `confirmation prompt` will appear to the users to hit `yes or no`, if the input is `yes` then the program continues with the selected color, else it loops back. The users can also turn the color back to default by entering `7`.

    <details>

    <summary><strong>Click to view the choose color functionality options</strong></summary>

    ![Prompt to choose yes / no and 1 - 7 for color choice](images/validation/test_cases/colors/choose_color_yes.png)
    ![Input as 'no' in color choice](images/validation/test_cases/colors/choose_color_no.png)
    ![Text color is red](images/validation/test_cases/colors/color_red.png)
    ![Text color is green ](images/validation/test_cases/colors/color_green.png)
    ![Text color is yellow](images/validation/test_cases/colors/color_yellow.png)
    ![Text color is blue](images/validation/test_cases/colors/color_blue.png)
    ![Text color is magenta](images/validation/test_cases/colors/color_magenta.png)
    ![Text color is cyan](images/validation/test_cases/colors/color_cyan.png)
    ![Text color is default](images/validation/test_cases/colors/color_default.png)

    </details>

#### View existing contact

- Once the users choose to change the input color (or not), the next thing they'll come to face are the prompt to `View existing contacts` on the program.

  <details>

  <summary><strong>Click to view the view contacts functionality</strong></summary>

  ### Enter 'yes' to choose a category
  ![Enter 'yes' to choose a category](images/validation/test_cases/view_contacts/view_contacts_yes.png)
  ### Confirm your choice by entering 'yes' to view contacts

  ### Show existing contacts in Personal
  ![Show existing contacts in Personal](images/validation/test_cases/view_contacts/view_personal.gif)
  ### See contacts categorized as 'Personal'

  ### Show existing contacts in Professional
  ![Show existing contacts in Professional](images/validation/test_cases/view_contacts/view_professional.png)
  ### Display contacts labeled as 'Professional'

  ### Show existing contacts in Emergency
  ![Show existing contacts in Emergency](images/validation/test_cases/view_contacts/view_emergency.png)
  ### View contacts listed under 'Emergency'

  ### Show existing contacts in Favorites
  ![Show existing contacts in Favorites](images/validation/test_cases/view_contacts/view_favorites.gif)
  ### Display contacts marked as 'Favorites'

  ### Show all existing contacts in all Categories
  ![Show all existing contacts in all Categories](images/validation/test_cases/view_contacts/view_all.gif)
  ### View all contacts across categories

  ### Don't want to view existing contacts
  ![Don't want to view existing contacts](images/validation/test_cases/view_contacts/view_dont_want.png)
  ### Skip viewing contacts by selecting '6'

  </details>



#### Add contacts

- When the users are done with `viewing existing contacts`, they can **add new contacts** in any of the categories they wish to *Personal - Professional - Emergency - Favorites* and have different fields for each of them such as *Name - Telephone number - Email address - Birthday - Notes* (name and telephone number are <ins>**mandatory**</ins>). Or they can just skip this action and move forward, or enter `esc` and terminate the program. Upon `invalid input` provided by the user, a new prompt will keep looping until `valid input` is provided.

  <details>

  <summary><strong>Click to view add contacts</strong></summary>
  
  ### All of the process of adding contacts
  ![All of the process of adding contacts](images/validation/test_cases/add_contacts/add_contact.gif)

  </details>

### Search contacts
- Users can search for contacts by *Name - Telephone number - Email address - Birthday*. It's designed to be non-case sensitive, guaranteeing easy access without any obstacles. Additionally, users have the option to skip this process by entering `no` or `esc` to terminate the program.

  <details>

  <summary><strong>Click to view search contacts functionality</strong></summary>

  ### Contacts are found
  ![Contacts are found in the search section](images/validation/test_cases/search_contacts/search_found.gif)
  ### Contacts found and displayed on tabulate format 

  ### No contacts found
  ![No contacts found in the search section](images/validation/test_cases/search_contacts/search_no_match.png)
  ### No matching contacts were found in the search results

  </details>

#### Edit contacts

- Users can **edit existing contacts** by choosing the `edit contacts` option. They start by selecting a category from which they want to edit contacts, such as **Personal** or **Professional**. Then, they choose the specific contact they wish to edit. Users can modify various fields like **Name**, **Telephone Number**, **Email**, **Birthday** and **Notes**. After making the edits, they see a confirmation message and the updated contact details are displayed. Finally, users can continue editing contacts, move to the next functionality of the program,return to the `main menu` or `terminate` the program.


  <details>

  <summary><strong>Click to view edit contacts functionality</strong></summary>

  ### All of the process of editing contacts
  ![The whole process of editing contacts in gif](images/validation/test_cases/edit_contacts/edit_contact.gif)
  ### Users choose the category of the contact to edit, the field of it and see the updated data. Also they can go back by 'cancel'.

  </details>


#### Delete contacts

- Users can **delete contacts** 

  <details>

  <summary><strong>Click to view delete contacts functionality</strong></summary>

  ### The process of deleting all contacts in a specific category
  ![The process of deleting all contacts in a specific category](images/validation/test_cases/delete_contacts/delete_specific_all.gif)
  ### Also in this case if the user decides to delete all contacts in all categories, there will be a new confirmation prompt

  ### The process of deleting individual contacts
  ![The process of deleting individual contacts](images/validation/test_cases/delete_contacts/delete_specific.gif)
  ### Once the contact is deleted, a message will appear telling the users that it's removed successfully.
  </details>



#### Main menu

- The main menu provides users with a convenient way to **navigate** back to each function of the program or **exit** manually.

  <details>

  <summary><strong>Click to view main menu</strong></summary>

  ### Inputs from 1 to 5 bring the user back to each function
  ![Main menu options for navigating back to each function](images/validation/test_cases/select_section/menu_exit.png)
  ### If the input is 6, exit the program

  </details>


## Fixed bugs 🐛

  ### Section 1

  <details>

  <summary><strong>Click to view first bug fixed</strong></summary>

  ### In this update, I focused on cleaning up the code, removing redundancy, and improving readability without affecting the core functionality.

1. **Removed Duplicate Print Statements**
   - Deleted a duplicate print statement that printed the existing data.
   - Removed redundant print statements within functions to avoid unnecessary output.

2. **Simplified Conditional Blocks**
   - Refactored the code to simplify the conditional blocks for better clarity and maintenance.

3. **Improved Function Logic**
   - Streamlined the `add_contacts` function by removing duplicate success messages.
   - Enhanced the `print_sheet_data` function to avoid redundant data prints.

4. **Indented Comments for Clarity**
   - Adjusted comment indentation to align with related code blocks, improving code readability.

5. **Removed Unnecessary Calls**
   - Eliminated the call to `main()` within the `if __name__ == "__main__":` block to simplify script execution logic.

 </details>


  ### Section 2

  <details>

  <summary><strong>Click to view second bug fixed</strong></summary>

  ### These changes help to maintain a cleaner codebase, reduce redundancy, and make the script more efficient and easier to read.
  
  - **Function:** `want_to_view_existing_contacts`
    - Improved return logic for better readability and efficiency.
    - **Before**
      ```python
      return view_contacts in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap"]
      ```
    - **After**
      ```python
      if view_contacts in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap"]:
          return True
      else:
          return False
      ```

  - **Function:** `want_to_add_contacts`
    - Added a new function to check if the user wants to add new contacts.
      ```python
      def want_to_add_contacts():
          """
          Asks the users if they want to add new contacts
          Returns True if they do, False otherwise
          """
          add_contacts_input = input("\nDo you want to add new contacts? (Yes/No): ").strip().lower()
          return add_contacts_input in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap"]
      ```

  - **Function:** `main`
    - Updated the main function to use `want_to_view_existing_contacts` and `want_to_add_contacts`.
    - **Before**
      ```python
      if want_to_view_existing_contacts():
          view_existing_contacts()
      add_contacts()
      ```
    - **After**
      ```python
      if want_to_view_existing_contacts():
          view_existing_contacts()
      if want_to_add_contacts():
          add_contacts()
      ```

  </details>


  ### Section 3
  
  <details>

  ### These updates standardize user input handling across the application, enhance the user experience.

  <summary><strong>Click to view third bug fixed</strong></summary>

  
  - **Global Variables**
    - Added comprehensive lists of affirmative and negative words to handle various user inputs more efficiently.
    - **Before**
      ```python
      yes_words = ("yes", "y", "yeah", "yeap", "yup", "yea", "yap")
      no_words = ("no", "n", "nah", "nope", "negative")
      ```
    - After
      ```python
      yes_words = ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly", "ye", "ok", "okay", "okey", "alright")
      no_words = ("no", "n", "nah", "nope", "negative", "not", "nay", "never")
      ```

  - **Function:** `use_program`
    - Updated to handle 'esc' input for terminating the program and improved word matching for 'yes' and 'no'.
    - Before
      ```python
      user_input = input("Do you want to use the contact manager? (yes/no):\n").strip().lower()
      if user_input in ("yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly","ye", "ok", "okay", "okey"):
      ```
    - **After**
      ```python
      user_input = input("Do you want to use the contact manager? (yes/no). You can enter 'esc' to terminate the program anytime.\n").strip().lower()
      if user_input in yes_words:
      ```

  - **Function:** `choose_color`
    - Refactored to use the comprehensive list of affirmative words.
    - **Before**
      ```python
      if choice in ["yes", "y", "yeah", "yeap", "yup", "yea", "yap", "affirmative", "absolutely", "sure", "aye", "certainly","ye", "ok", "okay", "okey"]:
      ```
    - **After**
      ```python
      if choice in yes_words:
      ```

  - **Other Functions**
    - Refactored similar input handling logic for consistency and better readability
      - `view_existing_contacts`
      - `add_contacts`
      - `export_contacts`
      - `search_contacts`

  - **Function:** `exit_program_with_countdown`
    - Fixed a missing `sys.exit()` call to properly terminate the program.
    - Added `sys.exit()` at the end of the function.

  </details>

### Section 4

<details>

<summary><strong>Click to view fourth bug fixed</strong></summary>

### These changes ensure that the deletion of contacts is handled more accurately, preventing potential data inconsistencies and enhancing user experience.

  - **Function:** `delete_contacts`
    - Ensured the proper deletion of rows in sheets.
    - **Before**
      ```python
      if confirm_choice in yes_words:
          # Clear all contacts in all categories
          for sheet in all_categories:
              sheet.clear()
              sheet_data = sheet.get_all_values()
              # Deletes from 2nd row onwards
              if len(sheet_data) > 1:
                  sheet.delete_rows(2, len(sheet_data))
          print("All contacts in all categories deleted successfully.")
      else:
          print("Deletion canceled.")
      break
      ```
    - **After**
      ```python
      if confirm_choice in yes_words:
          # Clear all contacts in all categories
          for sheet in all_categories:
              sheet.clear()
              sheet_data = sheet.get_all_values()
              # Deletes from 2nd row onwards
              if len(sheet_data) > 1:
                  sheet.delete_rows(2, len(sheet_data))
          print("All contacts in all categories deleted successfully.")
      else:
          print("Deletion canceled.")
      break

      # If the user selects a specific category
      sheet = all_categories[category_index]
      ```
    - Improved handling of deletion in a specific category.
    - **Before**
      ```python
      if action_choice in yes_words:
          sheet.clear()
          sheet_data = sheet.get_all_values()
          if len(sheet_data) > 1:
              sheet.delete_rows(2, len(sheet_data))
          print(f"All contacts in {sheet.title} category deleted successfully.")
      ```
    - **After**
      ```python
      if action_choice in yes_words:
          sheet.clear()
          sheet_data = sheet.get_all_values()
          if len(sheet_data) > 1:
              sheet.delete_rows(2, len(sheet_data))
          print(f"All contacts in {sheet.title} category deleted successfully.")
      elif action_choice in no_words:
          print("Deletion canceled.")
      ```

</details>

### Section 5

<details>

<summary><strong>Click to view fifth bug fixed</strong></summary>

### These updates enhance the functionality of adding and editing contacts, ensuring proper validation and consistent updates to the contact information.

  - **Function:** `add_contacts`
    - Improved email validation logic to check for length and proper format.
    - **Before**
      ```python
      if email_prompt in yes_words:
          email = input("\nEnter the contact's email address\n").strip()
          if '@' not in email or '.' not in email or email.count('@') != 1:
      ```
    - **After**
      ```python
      if email_prompt in yes_words:
          email = input("\nEnter the contact's email address (30 chars max)\n").strip()
          if len(email) > 30:
              print("\nEmail address exceeds 30 characters. Please enter a valid email address with 30 characters or less.")
              continue
          elif '@' not in email or '.' not in email or email.count('@') != 1:
              print("\nInvalid email address. Please enter a valid email address containing one '@' and at least one '.'")
              continue
      ```

- **Function:** `edit_contacts`
  - Improved logic to handle editing of specific fields and ensure proper sheet updates.
  - **Before**
    ```python
    contact += [''] * (field_index - len(contact) + 1)
    contact[field_index] = new_value
    sheet.update_row(contact_index, contact)
    sheet.update_cell(contact_index, field_index + 1, new_value)
    print("Contact updated successfully.")
    print(tabulate([contact], headers=headers, tablefmt="pretty"))
    ```
  - **After**
    ```python
    contact += [''] * (field_index - len(contact) + 1)
    contact[field_index] = new_value
    sheet.update_cell(contact_index, field_index + 1, new_value)
    print("Contact updated successfully.")
    updated_contact = sheet.row_values(contact_index)
    print(tabulate([updated_contact], headers=headers, tablefmt="pretty"))
    ```

</details>


## Unfixed issues
  Can't fix at this moment the read latency issue which sometimes lead to error 500 (timeout) due to high latency.
  For more info refer to [Warning](#️-warning-️)

## Deployment 🌐
### **<ins>BEFORE</ins> you move onto the *Heroku* part, you need to set your own Credentials**.

  <details>

  <summary><strong>Click to view how to set your own Credentials</strong></summary>

  1. Go to [Google Cloud Platform](https://console.cloud.google.com/welcome/new?pli=1).
  2. On the upper left corner click `Select a project` dropdown. Hit **New Project**.
  3. On the project name, enter your own. Then click *Create*, you don't have to change the *Location*.
  4. Once you're inside your project **dashboard**, on the left side click on the `☰` and select **APIs & Services** and then **Library**.
  5. In the searchbox, type **Google Drive API**, select it and click *Enable*.
  6. Now since you're inside the Google Drive API dashboard, on your `right` you should see **Create Credentials**. Click on that and now the magic begins.
  7. On the *Credential Type* menu leave it as **Google Drive API** and on the data radio boxes, select **Application data** and hit `Next`.
  8. Enter your *Service account name* - e.g this project is **ContactManager** - then click *Create and Continue*.
  9. On the role dropdown menu enter `Editor` and continue.
  10. You can skip this step - leave empty and click **Done**.
  11. Navigate to the **Credentials** menu on the left side of your screen, click on *Service Accounts* on what's been created.
  12. Click on **KEYS** and click on **ADD KEY** dropdown and **Create new key**. Select *JSON* and *Create*.
  13. Now your credentials are created and downloaded on the path of your choosing.
  14. They will have a "random" name, so the best thing to do now is to rename them into **creds.json**.

  *15. In order to activate the **Google Sheets API** it's quite similar and simpler. Simply go to the *Library* and search **Google Sheets API**, select it and click *Enable*. Done.

  </details>

### Via Heroku

  <details>

  <summary><strong>Click to view Heroku's deployment instructions</strong></summary>

  1. **Sign Up/Login to Heroku**
      - If you haven't already, sign up for a Heroku account at [Heroku's website](https://www.heroku.com/) or log in if you already have an account.

  2. **Create a New App on Heroku**
       - Once logged in, navigate to your Heroku dashboard and click on the **New** button, then select **Create new app**.
       - Choose a unique name for your app and select the region closest to your location.

  3. **Connect GitHub Repository**
       - After creating your app, go to the **Deploy** tab within your app's dashboard.
       - Under the **Deployment method** section, select **GitHub** as the deployment method.
       - Search for your GitHub repository in the **Connect to GitHub** section and click **Connect**.

  4. **Configure Deployment Options**
       - Once connected, choose the branch you want to deploy (e.g. *main*) and optionally enable automatic deploys for future commits.

  5. **Select Framework**
      - Since the Contact Manager includes both Python and Node.js components, you need to specify the correct buildpacks for deployment. 
       - Under the *Settings* tab of your Heroku app, navigate to the **Buildpacks** section and add the appropriate buildpacks for Python and Node.js.
       - <ins>***It's important to add the Python buildpack first***</ins>
       - Also, add the following environment variables
       - **CREDENTIALS.JSON** (or if you've named yours as *CREDS*) type on the "Key" box **CREDS** and on its right "Value" enter your own Creds info.
        - **PORT** set to **8000** to specify the port on which your app will run.

  6. **Deploy Branch**
       - After configuring the deployment options, manually deploy your application by clicking the **Deploy Branch** button.

  7. **Monitor Deployment Progress**
       - Heroku will start deploying your application from the selected GitHub branch. You can monitor the deployment progress from the activity log on the same page.

  8. **View Application**
      - Once the deployment is complete, Heroku will provide you with a URL to access your deployed application. Click on **View** button to open your application in a new tab.

  </details>


### Via git clone

<details>

<summary><strong>Click to view how to clone this repository</strong></summary>

  1. **Clone the repository**
      ```
      git clone https://github.com/Dimitris112/Contact-Manager-pp3.git
       ```

  2. **Navigate to the Repository**
      ```
      cd Contact-Manager-pp3
      ```

  3. *Setup your environment - make sure you have **[Python](https://www.python.org/downloads/) and [Node JS](https://nodejs.org/en)** installed on your machine.*

  4. **Run the app**
      - Navigate to the project directory and run this python script.
         ```
        python run.py 
         ```
        `run.py` of course if you've named your own as this. <ins>Optional</ins> you can use `python3 run.py`, depending on your version.

 5. **Commit changes**
      - After making changes, commit them to your repository
        ```
        git add .
        git commit -m "Your message"
        ```

6. **Push changes to GitHub**
      ```
      git push origin main
      ```

</details>

## Credits 🙏
- Used ***[rxaviers](https://gist.github.com/rxaviers/7360908)*** Complete list of github markdown emoji markup
- Used [ChatGPT 3.5](https://chatgpt.com/?oai-dm=1) / [Codeium](https://codeium.com/) / [Stack Overflow](https://stackoverflow.com/) for minor improvements and better explanation on my
requests for this project.
- The main idea for this project was obtained by the [Love Sandwiches](https://www.youtube.com/watch?v=Tns6HiDkVUI) walkthrough project of the [Code Institute course](https://codeinstitute.net/global/).

  ### 🙏 **𝓢𝓹𝓮𝓬𝓲𝓪𝓵 𝓣𝓱𝓪𝓷𝓴𝓼 𝓽𝓸 𝓼𝓸𝓶𝓮 𝓯𝓪𝓫𝓾𝓵𝓸𝓾𝓼 𝓹𝓮𝓸𝓹𝓵𝓮** 🙏
  - 🎓 **𝕽𝖔𝖍𝖎𝖙** - **Code Institute Mentor** [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/rohit0286)
  - 🚀 **𝓓𝓪𝓲𝓼𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/daisy-mcgirr/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/Dee-McG)
  - 🥇 **𝓙𝓾𝓪𝓷 𝓪𝓷𝓭 𝓞𝓷𝓵𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/juan-boccia/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/jbocciadev)
  - ⭐️ **𝓥𝓮𝓻𝓷𝓮𝓵𝓵** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/vernellclark/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/VCGithubCode)