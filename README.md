## 📞 **[Live application](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/)**
##### In order to open the application in a new tab, please hold **Ctrl** and left click or click it with your **mousewheel** if you're on Windows machine - hold **Command key** and left click if you're on Mac.

# Purpose of the project
   The purpose of the [Contact Manager](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/) is to allow users to create and manage their contacts in different tabs like  **Name**, **Telephone Number**, **Email**, **Birthday**, **Notes** and sort them as **Personal - Professional - Emergency - Favorites** inside a terminal environment.


## ⚠️ **WARNING** ⚠️

The program may take longer to load due to poor read latency on the *Google Sheets API (GetSpreadsheet)*.

<details>
  <summary>Click here to view the graphs</summary>
  
  ![Warning 1](images/validation/warning/warning_1.png "asd")
  
  ![Warning 2](images/validation/warning/warning_2.png "asd")
  
  ![Warning 3](images/validation/warning/warning_3.png "asdsa")
</details>

## Navigate to the README Sections

1. [User Stories](#🌟-user-stories-🌟)
    - [First Timer](#🚀-first-timer)
    - [Frequent User](#✨-frequent-user)
2. [Features](#features)
    - [Select Different Input Colors](#🎨-select-different-input-colors)
    - [View Contacts](#👀-view-contacts)
    - [Add Contacts](#➕-add-contacts)
    - [Search Contacts](#🔍-search-contacts)
    - [Edit Contacts](#🖋️-edit-contacts)
    - [Delete Contacts](#🗑️-delete-contacts)
    - [Main Menu](#🏠-main-menu)
3. [Flowchart](#flowchart)
4. [Technology Stack](#🚀-technology-stack)
5. [Testing](#testing)
    - [Python Validation](#-through-pep8)
    - [Test Cases](#test-cases)
    - [Fixed Bugs](#fixed-bugs)
6. [Deployment](#deployment)
7. [Credits](#credits)




## 🌟 User Stories 🌟

### 🚀 First Timer
🌿 **As a first timer, I'd like to:**
- **Add:** Seamlessly add my friends, colleagues, and relatives to my contacts list.
- **Organize:** Categorize contacts into Personal 🏠, Professional 💼, Emergency 🚨, and Favorites ⭐.
- **Access:** Navigate my contacts with an intuitive and visually appealing interface.
- **Manage:** Easily view, search, edit, and delete contacts with a keystrokes.
- **Experience:** Enjoy a delightful and user-friendly program, even without any prior experience with terminal-based applications.

### ✨ Frequent User
🌟 **As a returning user, I want to:**
- **Access:** Quickly retrieve previously added contacts for efficient communication.
- **Search:** Effortlessly search for contacts by name, phone number, email, or birthday.
- **Personalize:** Customize my experience by setting preferred input prompt colors and interface themes.
- **Manage:** Streamline contact management tasks with powerful batch editing and deletion features.
- **Expect:** Rely on the program's reliability, responsiveness, and lightning-fast performance for all my contact management needs.


## Features

### 🎨 Select Different Input Colors

- **Customization:** Users can personalize their experience by selecting from a vibrant palette of 6 colors, including Red, Green, Yellow, Blue, Magenta, and Cyan.
- **Reset:** With just a click, users can revert to the program's default color scheme to maintain consistency and clarity.

### 👀 View Contacts

- **Comprehensive Display:** Experience a detailed overview of all existing contacts, complete with every field meticulously organized for easy reference.

### ➕ Add Contacts

- **Effortless Addition:** Seamlessly add new contacts across four distinct categories: Personal, Professional, Emergency, and Favorites.
- **Flexible Fields:** Capture all essential contact details, including **Name**, **Telephone Number**, **Email Address**, **Birthday**, and **Notes**.

### 🔍 Search Contacts

- **Efficient Search:** Quickly locate specific contacts by **Name**, **Telephone Number**, **Email Address**, or **Birthday** using both letters and numbers.
- **Case Insensitive:** Enjoy hassle-free searching as the program ignores case sensitivity, ensuring accurate results every time.

### 🖋️ Edit Contacts

- **Customization Options:** Modify contact details with ease, providing flexibility and control over every aspect of your contact list.

### 🗑️ Delete Contacts

- **Streamlined Deletion:** Effortlessly remove unwanted contacts, whether it's clearing an entire category or targeting specific individuals for deletion.

### 🏠 Main Menu

- **Intuitive Navigation:** Seamlessly navigate between different program functionalities using simple numeric inputs, making it easy to find what you need.




## Flowchart

<details>
  <summary>View the flowchart</summary>

  ![Flowchart](images/validation/flowchart/flowchart.png)

</details>

## 🚀 **Technology Stack**

#### **Overview**

The Contact Manager project uses Python as its core programming language, supported by a range of libraries and packages. Additionally, ANSI escape codes are utilized for color customization within the terminal environment, it includes ASCII art to enhance the user interface.

#### Libraries and Packages Used

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
```

<details>
  <summary>📚View libraries and packages details</summary>

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



## Testing
  ### Through [PEP8](https://pep8ci.herokuapp.com/)

<details>

  <summary>View the python validation</summary>

  ![pep8](images/validation/pep8/pep8_valid.gif)

</details>


### Test cases
 1. Hoping off 
 2. b 
 3. c


### fixed bugs


## Deployment
- via Heroku

## credits
-  **𝓢𝓹𝓮𝓬𝓲𝓪𝓵 𝓣𝓱𝓪𝓷𝓴𝓼** to some fabulous people:
   - 🎓 **𝕽𝖔𝖍𝖎𝖙** - my Code Institute mentor [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/rohit0286)
   - 🚀 **𝓓𝓪𝓲𝓼𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/daisy-mcgirr/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/Dee-McG)
   - 🥇 **𝓙𝓾𝓪𝓷 𝓪𝓷𝓭 𝓞𝓷𝓵𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/juan-boccia/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/)
   - ⭐️ **𝓥𝓮𝓻𝓷𝓮𝓵𝓵** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/vernellclark/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/VCGithubCode)