
from fs_tools import list_files

# List all files
result = list_files("resumes")

print("All files:")
print(result)

# List only PDF files
pdf_files = list_files("resumes", ".pdf")

print("\nPDF files:")
print(pdf_files)
