
import os
import json

from groq import Groq

from fs_tools import list_files, read_file, search_in_file, write_file


# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-20b"


# Define available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory. Optionally filter by extension.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path."
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional extension such as .pdf or .txt."
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a PDF, TXT, or DOCX file and extract its content and metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search for a keyword inside a PDF, TXT, or DOCX file and return matching text with surrounding context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path of the file to search."
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for."
                    }
                },
                "required": ["filepath", "keyword"]
            }
        }
    }
]


# Get user query

# Get user query
user_query = input("What would you like me to do? ")


# Initialize conversation

messages = [
    {
        "role": "system",
        "content": (
            "You are an intelligent file assistant. "
            "Use the available tools to perform file operations. "
            "The only available tools are list_files, read_file, and search_in_file. "
            "Never attempt to call write_file or any other unavailable tool. "
            "When asked about file contents, use read_file before answering. "
            "Use list_files when you need to discover files. "
            "Use search_in_file when asked to find a specific keyword inside a file. "
            "Never invent file paths or file contents. "
            "Resumes are stored in the resumes directory. "
            "When asked about resumes, first use list_files to discover files. "
            "When asked to analyze multiple resumes, read every requested resume before generating the report. "
            "After reading all resumes, generate the complete report directly as your final text response. "
            "Do not request a tool to save the report. "
            "The Python application will save your final response automatically."
        )
    },
    {
        "role": "user",
        "content": user_query
    }
]




# Allow multiple tool-calling rounds
MAX_ITERATIONS = 12

for iteration in range(MAX_ITERATIONS):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # If the LLM has no more tools to execute
    if not message.tool_calls:

        final_content = message.content or ""

        print("\nFinal Assistant Response:")
        print(final_content)

        # Save the final response if the user requested this report file
        if "output/all_resume_analysis.txt" in user_query.lower():

            save_result = write_file(
                "output/all_resume_analysis.txt",
                final_content
            )

            print("\nFile Saving Result:")
            print(save_result)

        break

    # Add assistant's tool request to conversation
    messages.append(message)

    # Execute every requested tool
    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        arguments_dict = json.loads(
            tool_call.function.arguments
        )

        print("\nTool name:", tool_name)
        print("Tool arguments:", arguments_dict)

        if tool_name == "list_files":

            directory = arguments_dict["directory"]
            extension = arguments_dict.get("extension")

            if extension and not extension.startswith("."):
                extension = "." + extension

            result = list_files(directory, extension)

        elif tool_name == "read_file":

            filepath = arguments_dict["filepath"]
            result = read_file(filepath)

        elif tool_name == "search_in_file":

            filepath = arguments_dict["filepath"]
            keyword = arguments_dict["keyword"]

            result = search_in_file(filepath, keyword)


        else:

            result = {
                "success": False,
                "error": "Unknown tool"
            }

        print("Execution result:", result)

        # Return tool result to the LLM
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

else:
    print("\nMaximum tool-calling iterations reached.")
