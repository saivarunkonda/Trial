import os
import requests
from fpdf import FPDF

def process_file(file_path):
    """
    Reads the file, sends its content to the Gemini API,
    and returns the extracted information.
    """
    # Read the content of the file.
    with open(file_path, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    # Construct a prompt to instruct Gemini on what to extract.
    prompt = (
        "Extract the key information from the following text:\n\n"
        f"{file_contents}\n\n"
        "Please list the important points in a clear, concise manner."
    )

    # Retrieve the Gemini API key from the environment.
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    # Define the Gemini API endpoint and headers.
    url = "https://api.gemini.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }

    # Prepare the request payload.
    payload = {
        "model": "gemini-1",  # Use the appropriate Gemini model identifier.
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 500
    }

    # Call the Gemini API.
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Gemini API call failed with status code {response.status_code}: {response.text}")

    data = response.json()
    # Assuming the API returns a similar structure to OpenAI's.
    extracted_info = data["choices"][0]["message"]["content"].strip()
    return extracted_info

def create_pdf(text, output_pdf):
    """Creates a PDF file containing the provided text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split text into lines for better formatting.
    for line in text.split('\n'):
        pdf.cell(0, 10, txt=line, ln=True)
    pdf.output(output_pdf)
    print(f"PDF created: {output_pdf}")

def main():
    # Define the directory where uploaded files are stored.
    upload_dir = "uploads"

    # List files in the uploads directory.
    try:
        files = os.listdir(upload_dir)
    except FileNotFoundError:
        print(f"The directory '{upload_dir}' does not exist.")
        return

    if not files:
        print("No files found in the uploads directory.")
        return

    # For this example, process the first file found.
    file_to_process = os.path.join(upload_dir, files[0])
    print(f"Processing file: {file_to_process}")

    # Process the file using the Gemini API.
    extracted_info = process_file(file_to_process)

    # Generate a PDF file with the extracted information.
    output_pdf = "extracted_info.pdf"
    create_pdf(extracted_info, output_pdf)

if _name_ == "_main_":
    main()
