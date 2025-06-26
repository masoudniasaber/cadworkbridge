from ninja import Router, Form
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# ✅ Just try to load .env from wherever the current working directory is
load_dotenv()

# ✅ Set up router
router_chatbot = Router(tags=["Chatbot"])

# ✅ Load LLM with env var
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)

@router_chatbot.post("/")
def post_chatbot(request, message: str = Form(...)):
    trigger_words = ["document", "pdf", "title", "summary", "content", "text", "info", "information"]

    if any(word in message.lower() for word in trigger_words):
        try:
            loader = PyPDFLoader("bridge/static/pdf/example.pdf")
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            qa_chain = load_qa_chain(llm, chain_type="stuff")
            result = qa_chain.run(input_documents=chunks, question=message)

            return {"response": result}

        except Exception as e:
            return {"response": f"PDF load error: {str(e)}"}
    else:
        reply = llm.invoke([HumanMessage(content=message)])
        return {"response": reply.content}
