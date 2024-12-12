# PDF Chat API

## Overview

The **PDF Chat API** is a backend service built with **FastAPI** that enables you to:

1. Upload PDF documents.
2. Extract text and metadata from the uploaded PDFs.
3. Interact with the PDF content using a Large Language Model (LLM)—Google’s Gemini API in this example.
4. Query the PDF content through a chat-like interface and receive context-aware answers.
5. Utilize Retrieval-Augmented Generation (RAG) for large PDFs to improve query efficiency and accuracy.

This application demonstrates:

- Integration with an external LLM (Gemini).
- PDF text extraction and preprocessing.
- Rate limiting to manage request frequency.
- Robust logging and error handling.
- Comprehensive integration testing.
- Containerization with Docker.
- **RAG Approach** : Splits large PDFs into chunks, indexes them in a vector store, and retrieves only relevant chunks for each query.

## Key Features

- **Upload PDF Files**: Upload a PDF and get a unique `pdf_id`.
- **Chat with a PDF**: Query previously uploaded PDF content, now enhanced with a RAG approach.
- **LLM Integration (Gemini)**: Uses the Gemini model for generating intelligent responses.
- **RAG (Retrieval-Augmented Generation)**:  
  - Splits PDFs into chunks.
  - Embeds chunks and stores them in a vector database (e.g., Chroma).
  - Retrieves only the most relevant chunks for each query, making LLM responses more accurate and efficient.
- **Rate Limiting**: Implements `slowapi` to prevent abuse.
- **Logging**: Writes logs to console and rotating log files, with separate error logs.
- **Testing**: Integration tests for PDF upload and chat functionalities.
- **Docker**: Easily build and run the application in a containerized environment.

## Project Structure

```
PDF-Chat-API/
├─ app/
│  ├─ core/
│  │  ├─ config.py
│  │  └─ logger.py
│  ├─ models/
│  │  └─ state.py
│  ├─ routers/
│  │  ├─ pdf.py
│  │  └─ chat.py
│  ├─ services/
│  │  ├─ pdf_service.py       # Processes PDF and stores chunks in vector DB
│  │  ├─ llm_service.py       # Uses RAG approach to retrieve chunks & query LLM
│  │  └─ rag_service.py       # Handles chunking, embedding, and vector storage
│  ├─ utils/
│  │  └─ pdf_utils.py
│  └─ main.py
├─ tests/
│  ├─ test_chat.py
│  ├─ test_pdf.py
│  └─ dummy.pdf
├─ logs/
│  ├─ app.log
│  └─ error.log
├─ requirements.txt
├─ Dockerfile
├─ .env (not committed to version control)
└─ README.md
```

### Branches and Versions

- **Main Branch**: The `main` branch includes the RAG (Retrieval-Augmented Generation) implementation, providing advanced chunking and vector store retrieval for large PDFs.

- **Dev Branch**: If you prefer a simpler version without the RAG integration, check out the `dev` branch. This branch contains a "softer" version of the application, focusing on direct PDF-to-LLM interactions without the complexity of chunking and vector retrieval.

## Setup Instructions

### 1. Prerequisites

- **Python 3.9+** recommended.
- A **Google Gemini API Key** (`GEMINI_API_KEY`).

### 2. Clone the Repository

```bash
git clone https://github.com/kerem-ozt/PDF-Chat-API.git
cd PDF-Chat-API
```

### 3. Create and Activate a Virtual Environment (If Running Locally)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- **FastAPI**, **uvicorn**, **gunicorn**: For the API server.
- **python-dotenv**: For environment variables.
- **google-generativeai**: Integrates with the Gemini API.
- **pypdf**: PDF text extraction.
- **slowapi**: Rate limiting.
- **python-json-logger**: JSON formatted logs.
- **fpdf**, **pytest**: For testing.
- **sentence-transformers**, **chromadb**: For RAG approach (embeddings, vector store).
- **faiss-cpu** CPU optimization.

### 5. Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Ensure `.env` is in `.gitignore` to avoid committing it.

### 6. Running the Application Locally

```bash
uvicorn app.main:app --reload
```

The app runs at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 7. Docker Usage

A `Dockerfile` is included.

**Build the image:**
```bash
docker build -t pdf-chat-api .
```

**Run the container:**
Supply the `GEMINI_API_KEY` at runtime:
```bash
docker run -p 8000:8000 -e GEMINI_API_KEY=your_actual_key pdf-chat-api
```

Access at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 8. API Endpoints

#### Health Check

- **GET** `/health`
- **Checks:** API availability.
- **Rate Limit:** 1 request/minute.

**Example:**
```bash
curl http://127.0.0.1:8000/health
```

#### Upload PDF

- **POST** `/v1/pdf`
- **Description:** Upload a PDF, store its text as chunks in a vector database, returns `pdf_id`.
- **Input:** `multipart/form-data` with `file`.
- **Rate Limit:** 5 requests/minute.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/v1/pdf" \
-F "file=@/path/to/your.pdf"
```

**Response:**
```json
{
  "pdf_id": "unique_pdf_identifier"
}
```

#### Chat with PDF (RAG Enabled)

- **POST** `/v1/chat/{pdf_id}`
- **Description:** Queries the PDF by retrieving relevant chunks via RAG and then sending them to LLM for an answer.
- **Input:** JSON body with `"message"`.
- **Rate Limit:** 3 requests/minute.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/v1/chat/{pdf_id}" \
-H "Content-Type: application/json" \
-d '{"message":"What is this PDF about?"}'
```

**Response:**
```json
{
  "response": "The PDF is about ..."
}
```

### 9. Logging

- **app.log**: INFO and above, uses `RotatingFileHandler`.
- **error.log**: ERROR and above.
- Console logs in JSON format.
- Check logs via `tail -f logs/app.log`.

### 10. Testing

Integration tests in `tests/`:

- `test_pdf.py`: Tests PDF upload.
- `test_chat.py`: Tests chat endpoint (with PDF upload first).

Run tests:
```bash
python -m pytest
```