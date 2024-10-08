import requests
from pathlib import Path

def correct_markdown_spelling(markdown_content, temperature=0.1):
    """
    Send the entire markdown content to the LLM for spelling correction.
    
    Args:
    markdown_content (str): The content to be spell-checked.
    temperature (float): Controls randomness in output. Lower values make the output more deterministic.
                         Range is typically 0.0 to 1.0, but can go higher.
    """
    prompt = f"""Please correct any spelling mistakes in the following markdown text. 
    Return the exact same text with only spelling mistakes corrected and add an asterisk after words that are corrected. 
    Maintain all original formatting, line breaks, and structure.
    Do not add any prefix to the output. Do not say "Here is the corrected markdown text with spelling mistakes corrected and asterisk added after the corrected words:"
    Do not add or remove any content, only correct spelling:

{markdown_content}"""

    response = requests.post('http://localhost:11434/api/generate',
                             json={
                                 "model": "llama3.1",
                                 "prompt": prompt,
                                 "stream": False,
                                 "temperature": temperature
                             })
    
    return response.json()['response']

def process_markdown_file(input_file_path, output_file_path, temperature=0.1):
    """Process a markdown file, perform spell checking, and save the corrected output."""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    corrected_content = correct_markdown_spelling(content, temperature)

    # Save the corrected text to a new markdown file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(corrected_content)

    return corrected_content

def main():
    input_file_path = r'C:\Store\spell_check_input.md' 
    output_file_path = r'C:\Store\spell_check_output.md' 
    temperature = 0.1
    
    process_markdown_file(input_file_path, output_file_path, temperature)

    print(f"Spell check complete. Corrected text saved to: {output_file_path}")
    print(f"Temperature used: {temperature}")

if __name__ == "__main__":
    main()