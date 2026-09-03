import os
from pearl_rag import PearlDocumentReader

def main():
    reader = PearlDocumentReader()

    # Create a temporary test document
    sample_file = "sample_notes.txt"
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("Project Pearl Launch Plan:\n1. Complete RAG integration.\n2. Add voice wake-word.\n3. Deploy final v1.0.")

    print("--- Pearl Level 14: Document RAG Reader Test ---\n")

    content = reader.read_document(sample_file)

    print("Extracted Document Content:")
    print("-" * 45)
    print(content)
    print("-" * 45)

    # Clean up test file
    if os.path.exists(sample_file):
        os.remove(sample_file)

if __name__ == "__main__":
    main()