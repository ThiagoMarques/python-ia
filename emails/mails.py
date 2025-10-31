import os
import re
import json
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


BASE_DIR = Path(__file__).resolve().parent
RESUMOS_FILE = BASE_DIR / "resumos.txt"

load_dotenv(BASE_DIR.parent / ".env")

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def resume_email(email):
    print("Gerando resumos dos emails...")
    if not email:
        print("Email não encontrado.")
        return None

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Erro: variável de ambiente GEMINI_API_KEY não encontrada.")
        return None

    try:
        lista_de_resumos = []
        model = genai.GenerativeModel('gemini-2.5-flash')
        #isinstance verifica se o email é um dicionário
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
        #getattr retorna resumo.text se existir, caso contrario retorna None
        lista_de_resumos.append(getattr(resume, 'text', None))  
        salvar_resumos(getattr(resume, 'text', None))
        return getattr(resume, 'text', None)
    except Exception as e:
        print(f"Erro ao gerar resumos dos emails: {e}")
        return None


def _extract_json(text: str) -> str:
    if not text:
        return ''
    fenced = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    return text.strip()

def salvar_resumos(resumos):
    if not resumos:
        print("Nenhum resumo para salvar.")
        return

    if isinstance(resumos, str):
        resumos = [resumos]

    proximo_indice = 1
    try:
        with RESUMOS_FILE.open('r', encoding='utf-8') as f:
            existentes = re.findall(r'Resumo do e-mail (\d+):', f.read())
            if existentes:
                proximo_indice = int(existentes[-1]) + 1
    except FileNotFoundError:
        pass

    with RESUMOS_FILE.open('a', encoding='utf-8') as f:
        for deslocamento, resumo in enumerate(resumos):
            indice = proximo_indice + deslocamento
            f.write(f'Resumo do e-mail {indice}:\n')
            f.write(f"{resumo.strip()}\n\n")
    print("Resumos salvos com sucesso.")

def carregar_resumos():
    with RESUMOS_FILE.open('r', encoding='utf-8') as f:
        return f.readlines()
    print("Resumos carregados com sucesso.")
    return None

def main():
    quantidade_de_emails = 2
    print(f"Gerando {quantidade_de_emails} emails...")
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Erro: variável de ambiente GEMINI_API_KEY não encontrada.")
        return

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = (
            f"Gere exatamente {quantidade_de_emails} emails fictícios no formato JSON."
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
