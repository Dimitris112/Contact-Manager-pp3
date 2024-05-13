# Purpose of the project
   The purpose of the [Contact Manager](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/) is to allow users to create and manage their contacts in different tabs like  **Name**, **Telephone Number**, **Email**, **Birthday**, **Notes** and sort them as **Personal - Professional - Emergency - Favorites** inside a terminal environment

 <span style="color:red; font-size:35px;">  **W A R N I N G** </span>
> 
> The program takes a lot of time to load due to its bad read latency on the **Google Sheets API (GetSpreadsheet)**.
>
> I can't fix it on my present knowledge.
>
> Please be patient.
>
> <details>
>
> <summary>Click here to have a look on the graphs</summary>
>
> ![Warning 1](images/validation/warning/warning_1.png "asd")
>
> ![Warning 2](images/validation/warning/warning_2.png "asd")
>
> ![Warning 3](images/validation/warning/warning_3.png "asdsa")
>
> </details>

## user stories

  ### First timer

  - As a first timer I'd like to add my friends, colleagues, relatives - maybe one more for favorites -, in a friendly environment and be able to access them at anytime.

  ### Frequent user

   -  As a returning 



## Features

   ### Select different input colors

   - Users can change their input color to their liking from a list of **6 colors** such as `Red - Green - Yellow - Blue - Magenta - Cyan` and if they wish, they can then `Reset` it to its default color.

   ### View contacts

   - Users can view existing contacts added to the program including every **detail in each fields**.

   ### Add contacts
  
   - Users can add new contacts in four different categories *Personal - Professional - Emergency - Favorites* and also add different fields for each such as **Name - Telephone Number - Email address - Birthday - Notes**.

  ### Search contacts
  
   - Users can search through their contacts by **Name - Telephone Number - Email address - Birthday** either by `letters` or `numbers` and if any contact includes the **given input** (non case sensitive) they will be displayed.

  ### Edit contacts
  
   - Users can edit their contacts in every **category and field** they wish.

  ### Delete contacts
  
   - Users can delete either all of the contacts in every **category**, every contact in a specific **category** or a specific contact.

  ### Main menu
  
   - Users can **navigate** to each part of the program easily by entering an input from `1 through 6`.


## Flowchart

<details>
  <summary>View the flowchart</summary>

  ![Flowchart](images/validation/flowchart/flowchart.png)

</details>

### 🚀 **Technology Stack**

### Python + Libraries + Packages / ANSI Colors

All of the libraries and packages used

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
```
### 📚 Libraries and Packages

<details>
  <summary>View libraries and packages details</summary>

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