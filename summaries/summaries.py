import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "example.csv"
OUTPUT_FILE = BASE_DIR / "example_summary.csv"


load_dotenv(BASE_DIR.parent / ".env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_summary(text: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(text)
    return response.text


def main() -> None:
    df = pd.read_csv(DATA_FILE)
    if "text" not in df.columns:
        raise KeyError("O arquivo example.csv deve conter uma coluna 'text'.")

    for index, row in df.iterrows():
        summary = generate_summary(row["text"])
        df.at[index, "summary"] = summary

    df.to_csv(OUTPUT_FILE, index=False)
    print("Resumo gerado com sucesso em", OUTPUT_FILE)


if __name__ == "__main__":
    main()

