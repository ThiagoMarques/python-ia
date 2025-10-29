import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def main():
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = input("Digite sua pergunta: ")
        while prompt != 'fim':
            resposta = model.generate_content(prompt)
            print(resposta.text)
            prompt = input("Digite sua pergunta: ")
    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")

if __name__ == "__main__":
    main()
