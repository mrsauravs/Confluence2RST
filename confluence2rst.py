import requests
from bs4 import BeautifulSoup
import openai

# Fetch content from Confluence
def fetch_confluence_page(page_id, base_url, token):
    """Fetch content from Confluence using the REST API"""
    url = f"{base_url}/wiki/rest/api/content/{page_id}?expand=body.storage"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Confluence page: {e}")
        exit(1)

# Rewrite content using OpenAI
def rewrite_content_with_ai(text):
    """Use OpenAI API to rewrite content"""
    try:
        openai.api_key = input("Enter your OpenAI API Key: ").strip()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical writer rewriting content in professional US English."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error rewriting content with AI: {e}")
        return text  # Return the original text if AI fails

# Parse Confluence content
def parse_confluence_content(confluence_data):
    """Parse Confluence content and convert it to reStructuredText"""
    title = confluence_data['title']
    html_content = confluence_data['body']['storage']['value']

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize reST content
    rst_content = f"\n{'=' * len(title)}\n{title}\n{'=' * len(title)}\n\n"

    # Process each element in the Confluence page body
    for element in soup.body.children:
        if element.name == 'h1':
            text = element.text
            rewritten = rewrite_content_with_ai(text)
            rst_content += f"\n{rewritten}\n{'=' * len(rewritten)}\n"
        elif element.name == 'h2':
            text = element.text
            rewritten = rewrite_content_with_ai(text)
            rst_content += f"\n{rewritten}\n{'-' * len(rewritten)}\n"
        elif element.name == 'p':
            text = element.text
            rewritten = rewrite_content_with_ai(text)
            rst_content += f"{rewritten}\n\n"
        elif element.name == 'pre':
            rst_content += f".. code-block::\n\n    {element.text.strip().replace('\n', '\n    ')}\n\n"
        elif element.name == 'ul':
            for li in element.find_all('li'):
                text = li.text
                rewritten = rewrite_content_with_ai(text)
                rst_content += f"- {rewritten}\n"
            rst_content += '\n'
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li'), start=1):
                text = li.text
                rewritten = rewrite_content_with_ai(text)
                rst_content += f"{i}. {rewritten}\n"
            rst_content += '\n'
        elif element.name == 'table':
            rows = element.find_all('tr')
            col_widths = [max(len(cell.text) for cell in row.find_all(['th', 'td'])) + 2 for row in rows for cell in row.find_all(['th', 'td'])]

            # Table borders
            border = '+' + '+'.join(['-' * width for width in col_widths]) + '+\n'
            rst_content += border

            for row in rows:
                cells = row.find_all(['th', 'td'])
                rst_content += '|' + '|'.join([f" {cell.text.strip().ljust(width - 1)} " for cell, width in zip(cells, col_widths)]) + '|\n'
                rst_content += border

    return rst_content

# Save content to .rst file
def save_to_file(file_name, content):
    """Save content to .rst file"""
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File saved as {file_name}")
    except IOError as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    page_id = input("Enter Confluence Page ID: ").strip()
    base_url = input("Enter Confluence Base URL (e.g., https://your-domain.atlassian.net): ").strip()
    token = input("Enter Confluence API Token: ").strip()

    try:
        confluence_data = fetch_confluence_page(page_id, base_url, token)
        rst_content = parse_confluence_content(confluence_data)
        file_name = f"{confluence_data['title'].replace(' ', '_')}.rst"
        save_to_file(file_name, rst_content)
    except Exception as e:
        print(f"An error occurred: {e}")
