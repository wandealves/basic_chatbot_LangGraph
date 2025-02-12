from litellm import completion
import os
from dotenv import load_dotenv

def main():
    print("Hello from basic-chatbot-langgraph!")
    load_dotenv ()
    os.environ['DEEPSEEK_API_KEY'] = os.getenv ("DEEPSEEK_API_KEY")
    response = completion(
        model="deepseek/deepseek-chat", 
        messages=[
            {"role": "user", "content": "Qual a capital do Brasil"}
        ],
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
