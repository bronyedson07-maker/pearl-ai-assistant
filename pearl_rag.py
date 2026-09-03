import os
from pypdf import PdfReader

class PearlDocumentReader:
    """
    Reads local PDF and text files, extracting content to answer questions.
    """

    @staticmethod
    def read_document(file_path, max_pages=10):
        """Reads text from a PDF or TXT file."""
        if not os.path.exists(file_path):
            return f"Error: File not found at '{file_path}'."

        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()

            elif ext == ".pdf":
                reader = PdfReader(file_path)
                text = ""
                total_pages = min(len(reader.pages), max_pages)

                for idx in range(total_pages):
                    page_text = reader.pages[idx].extract_text()
                    if page_text:
                        text += f"\n--- Page {idx + 1} ---\n" + page_text

                return text if text else "Could not extract text from PDF."

            else:
                return f"Unsupported file format '{ext}'. Please provide a .pdf or .txt file."

        except Exception as e:
            return f"Error reading document: {e}"