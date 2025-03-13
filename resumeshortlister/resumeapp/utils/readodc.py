from docx import Document

import win32com.client

def read_doc_file(file_path):
    try:
        # Initialize Word application
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # Do not show Word UI
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text  # Extract text content
        doc.Close()
        word.Quit()
        print(text)
        return text
    except Exception as e:
        return f"Error reading Word file: {e}"

# Example usage
file_path = r"C:\Users\gkhol\Downloads\manual-selenium-4-years-experience.doc"  # Replace with your file path
content = read_doc_file(file_path)
print(content)


# Example usage
# file_path = r"C:\Users\gkhol\Downloads\manual-selenium-4-years-experience.doc" # Replace with the path to your Word document
# content = read_word_file(file_path)
# print(content)  # Print the extracted text
