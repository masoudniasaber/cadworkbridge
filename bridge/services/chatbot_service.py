from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0.3
)

# ✅ Main chat handler logic
def handle_chat(message: str) -> str:
    trigger_words = ["document", "pdf", "title", "summary", "content", "text", "info", "information"]

    if any(word in message.lower() for word in trigger_words):
        try:
            loader = PyPDFLoader("bridge/static/pdf/example.pdf")
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            qa_chain = load_qa_chain(llm, chain_type="stuff")
            result = qa_chain.run(input_documents=chunks, question=message)

            return result

        except Exception as e:
            return f"❌ PDF load error: {str(e)}"

    # ✅ Normal chat response
    reply = llm.invoke([HumanMessage(content=message)])
    return reply.content
