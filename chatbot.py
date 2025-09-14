import os
from dotenv import load_dotenv
import qdrant_client

from langchain_qdrant import QdrantVectorStore

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()


if "GOOGLE_API_KEY" not in os.environ:
    print("Erro: GOOGLE_API_KEY não encontrada. Crie um arquivo .env.")
    exit()


embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
DB_PATH = "./qdrant_db"


client = qdrant_client.QdrantClient(path=DB_PATH)


vectorstore = QdrantVectorStore(
    client=client,
    collection_name="loja_varejista",
    embedding=embedding,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", 
    temperature=0.1
)

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 30}), 
    llm=llm
)

prompt_template = """
Você é um assistente de vendas de uma loja de varejo. Sua tarefa é responder às perguntas dos clientes de forma amigável e precisa, utilizando APENAS as informações fornecidas no contexto abaixo.

**Regras Importantes:**
1.  Baseie sua resposta estritamente nas informações encontradas no contexto. Não invente produtos, preços ou promoções.
2.  Se a resposta para a pergunta não estiver no contexto, diga educadamente que você não possui essa informação no momento.
3.  Os produtos em promoção estão listados com a variavel em_promoçao == True

**Contexto Fornecido pelo Sistema de Busca:**
{context}

**Pergunta do Cliente:**
{question}

**Resposta do Assistente:**
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever_from_llm,
    return_source_documents=False, 
    chain_type_kwargs={"prompt": PROMPT}
)


if __name__ == "__main__":
    print("Assistente virtual iniciado")
    while True:
        try:
            query = input("\nVocê: ")
            if query.lower() in ["sair", "exit", "quit"]:
                print("Até logo!")
                break
            result = qa_chain.invoke({"query": query})
            print(f"Assistente: {result['result']}")
        except (KeyboardInterrupt, EOFError):
            print("\nAté logo!")
            break