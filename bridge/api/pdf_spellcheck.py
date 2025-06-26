from ninja import Router, File
from ninja.files import UploadedFile
from langchain_openai import ChatOpenAI
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os
import tempfile

# ✅ Load .env from current folder if it exists (for local dev)
# load_dotenv(".env")

# ✅ Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Set up router
router_pdf = Router(tags=["PDF Spell Checker"])

# ✅ Initialize OpenAI client
llm = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0.2
)

# ✅ Extract text with page headers
def extract_pdf_text(file_path):
    text = ''
    with fitz.open(file_path) as doc:
        for i, page in enumerate(doc, 1):
            page_text = page.get_text("text")
            if page_text:
                text += f"--- Page {i} ---\n{page_text.strip()}\n\n"
    return text

# ✅ Send to GPT
def post_proofread_pdf(full_text):
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

# ✅ Clean GPT output
def clean_spellcheck_response(text):
    lines = [line.strip() for line in text.split("\n") if "➜" in line]
    return '\n'.join(sorted(set(lines)))

# ✅ API endpoint
@router_pdf.post("/spellcheck/")
def post_pdf_spellcheck(request, pdf: UploadedFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.read())
            tmp_path = tmp.name

        full_text = extract_pdf_text(tmp_path)
        raw_response = post_proofread_pdf(full_text)
        cleaned = clean_spellcheck_response(raw_response)

        os.remove(tmp_path)
        return {"corrections": cleaned or "✅ No mistakes found."}

    except Exception as e:
        return {"error": f"❌ Failed to process: {str(e)}"}


@router_pdf.get("/check-openai-key/")
def check_openai_key(request):
    key = os.getenv("OPENAI_API_KEY")
    return {
        "key_found": bool(key),
        "starts_with": key[:5] + "..." if key else "❌ Not set"
    }
