# python-ia

Projeto de exemplos em Python para consumir a API do Google Gemini (google-generativeai) e a Groq.

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
- Gerar e resumir e-mails (configure a quantidade direto em `emails/mails.py`, ajustando `quantidade_de_emails`):
```bash
python emails/mails.py
```

- Exemplo simples de chamada ao Gemini (arquivo de exemplo):
```bash
python basic_gemini.py
```

- Exemplo simples usando a Groq (LLM via SDK `groq`):
```bash
python groq_examples/groq_client.py
```

- Exemplo de consumo da Groq com extração em função (`llm.py`):
```bash
python groq_examples/llm.py
```

- Gerar rotas a partir da lista de cidades e salvar um CSV com os campos principais:
```bash
python routes/routes.py
```

- Gerar resumos a partir de um CSV com textos (espera coluna `text`):
```bash
python summaries/summaries.py
```

### Dicas de uso com Groq
- Modelos comuns: `llama-3.1-8b-instant` (rápido), `llama-3.1-70b-versatile` (mais capaz).
- `groq_examples/groq_client.py` mostra uma chamada direta via SDK; `groq_examples/llm.py` encapsula a criação do cliente (`get_groq_client`) e expõe `simple_chat` para reuso.
- Ajuste `model`, `prompt` e parâmetros em `simple_chat()` conforme sua necessidade.
- Garanta que `GROQ_API_KEY` esteja definido no `.env`.

## Notas
- Se estiver em Python 3.9, podem aparecer avisos como FutureWarning e NotOpenSSLWarning. Não bloqueiam a execução, mas recomenda-se atualizar para Python 3.10+.
- O script `mails.py` tenta forçar a resposta do modelo em JSON. Se a resposta vier cercada em bloco ```json, o script faz a extração e o parsing automaticamente.
- Para depurar, você pode imprimir o texto bruto retornado pelo modelo antes de fazer o `json.loads`.

## Estrutura
- `emails/`
  - `mails.py`: gera e-mails fictícios (quantidade configurável) e cria um resumo para cada um.
  - `resumos.txt`: saída cumulativa dos resumos.
- `groq_examples/`
  - `groq_client.py`: exemplo mínimo usando a Groq (chat simples).
  - `llm.py`: versão modular do consumo da Groq, com funções reutilizáveis.
- `routes/`
  - `routes.py`: gera rotas entre as cidades listadas em `cidades.txt`, resume cada rota e salva os campos principais em `planning.csv` pronto para planilha.
  - `cidades.txt`: lista de pontos de partida/destino.
  - `planning.csv`: último resultado gerado (UTF-8 BOM para abrir no Excel).
- `summaries/`
  - `summaries.py`: gera resumos para cada linha do CSV de entrada (exige coluna `text`).
  - `example.csv`: arquivo de exemplo com textos.
- `basic_gemini.py`: exemplo mínimo de uso do Gemini.
- `requirements.txt`: dependências do projeto.

## Solução de problemas
- Erro de variável de ambiente: verifique se `GEMINI_API_KEY` está definido no `.env`.
- Problemas de SSL/OpenSSL no macOS antigo: atualize Python via `pyenv`/`brew` e recrie o `venv`.
