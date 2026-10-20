import json
from openai import OpenAI
from dotenv import load_dotenv

from fs_tools import read_file, list_files, write_file, search_in_file

load_dotenv()

client = OpenAI()


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a resume file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"}
                },
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"},
                    "extension": {"type": "string"},
                },
                "required": ["directory"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filepath", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search keyword in file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "keyword": {"type": "string"},
                },
                "required": ["filepath", "keyword"],
            },
        },
    },
]


AVAILABLE_FUNCTIONS = {
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "search_in_file": search_in_file,
}


def chat():

    messages = [
        {
            "role": "system",
            "content": "You are a resume analysis assistant that can read files and search resumes.",
        }
    ]

    while True:

        user_input = input("\nUser: ")

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        if msg.tool_calls:

            for tool_call in msg.tool_calls:

                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                function = AVAILABLE_FUNCTIONS[function_name]

                result = function(**arguments)

                messages.append(msg)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            print("\nAssistant:", second_response.choices[0].message.content)

        else:

            print("\nAssistant:", msg.content)


if __name__ == "__main__":
    chat()