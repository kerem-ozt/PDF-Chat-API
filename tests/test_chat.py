import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_with_pdf():
    sample_pdf_path = "tests/dummy.pdf"
    if not os.path.exists(sample_pdf_path):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="This PDF is used for chatting test.", ln=True)
        pdf.output(sample_pdf_path)

    with open(sample_pdf_path, "rb") as f:
        upload_response = client.post(
            "/v1/pdf",
            files={"file": ("dummy.pdf", f, "application/pdf")}
        )
    assert upload_response.status_code == 200
    pdf_id = upload_response.json().get("pdf_id")
    assert pdf_id is not None

    chat_payload = {
        "message": "What is this PDF about?"
    }
    chat_response = client.post(f"/v1/chat/{pdf_id}", json=chat_payload)
    assert chat_response.status_code == 200
    json_response = chat_response.json()
    assert "response" in json_response
    assert isinstance(json_response["response"], str)
    assert len(json_response["response"]) > 0
