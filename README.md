# Purpose of the project
  - The purpose of the [Contact Manager](https://contact-manager-pp3-f1ca0d7e5b14.herokuapp.com/) is to allow users to create and manage their contacts in different tabs like  **Name**, **Telephone Number**, **Email**, **Birthday**, **Notes** and sort them as **Personal - Professional - Emergency - Favorites** inside a terminal environment

> <span style="color:red; font-size:35px;"> **W A R N I N G**</span>
> 
> The program takes a lot of time to load due to its bad read latency on the **Google Sheets API (GetSpreadsheet)**.
>
> I can't fix it on my present knowledge.
>
> Please be patient.
>
> <details>
> <summary>Click here to have a look on the graphs</summary>
>
> ![Warning 1](images/validation/warning/warning_1.png "asd")
>
>![Warning 2](images/validation/warning/warning_2.png "asd")
>
> ![Warning 3](images/validation/warning/warning_3.png "asdsa")
>

> </details>
## user stories

## Features
  - Select different input colors
    - a
  - View contacts
    - a
  - Add contacts
    - a
  - Search contacts
    - a
  - Edit contacts
    - a
  - Delete contacts
    - a
  - Main menu
    - a
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




## testing
- Through [PEP8](https://pep8ci.herokuapp.com/)

  <details>
    <summary>View the python validation</summary>

    ![pep8](images/validation/pep8/pep8_valid.gif)

  </details>
- 8.2 test cases (user story based with screenshots)
- 8.3 fixed bugs
## Deployment
- via Heroku
## credits
-  **𝓢𝓹𝓮𝓬𝓲𝓪𝓵 𝓣𝓱𝓪𝓷𝓴𝓼** to some fabulous people:
   - 🎓 **𝕽𝖔𝖍𝖎𝖙** - my Code Institute mentor
   - 🚀 **𝓓𝓪𝓲𝓼𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/daisy-mcgirr/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/Dee-McG)
   - 🥇 **𝓙𝓾𝓪𝓷 𝓪𝓷𝓭 𝓞𝓷𝓵𝔂** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/juan-boccia/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/)
   - ⭐️ **𝓥𝓮𝓻𝓷𝓮𝓵𝓵** [<img src="https://img.icons8.com/color/24/000000/linkedin.png"/>](https://www.linkedin.com/in/vernellclark/) [<img src="https://img.icons8.com/color/24/ffffff/github.png"/>](https://github.com/VCGithubCode)

