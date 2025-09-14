import csv
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

def carregar_produtos_csv(filepath):
    produtos = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['preco'] = float(row['preco'])
                row['estoque'] = int(row['estoque'])
                row['em_promocao'] = row['em_promocao'].lower() == 'true'
                produtos.append(row)
        print(f"Sucesso: {len(produtos)} produtos carregados do arquivo '{filepath}'.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
        return []
    return produtos


produtos_loja = carregar_produtos_csv('produtos.csv')
info_geral = [
    {"tipo": "pagamento", "conteudo": "Aceitamos Cartão de Crédito, PIX e Boleto."},
    {"tipo": "horario", "conteudo": "Funcionamos de segunda a sábado, das 9h às 20h."}
]

documentos = []
if produtos_loja:
    for produto in produtos_loja:
        conteudo = (
            f"Nome do Produto: {produto['nome']}\n"
            f"Categoria: {produto['categoria']}\n"
            f"Descrição: {produto['descricao']}\n"
            f"Preço: R$ {produto['preco']:.2f}\n"
            f"Unidades em Estoque: {produto['estoque']}\n" 
            f"Em promoção: {'Sim' if produto['em_promocao'] else 'Não'}"
        )
        doc = Document(page_content=conteudo, metadata={"id": produto["id"], "nome": produto["nome"]})
        documentos.append(doc)

    for info in info_geral:
        doc = Document(page_content=info['conteudo'], metadata={"tipo": info["tipo"]})
        documentos.append(doc)
        
    produtos_em_promocao = [p['nome'] for p in produtos_loja if p['em_promocao']]
    if produtos_em_promocao:
        conteudo_resumo = (
            "Estes são todos os produtos que estão em promoção atualmente na loja: "
            + ", ".join(produtos_em_promocao)
        )
        doc_resumo = Document(page_content=conteudo_resumo, metadata={"tipo": "resumo_promocao"})
        documentos.append(doc_resumo)


    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    qdrant = QdrantVectorStore.from_documents(
        documentos,
        embeddings,
        path="./qdrant_db",
        collection_name="loja_varejista",
    )

    print("Banco de dados vetorial carregado")
    qdrant.client.close()

else:
    print("Erro")