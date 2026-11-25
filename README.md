LLM File Assistant
A Python-based file assistant that uses an LLM's function-calling
capability to work with resume files. It can discover files, read
supported documents, search their contents, and save generated summaries
or reports.
Features
- Read files: Extract text and metadata from PDF, TXT, and DOCX
  files.
- List files: List files in a directory, optionally filtering by
  extension.
- Search files: Perform case-insensitive keyword searches and
  return matching text with surrounding context.
- Write files: Save generated text and create parent directories
  when needed.
- LLM tool calling: The LLM selects an available tool based on the
  user's natural-language request. The Python application executes the
  function and returns its result to the LLM.
Project structure
File System Assistant/
├── fs_tools.py
├── llm_file_assistant.py
├── requirements.txt
├── README.md
├── resumes/
│   ├── resume_01_aarav_mehta.pdf
│   ├── resume_02_isha_reddy.docx
│   ├── resume_03_kabir_shah.txt
│   ├── resume_04_nandini_rao.pdf
│   └── resume_05_omkar_patil.docx
└── output/
    └── all_resume_analysis.txt
The output/ directory and report file are created when the application
saves a report. Your actual filenames may differ.
Requirements
- Python 3.10 or newer
- A Groq API key
- The Python packages listed in requirements.txt
Setup
1. Open the project directory
In PowerShell, navigate to the project folder:
cd "C:\Users\YOUR_USERNAME\File System Assistant"
2. Create and activate a virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install -r requirements.txt
4. Configure the Groq API key
Set the key in the current PowerShell session:
$env:GROQ_API_KEY="your_groq_api_key"
Do not commit your API key to GitHub or place it directly in source
code. The application reads it from the GROQ_API_KEY environment
variable.
Run the application
Make sure the resumes/ directory contains your resume files, then run:
python llm_file_assistant.py
Enter a natural-language request when prompted.
Example requests
Read all resumes in the resumes folder and summarize each candidate.
Find resumes mentioning Python experience.
Read resume_01_aarav_mehta.pdf and summarize the candidate.
The application can also process a request to generate a report and save
it when that save behavior is supported by the current application code.
Available file system functions
The fs_tools.py module provides:
  Function                                                      Purpose
  read_file(filepath: str) -> dict                            Reads PDF, TXT, or DOCX files and
returns extracted content with
metadata.

  list_files(directory: str, extension: str = None) -> list   Lists files and returns their name,
size, and modified date. An
extension filter can be supplied.

  write_file(filepath: str, content: str) -> dict             Writes text to a file and creates
parent directories when required.
search_in_file(filepath: str, keyword: str) -> dict         Searches file content without case
sensitivity and returns matches
with surrounding context.
How LLM tool calling works
1. The user enters a natural-language request.
2. The application sends the conversation and tool definitions to the
   Groq model.
3. The model chooses an available tool and returns its name and
   arguments.
4. The Python application parses the arguments and calls the
   corresponding function from fs_tools.py.
5. The application sends the tool result back to the model.
6. The model may request further tool calls or return a final response.
The LLM selects and requests tools; the Python application performs the
actual file operations.
Notes and limitations
- Supported document formats for reading and searching are PDF, TXT,
  and DOCX.
- PDF text extraction depends on the PDF containing extractable text.
  Image-only scanned PDFs may require OCR, which is not included here.
- The model name and available tools are configured in
  llm_file_assistant.py.
- Keep the resumes/ directory and requested file paths consistent
  with the paths supplied in user requests.
- API access requires a valid Groq API key and an available network
  connection.
Security
- Keep API keys private.
- Do not upload real personal resumes or confidential documents to an
  LLM service unless you have permission and have considered the
  provider's data-handling terms.
- Use dummy or anonymized resumes for demonstrations and testing.
Assignment scope
This project demonstrates LLM function calling, structured tool
interfaces, programmatic file I/O, and document text extraction/search.
The README describes the current project scope and does not imply that
optional features such as OCR, a web interface, or a database are
implemented.