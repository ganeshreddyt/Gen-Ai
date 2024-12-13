from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(groq_api_key=api_key, model_name='llama3-8b-8192')

if __name__ == "__main__":
    response = llm.invoke("Name 4 yugas in sanathana dharma ?")
    print(response.content)

