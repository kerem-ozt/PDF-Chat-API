import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    sample_pdf_path = "tests/dummy.pdf"
    if not os.path.exists(sample_pdf_path):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="This is a sample PDF for testing.", ln=True)
        pdf.output(sample_pdf_path)
    
    with open(sample_pdf_path, "rb") as f:
        response = client.post(
            "/v1/pdf",
            files={"file": ("dummy.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    json_response = response.json()
    assert "pdf_id" in json_response
    assert len(json_response["pdf_id"]) > 0
