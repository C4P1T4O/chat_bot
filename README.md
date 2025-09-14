# Chatbot de Produtos com Google Gemini

Este é um projeto de chatbot inteligente, desenvolvido para responder a perguntas sobre um catálogo de produtos específico. Ele utiliza a API do Google Gemini para processar a linguagem natural e fornecer respostas precisas com base nos dados fornecidos em um arquivo CSV.

## Funcionalidades

-   **Processamento de Linguagem Natural:** Utiliza o poder da LLM do Google Gemini para entender as perguntas dos usuários.
-   **Base de Conhecimento Customizável:** Os produtos e suas informações são carregados a partir de um simples arquivo `produtos.csv`, facilitando a atualização e gestão do catálogo.
-   **Ingestão de Dados:** Um script (`ingest.py`) processa e prepara os dados dos produtos para que o chatbot possa utilizá-los de forma eficiente.

## Pré-requisitos

-   Python 3.8 ou superior
-   Conta no [Google AI Studio](https://aistudio.google.com/) para obter uma chave de API do Gemini.

## Guia de Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### 1. Configure sua Chave de API

A primeira e mais importante etapa é configurar sua chave de API do Google Gemini.

1.  Dentro do arquivo .env, adicione a sua chave de API, substituindo `SUA_CHAVE_API_AQUI` pela chave que você gerou no Google AI Studio:


### 2. Instale as Dependências

Este projeto utiliza bibliotecas Python listadas no arquivo `requirements.txt`. Para instalá-las, execute o seguinte comando no seu terminal:

```bash
pip install -r requirements.txt
```

### 3. Personalize o Catálogo de Produtos

Edite o arquivo `produtos.csv` para incluir os produtos que você deseja que o chatbot conheça. Certifique-se de manter a estrutura das colunas do arquivo para que o script de ingestão funcione corretamente.

-   Abra `produtos.csv` em um editor de planilhas (como Excel, Google Sheets) ou editor de texto.
-   Altere as linhas existentes ou adicione novas com as informações dos seus produtos.

### 4. Processe os Dados dos Produtos (Ingestão)

Antes de executar o chatbot, você precisa rodar o script de ingestão. Este script irá ler o seu `produtos.csv` e preparar os dados para serem consultados pelo modelo de linguagem.

Execute o seguinte comando no terminal:

```bash
python ingest.py
```

Aguarde a conclusão do processo. Ele só precisa ser executado novamente se você fizer alterações no arquivo `produtos.csv`.

### 5. Inicie o Chatbot

Com tudo configurado e os dados processados, você pode finalmente iniciar o chatbot.

Execute o comando:

```bash
python chatbot.py
```

O terminal agora estará pronto para receber suas perguntas. Interaja com o bot e teste seu conhecimento sobre os produtos que você cadastrou!

---

## Estrutura do Projeto

```
.
├── .env                  # Arquivo para a chave de API
├── chatbot.py            # Script principal que executa a interface do chatbot
├── ingest.py             # Script para processar os dados do CSV
├── produtos.csv          # Arquivo com os dados dos produtos
├── requirements.txt      # Lista de dependências Python
└── README.md             # Este arquivo
```