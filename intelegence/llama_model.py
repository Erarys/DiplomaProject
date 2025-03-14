from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext
)

import os
from dotenv import load_dotenv


def ai_helper(question: str):
    question = f"{question}"
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=140)
    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        embed_batch_size=100
    )
    Settings.transformations = [SentenceSplitter(chunk_size=1024)]

    if not os.path.exists("storage"):
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(
            documents, embed_model=Settings.embed_model, transformations=Settings.transformations
        )
        index.storage_context.persist()
    else:
        storage_context = StorageContext.from_defaults(persist_dir="storage")
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response.response)


if __name__ == "__main__":
    answer = ai_helper("Привет мои друг")
    print(answer)