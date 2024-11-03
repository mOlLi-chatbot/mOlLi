import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


def initialize_chat_openai(
    model: str,
    base_url: str,
    api_key: str,
    temperature: float = 0.0,
    max_retries: int = 2
) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI instance."""
    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature,
        max_retries=max_retries,
    )

def get_ai_response(
    user_message: str,
    llm: ChatOpenAI,
    parser: StrOutputParser
) -> str:
    """Get a response from the AI model based on user input."""
    messages = [("human", user_message)]
    chain = llm | parser
    return chain.invoke(messages)

def load_environment() -> None:
    """Load environment variables from the .env file."""
    load_dotenv()

def get_api_key() -> str:
    """Retrieve the OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")

# def main():
#     load_environment()
#     api_key = get_api_key()
#     base_url = "https://api.avalai.ir/v1"
#     model = "gpt-3.5-turbo-0125"
#     user_message = "What is the capital of France?"

#     llm = initialize_chat_openai(model, base_url, api_key)
#     parser = StrOutputParser()
#     response = get_ai_response(user_message, llm, parser)

#     print("AI:", response)

# if __name__ == "__main__":
#     main()