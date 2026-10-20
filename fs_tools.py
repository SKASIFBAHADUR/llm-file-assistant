import os
from datetime import datetime
from PyPDF2 import PdfReader
import docx


def read_file(filepath: str):
    try:

        ext = os.path.splitext(filepath)[1].lower()
        text = ""

        if ext == ".txt":

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        elif ext == ".pdf":

            reader = PdfReader(filepath)

            for page in reader.pages:
                text += page.extract_text()

        elif ext == ".docx":

            doc = docx.Document(filepath)

            for p in doc.paragraphs:
                text += p.text + "\n"

        else:
            return {"error": "Unsupported file"}

        return {
            "status": "success",
            "content": text,
            "metadata": {
                "filename": os.path.basename(filepath),
                "size": os.path.getsize(filepath),
                "modified": datetime.fromtimestamp(
                    os.path.getmtime(filepath)
                ).isoformat(),
            },
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def list_files(directory: str, extension: str = None):

    files = []

    for file in os.listdir(directory):

        if extension and not file.endswith(extension):
            continue

        path = os.path.join(directory, file)

        if os.path.isfile(path):

            files.append(
                {
                    "name": file,
                    "size": os.path.getsize(path),
                    "modified": datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ).isoformat(),
                }
            )

    return files


def write_file(filepath: str, content: str):

    try:

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "success", "path": filepath}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_in_file(filepath: str, keyword: str):

    data = read_file(filepath)

    if data["status"] != "success":
        return data

    text = data["content"].lower()
    keyword = keyword.lower()

    matches = []

    for line in text.split("\n"):

        if keyword in line:
            matches.append(line.strip())

    return {
        "status": "success",
        "matches": matches,
    }