from pypdf import PdfReader

file_path = r"C:\Users\YourName\Documents\python_notes.pdf"

try:
    reader = PdfReader(file_path, strict=False)

    print("PDF opened successfully!")
    print("Total pages:", len(reader.pages))

    for page_number, page in enumerate(reader.pages, start=1):
        print(f"\n--- Page {page_number} ---")

        text = page.extract_text() or ""

        print(text)

except Exception as error:
    print("PDF reading failed!")
    print("Error type:", type(error).__name__)
    print("Error:", str(error))