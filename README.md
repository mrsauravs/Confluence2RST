# Confluence2RST

A simple Python script that converts your Confluence page into restructured text.

## Prerequisites

### Install Python
Ensure Python 3.x is installed on your machine. You can check this by running:

`python --version`

`python3 --version`

If Python is not installed, download it from the official Python website.

### Install Required Libraries
The script requires the following libraries:

- requests
- beautifulsoup4
- openai

Install them using pip:

`pip install requests beautifulsoup4 openai` or,

`pip3 install requests beautifulsoup4 openai`

## Download the Script

1. Copy or download the code into a file named, for example, confluence2rst.py.

2. Save it in your working directory.

## Run the Script

1. Open a terminal or command prompt, navigate to the directory containing the script, and execute it using:

  `python confluence_to_rst.py`
  
  or, if python points to Python 2, use:
  
  `python3 confluence_to_rst.py`
  
2. Enter the following inputs when the script asks you for:

    - Confluence Page ID: Enter the unique ID of the Confluence page you want to fetch.
    - Base URL: Enter your Confluence base URL (e.g., https://your-domain.atlassian.net).
    - API Token: Provide a valid API token for authentication.

3. Check the Output
   The script will fetch the Confluence page, convert it to reStructuredText format, and save it as a .rst file in the same directory.
   The file will be named based on the title of the Confluence page, replacing spaces with underscores.

## Troubleshooting
If you encounter any errors:

- Verify the Confluence Page ID, Base URL, and API Token.
- Ensure the page is accessible using the credentials provided.
- Check the script output for specific error messages.
