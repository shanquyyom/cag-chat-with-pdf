import os
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


def get_llm_response(context:str, query:str) -> str:

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
            "Please set it to your Google Gemini API key(get key from)"
        )
    

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role = "user",
            parts = [types.Part.from_text(text=query)],
        ),
    ]


    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text=(
                    "you are a helpfull assistant that can answer questions based on the provided context delimited "
                    "with triple backtickets .\n\n"
                    "You will be given a context and a user query. your task is to generate a response that is"
                    "relevent to the query based on the context provided. if the context does not contain enough"
                    "Information to answer the query, you should indicate the    do not have any information"
                    "to provide a complete answer.\n\n"
                    "If the context is empty, you should respond with a message indicating that you do not have"
                    "enough information to answer the query.\n\n"
                    "You should always respond in a friendly and helpfull manner.you should not include any "
                    "personal openions or information in your responses.\n\n "
                    f"Context:\n```{context}```"
                )
            )
        ]
    )


    response_text = ""
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,

    ):
        response_text += chunk.text
        
    return response_text