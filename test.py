import sqlite3 as s
import json

con = s.connect("""./qa_engine/feedback_database/feedback.sqlite3""")
cur = con.cursor()
row = cur.execute("""SELECT * FROM feedbacks""")
print(row.fetchall())


from app_config import config
from langchain_community.vectorstores import Chroma
import chromadb
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

__chroma_client1 = chromadb.PersistentClient(path=config["FeedbackDatabaseFolderPath"])

__embedding_function = SentenceTransformerEmbeddings(
    model_name=config["SentenceTransformerModel"]
)


client1 = Chroma(
    embedding_function=__embedding_function,
    client=__chroma_client1,
    collection_name=config["FeedbackDatabaseCollectionName"],
)

documents = client1.similarity_search(query="iit delhi student", k=1)
ids = []
for document in documents:
    qid = document.metadata["question-id"]
    print(qid)
    row = cur.execute(
        """SELECT article_id_list FROM feedbacks where question_id = ?""", (qid,)
    )
    row = row.fetchone()
    ids.extend(json.loads(row[0]))


__chroma_client2 = chromadb.PersistentClient(path=config["NewspaperDatabasePath"])


client2 = Chroma(
    embedding_function=__embedding_function,
    client=__chroma_client2,
    collection_name=config["NewspaperDatabaseCollectionName"],
)

result = client2.get(ids=ids)

for document in result["documents"]:
    print(document)

for metadata in result["metadatas"]:
    print(metadata)
