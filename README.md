# python-ia

Projeto de exemplos em Python para consumir a API do Google Gemini (google-generativeai).

## Requisitos
- Python 3.10 ou superior (recomendado). Python 3.9 funciona, mas pode emitir avisos de EOL/SSL.
- Conta e chave de API do Gemini.

## Instalação
```bash
# navegue até a pasta do projeto (ajuste o caminho conforme seu ambiente)
cd python-ia

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração
Crie um arquivo `.env` na raiz do projeto com sua chave:
```bash
echo "GEMINI_API_KEY=SEU_TOKEN_AQUI" > .env
echo "GROQ_API_KEY=SEU_TOKEN_DA_GROQ_AQUI" >> .env
```

## Execução
- Gerar 10 e-mails de exemplo e resumos:
```bash
python mails.py
```

- Exemplo simples de chamada ao Gemini (arquivo de exemplo):
```bash
python basic_gemini.py
```

- Exemplo simples usando a Groq (LLM via SDK `groq`):
```bash
python llm.py
```

## Notas
- Se estiver em Python 3.9, podem aparecer avisos como FutureWarning e NotOpenSSLWarning. Não bloqueiam a execução, mas recomenda-se atualizar para Python 3.10+.
- O script `mails.py` tenta forçar a resposta do modelo em JSON. Se a resposta vier cercada em bloco ```json, o script faz a extração e o parsing automaticamente.
- Para depurar, você pode imprimir o texto bruto retornado pelo modelo antes de fazer o `json.loads`.

## Estrutura
- `mails.py`: gera 10 e-mails fictícios (assunto, corpo, destinatário) e cria um resumo para cada um.
- `basic_gemini.py`: exemplo mínimo de uso do Gemini.
- `requirements.txt`: dependências do projeto.

## Solução de problemas
- Erro de variável de ambiente: verifique se `GEMINI_API_KEY` está definido no `.env`.
- Problemas de SSL/OpenSSL no macOS antigo: atualize Python via `pyenv`/`brew` e recrie o `venv`.
