import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def resume_email(email):
    print("Gerando resumo do email...")
    if not email:
        print("Email não encontrado.")
        return None

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Erro: variável de ambiente GEMINI_API_KEY não encontrada.")
        return None

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        //isinstance verifica se o email é um dicionário
        assunto = email.get('assunto') if isinstance(email, dict) else None
        corpo = email.get('corpo') if isinstance(email, dict) else None
        destinatario = email.get('destinatario') if isinstance(email, dict) else None

        contents = (
            "Gere um resumo conciso (1-2 frases) deste email. "
            "Formato: 'Resumo: <texto>'.\n" 
            f"Assunto: {assunto}\n"
            f"Destinatário: {destinatario}\n"
            f"Corpo: {corpo}"
        )
        resume = model.generate_content(contents=contents)
        //getattr retorna resumo.text se existir, caso contrario retorna None
        return getattr(resume, 'text', None)
    except Exception as e:
        print(f"Erro ao gerar resumo do email: {e}")
        return None


def _extract_json(text: str) -> str:
    if not text:
        return ''
    fenced = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    return text.strip()

def main():
    print("Gerando emails...")

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Erro: variável de ambiente GEMINI_API_KEY não encontrada.")
        return

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = (
            "Gere exatamente 10 emails fictícios no formato JSON. "
            "Retorne um array JSON de objetos com as chaves: "
            "'assunto', 'corpo', 'destinatario'. "
            "Não inclua nenhum texto fora do JSON."
        )

        response = model.generate_content(prompt)
        text = getattr(response, 'text', '')
        if not text:
            print("Resposta vazia da API.")
            return
        parsed = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            cleaned = _extract_json(text)
            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                print(text)
                return

        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        if isinstance(parsed, list):
            for email in parsed:
                resume = resume_email(email)
                if resume:
                    print(resume)
                print("-" * 100)



    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")

if __name__ == "__main__":
    main()
