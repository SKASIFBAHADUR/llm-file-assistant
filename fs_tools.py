import os
from datetime import datetime
from pypdf import PdfReader
from docx import Document



def read_file(filepath: str) -> dict:
    try:
        extension = os.path.splitext(filepath)[1].lower()

        content = ""

        if extension == ".txt":
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

        elif extension == ".pdf":
            reader = PdfReader(filepath)

            for page in reader.pages:
                content += page.extract_text() or ""

        elif extension == ".docx":
            document = Document(filepath)

            for paragraph in document.paragraphs:
                content += paragraph.text + "\n"

        else:
            return {
                "success": False,
                "error": "Unsupported file format"
            }

        return {
            "success": True,
            "content": content,
            "metadata": {
                "filename": os.path.basename(filepath),
                "extension": extension,
                "size": os.path.getsize(filepath)
            }
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": "File not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    

def list_files(directory: str, extension: str = None) -> list:
    try:
        files = []

        for filename in os.listdir(directory):

            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):

                if extension is None or filename.lower().endswith(extension.lower()):

                    file_info = {
                        "name": filename,
                        "size": os.path.getsize(filepath),
                        "modified_date": datetime.fromtimestamp(
                            os.path.getmtime(filepath)
                        ).strftime("%Y-%m-%d")
                    }

                    files.append(file_info)

        return files

    except FileNotFoundError:
        return []

    except Exception as e:
        print(f"Error: {e}")
        return []



def write_file(filepath: str, content: str) -> dict:
    try:
        directory = os.path.dirname(filepath)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "message": "File created successfully",
            "filepath": filepath
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    


def search_in_file(filepath: str, keyword: str) -> dict:
    try:
        if not keyword.strip():
            return {
                "success": False,
                "error": "Keyword cannot be empty"
            }

        result = read_file(filepath)

        if not result["success"]:
            return result

        content = result["content"]

        matches = []
        search_content = content.lower()
        search_keyword = keyword.lower()

        start = 0

        while True:
            index = search_content.find(search_keyword, start)

            if index == -1:
                break

            context_start = max(0, index - 50)
            context_end = min(
                len(content),
                index + len(keyword) + 50
            )

            context = content[context_start:context_end]

            matches.append({
                "context": context
            })

            start = index + len(search_keyword)

        return {
            "success": True,
            "keyword": keyword,
            "total_matches": len(matches),
            "matches": matches
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


