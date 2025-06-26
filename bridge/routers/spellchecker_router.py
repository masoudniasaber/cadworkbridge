from ninja import Router, File
from ninja.files import UploadedFile
import tempfile, os

from ..services.spellchecker_service import (
    extract_pdf_text,
    post_proofread_pdf,
    clean_spellcheck_response,
)

router_spellchecker = Router(tags=["Spell Checker"])

@router_spellchecker.post("/spellcheck/")
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

@router_spellchecker.get("/check-openai-key/")
def check_openai_key(request):
    key = os.getenv("OPENAI_API_KEY")
    return {
        "key_found": bool(key),
        "starts_with": key[:5] + "..." if key else "❌ Not set"
    }
