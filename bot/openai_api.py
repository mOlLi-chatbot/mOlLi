import os

import psycopg2
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from psycopg2.extras import RealDictCursor
import bot.settings as settings


def get_db_connection():
    """Establish and return a database connection."""
    load_dotenv()  # Load environment variables from .env file
    host = os.getenv('DB_SERVICE_NAME')
    if settings.DEBUG:
        host = os.getenv('DB_HOST')
    return psycopg2.connect(
        host=host,
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
    )

def save_chat_to_db(session_id: str, user_message: str, ai_response: str) -> None:
    """Save a chat interaction to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO chat_history (session_id, user_message, ai_response)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (session_id, user_message, ai_response))
    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history(session_id: str) -> list[dict]:
    """Retrieve chat history for a given session."""
    if session_id is None:
        return []
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT user_message, ai_response, timestamp
    FROM chat_chathistory
    WHERE session_id = %s
    ORDER BY timestamp ASC
    """
    cursor.execute(query, (session_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history

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


def get_ai_response_with_history(
    session_id: str,
    user_message: str,
    llm: ChatOpenAI,
    parser: StrOutputParser,
    save_to_db=False
) -> str:
    """Get AI response while considering chat history."""
    # Retrieve history
    history = get_chat_history(session_id)

    # Format history for the prompt
    formatted_history = [
        f"User: {entry['user_message']}\nAI: {entry['ai_response']}"
        for entry in history
    ]
    formatted_prompt = "\n".join(formatted_history)
    full_prompt = f"{formatted_prompt}\nUser: {user_message}"

    # Get AI response
    messages = [("human", full_prompt)]
    chain = llm | parser
    response = chain.invoke(messages)

    # Save the new interaction
    if save_to_db:
        save_chat_to_db(session_id, user_message, response)

    return response


def load_environment() -> None:
    """Load environment variables from the .env file."""
    load_dotenv()


def get_api_key() -> str:
    """Retrieve the OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")


def main():
    load_environment()
    api_key = get_api_key()
    base_url = "https://api.avalai.ir/v1"
    model = "gpt-4o-mini"
    session_id = "unique_session_id_123"  # Replace with a dynamic session ID

    llm = initialize_chat_openai(model, base_url, api_key)
    parser = StrOutputParser()

    while True:
        user_message = input("You: ")
        if user_message.lower() in {"exit", "quit"}:
            break

        response = get_ai_response_with_history(session_id, user_message, llm, parser)
        print("AI:", response)

if __name__ == "__main__":
    main()
