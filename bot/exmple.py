# Smaple code example on how to use the openai api.py
from langchain_core.output_parsers import StrOutputParser
from openai_api import (get_ai_response,
                        get_api_key,
                        initialize_chat_openai,
                        load_environment)


def main():
    load_environment()
    api_key = get_api_key()
    base_url = "https://api.avalai.ir/v1"
    model = "gpt-3.5-turbo-0125"
    
    user_message = "capatil of Japan?"
    
    llm = initialize_chat_openai(model, base_url, api_key)
    parser = StrOutputParser()
    response = get_ai_response(user_message, llm, parser)

    print("AI:", response)

if __name__ == "__main__":
    main()
