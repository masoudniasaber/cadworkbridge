from ninja import Router, Form
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env (for local dev)
# load_dotenv(".env")

# ✅ Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Set up router
router_chatbot = Router(tags=["Chatbot"])

# ✅ Initialize LLM
llm = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0.3
)

# ✅ Chatbot POST endpoint
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
            return {"response": f"❌ PDF load error: {str(e)}"}

    else:
        reply = llm.invoke([HumanMessage(content=message)])
        return {"response": reply.content}

# ✅ Temporary API key check route
@router_chatbot.get("/check-openai-key/")
def check_openai_key(request):
    key = os.getenv("OPENAI_API_KEY")
    return {
        "key_found": bool(key),
        "starts_with": key[:5] + "..." if key else "❌ Not set"
    }
