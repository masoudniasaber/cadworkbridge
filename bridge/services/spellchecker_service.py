import fitz  # PyMuPDF
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0.2
)

def extract_pdf_text(file_path: str) -> str:
    text = ''
    with fitz.open(file_path) as doc:
        for i, page in enumerate(doc, 1):
            content = page.get_text("text")
            if content:
                text += f"--- Page {i} ---\n{content.strip()}\n\n"
    return text

def post_proofread_pdf(full_text: str) -> str:
    prompt = f"""
You're a technical proofreader for a construction PDF.

❌ Ignore numbers, drawing references, and standard acronyms.
✅ Only list real spelling mistakes or word issues — especially in UPPERCASE titles.

⚠️ Format corrections like:
"WRONG" ➜ "CORRECT"

Preserve page numbers if visible.

Now check:
{full_text}
"""
    try:
        result = llm.invoke(prompt)
        return result.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

def clean_spellcheck_response(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.split("\n") if "➜" in line]
    return "\n".join(sorted(set(lines)))
