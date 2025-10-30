import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY não encontrado. Defina no .env ou variável de ambiente."
        )
    return Groq(api_key=api_key)


def simple_chat(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    client = get_groq_client()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=512,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    print(simple_chat("Explique em uma frase o que é a Groq."))
