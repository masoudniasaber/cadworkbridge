from ninja import NinjaAPI, Form
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api = NinjaAPI()

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.get("/hello")
def hello(request):
    return {"message": "Hello from Django Ninja"}

# Set up ChatOpenAI
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)

@api.post("/chat")
def chat(request, message: str = Form(...)):
    # Trigger words that signal document-based question
    trigger_words = ["document", "pdf", "title", "summary", "content", "text", "info", "information"]

    if any(word in message.lower() for word in trigger_words):
        try:
            loader = PyPDFLoader("bridge/static/pdf/example.pdf")
            docs = loader.load()

            # Split to avoid token overflow
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            qa_chain = load_qa_chain(llm, chain_type="stuff")
            result = qa_chain.run(input_documents=chunks, question=message)

            return {"response": result}

        except Exception as e:
            return {"response": f"PDF load error: {str(e)}"}

    else:
        # Default LLM reply
        reply = llm.invoke([HumanMessage(content=message)])
        return {"response": reply.content}
