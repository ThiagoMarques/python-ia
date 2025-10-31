import csv
import os
from io import StringIO
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

BASE_DIR = Path(__file__).resolve().parent
CIDADES_FILE = BASE_DIR / "cidades.txt"
PLANNING_FILE = BASE_DIR / "planning.csv"

load_dotenv(BASE_DIR.parent / ".env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_routes():
    model = genai.GenerativeModel('gemini-2.5-flash')
    quantidade_de_rotas = 2
    cidades = CIDADES_FILE.read_text(encoding="utf-8").strip()
    print(f"Cidades: {cidades}")
    prompt = (
        f"Gere {quantidade_de_rotas} rotas de viagem entre as cidades abaixo: {cidades} e exiba:\n"
        "- Percurso: (em uma única linha)\n"
        "- Distância: (em km)\n"
        "- Tempo de viagem: (em horas)\n"
        "- Custo da viagem: (em reais)\n"
        "- Tipo de viagem: (ex: 'Ida e volta', 'Ida', 'Volta')\n"
        "- Tipo de transporte: (ex: 'Avião', 'Carro', 'Ônibus', 'Trem')\n"
        "- Tipo de hospedagem: (ex: 'Hotel', 'Pousada', 'Hostel')\n"
        "- Tipo de alimentação: (ex: 'Restaurante', 'Bar', 'Lanchonete')\n"
        "- Tipo de atividade: (ex: 'Shopping', 'Museu', 'Praia', 'Parque', 'Outro')\n"
        "- Gasto estimado: (em reais)"
    )
    response = model.generate_content(prompt)
    return response.text

def save_routes(routes):
    if PLANNING_FILE.exists():
        PLANNING_FILE.unlink()
    if not routes:
        print("Nenhuma rota encontrada.")
        return
    if isinstance(routes, str):
        routes = [routes]
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = (
        "Faça um resumo das rotas de viagem abaixo e devolva cada rota em uma linha pronta para CSV, usando ';' como separador e sem usar ';' dentro dos valores:\n"
        "Rotas:\n"
        f"{chr(10).join(routes)}\n"
        "Formato desejado por linha: Percurso; Distância; Tempo de viagem; Custo da viagem; Tipo de viagem; Tipo de transporte; Tipo de hospedagem; Tipo de alimentação; Tipo de atividade; Gasto estimado."
    )
    response = model.generate_content(prompt)
    print(f"Resumo para csv: {response.text}")
    with PLANNING_FILE.open('a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        lines = [line.strip("-• ") for line in response.text.splitlines() if line.strip()]
        for line in lines:
            parsed = next(csv.reader(StringIO(line), delimiter=';'))
            columns = [col.strip().strip('"').replace('""', '"') for col in parsed]
            writer.writerow(columns)
    print("Rotas salvas com sucesso.")

def main():
    routes = generate_routes()
    print(f"Rotas: {routes}")
    save_routes(routes)
if __name__ == "__main__":
    main()